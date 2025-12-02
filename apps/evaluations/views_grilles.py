# apps/evaluations/views_grilles.py
"""
Vues pour les grilles d'évaluation avec export CSV et import Word
"""
import csv
import os
import tempfile
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse_lazy
from .models_grilles import (
    GrilleEvaluation,
    EvaluationAvecGrille,
    CritereEvaluation,
    ElementEvaluation
)
from .forms_grilles import (
    EvaluationAvecGrilleForm, ReponseCritereForm,
    GrilleEvaluationForm, CritereFormSet
)
from .forms_import import ImportGrilleWordForm
from .importers.import_word_grille import WordGrilleImporter


class GrilleEvaluationListView(LoginRequiredMixin, ListView):
    """Liste des grilles d'évaluation disponibles"""
    model = GrilleEvaluation
    template_name = 'evaluations/grilles/liste.html'
    context_object_name = 'grilles'
    paginate_by = 20
    
    def get_queryset(self):
        qs = GrilleEvaluation.objects.filter(actif=True).select_related(
            'type_grille', 'cours', 'classe', 'createur'
        ).prefetch_related('criteres')
        
        # Filtres
        type_grille = self.request.GET.get('type_grille')
        if type_grille:
            qs = qs.filter(type_grille_id=type_grille)
        
        classe = self.request.GET.get('classe')
        if classe:
            qs = qs.filter(classe_id=classe)
        
        search = self.request.GET.get('search')
        if search:
            qs = qs.filter(
                Q(titre__icontains=search) |
                Q(description__icontains=search) |
                Q(cours__titre__icontains=search)
            )
        
        return qs.order_by('-date_creation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models_grilles import TypeGrilleEvaluation
        from apps.utilisateurs.models_formation import Classe
        context['types_grilles'] = TypeGrilleEvaluation.objects.filter(actif=True)
        context['classes'] = Classe.objects.all()
        return context


class GrilleEvaluationDetailView(LoginRequiredMixin, DetailView):
    """Détails d'une grille d'évaluation"""
    model = GrilleEvaluation
    template_name = 'evaluations/grilles/detail.html'
    context_object_name = 'grille'
    
    def get_queryset(self):
        return GrilleEvaluation.objects.select_related(
            'type_grille', 'cours', 'classe', 'createur'
        ).prefetch_related(
            'criteres__elements',
            'competences_evaluees',
            'jalons_evalues'
        )


class EvaluationAvecGrilleCreateView(LoginRequiredMixin, CreateView):
    """Créer une évaluation avec une grille"""
    model = EvaluationAvecGrille
    form_class = EvaluationAvecGrilleForm
    template_name = 'evaluations/grilles/evaluer.html'
    
    def get_initial(self):
        grille = get_object_or_404(GrilleEvaluation, pk=self.kwargs['grille_id'])
        return {
            'grille': grille,
            'evaluateur': self.request.user
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grille'] = get_object_or_404(GrilleEvaluation, pk=self.kwargs['grille_id'])
        return context
    
    def form_valid(self, form):
        form.instance.evaluateur = self.request.user
        messages.success(self.request, 'Évaluation créée avec succès !')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('grilles:detail', kwargs={'pk': self.object.grille.id})


class ImportGrilleWordView(LoginRequiredMixin, FormView):
    """Vue pour importer une grille depuis un document Word"""
    template_name = 'evaluations/grilles/import_word.html'
    form_class = ImportGrilleWordForm
    success_url = reverse_lazy('grilles:liste')
    
    def form_valid(self, form):
        fichier = form.cleaned_data['fichier']
        type_grille = form.cleaned_data['type_grille']
        cours = form.cleaned_data.get('cours')
        classe = form.cleaned_data.get('classe')
        
        # Sauvegarder le fichier temporairement
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            for chunk in fichier.chunks():
                tmp_file.write(chunk)
            tmp_path = tmp_file.name
        
        try:
            # Importer la grille
            importer = WordGrilleImporter(tmp_path)
            grille = importer.create_grille(
                type_grille_id=type_grille.id,
                cours_id=cours.id if cours else None,
                classe_id=classe.id if classe else None,
                createur=self.request.user
            )
            
            messages.success(
                self.request,
                f'Grille "{grille.titre}" importée avec succès ! '
                f'({grille.criteres.count()} critères créés)'
            )
            
        except Exception as e:
            messages.error(
                self.request,
                f'Erreur lors de l\'import : {str(e)}'
            )
        finally:
            # Supprimer le fichier temporaire
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models_grilles import TypeGrilleEvaluation
        context['types_grilles'] = TypeGrilleEvaluation.objects.filter(actif=True)
        return context


def export_grille_csv(request, grille_id):
    """Exporte une grille d'évaluation en CSV"""
    grille = get_object_or_404(GrilleEvaluation, pk=grille_id)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="grille_{grille.id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['GRILLE D\'ÉVALUATION'])
    writer.writerow(['Titre', grille.titre])
    writer.writerow(['Description', grille.description])
    writer.writerow(['Type', grille.type_grille.nom])
    writer.writerow(['Note maximale', grille.note_maximale])
    writer.writerow([])
    writer.writerow(['CRITÈRES D\'ÉVALUATION'])
    writer.writerow(['Ordre', 'Libellé', 'Description', 'Poids', 'Note max'])
    
    for critere in grille.criteres.filter(actif=True).order_by('ordre'):
        writer.writerow([
            critere.ordre,
            critere.libelle,
            critere.description or '',
            critere.poids,
            critere.note_maximale or ''
        ])
        
        # Éléments
        elements = critere.elements.filter(actif=True).order_by('ordre')
        if elements.exists():
            writer.writerow(['', 'Éléments:', '', '', ''])
            for elem in elements:
                writer.writerow(['', f"  - {elem.libelle}", elem.description or '', elem.poids, ''])
        writer.writerow([])
    
    return response


def export_evaluation_csv(request, evaluation_id):
    """Exporte une évaluation complétée en CSV"""
    evaluation = get_object_or_404(EvaluationAvecGrille, pk=evaluation_id)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="evaluation_{evaluation.id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ÉVALUATION'])
    writer.writerow(['Étudiant', str(evaluation.etudiant)])
    writer.writerow(['Grille', evaluation.grille.titre])
    writer.writerow(['Date', evaluation.date_evaluation.strftime('%d/%m/%Y')])
    writer.writerow(['Note obtenue', f"{evaluation.note_obtenue or 0}/{evaluation.note_sur or 0}"])
    writer.writerow([])
    writer.writerow(['RÉPONSES PAR CRITÈRE'])
    writer.writerow(['Critère', 'Note', 'Niveau', 'Commentaire'])
    
    reponses = evaluation.reponses_criteres.select_related('critere').order_by('critere__ordre')
    for reponse in reponses:
        writer.writerow([
            reponse.critere.libelle,
            str(reponse.note or ''),
            reponse.get_niveau_display() if reponse.niveau else '',
            reponse.commentaire or ''
        ])
        
        # Réponses par élément
        reponses_elements = reponse.reponses_elements.select_related('element').order_by('element__ordre')
        if reponses_elements.exists():
            writer.writerow(['', 'Éléments:', '', ''])
            for rep_elem in reponses_elements:
                writer.writerow([
                    f"  - {rep_elem.element.libelle}",
                    str(rep_elem.note or ''),
                    rep_elem.get_niveau_display() if rep_elem.niveau else '',
                    rep_elem.commentaire or ''
                ])
        writer.writerow([])
    
    return response


class GrilleEvaluationCreateView(LoginRequiredMixin, CreateView):
    """Vue pour créer une grille d'évaluation avec critères"""
    model = GrilleEvaluation
    form_class = GrilleEvaluationForm
    template_name = 'evaluations/grilles/creer.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['critere_formset'] = CritereFormSet(self.request.POST)
        else:
            context['critere_formset'] = CritereFormSet()
        
        # Ajouter les données nécessaires pour le formulaire
        from .models_grilles import TypeGrilleEvaluation
        from apps.utilisateurs.models_formation import Classe, Cours, Competence, CompetenceJalon
        
        context['types_grilles'] = TypeGrilleEvaluation.objects.filter(actif=True)
        context['classes'] = Classe.objects.all()
        context['cours'] = Cours.objects.filter(actif=True)
        context['competences'] = Competence.objects.all()
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        critere_formset = context['critere_formset']
        
        # Sauvegarder la grille avec le créateur
        form.instance.createur = self.request.user
        self.object = form.save()
        
        # Sauvegarder les critères
        if critere_formset.is_valid():
            critere_formset.instance = self.object
            critere_formset.save()
            messages.success(
                self.request,
                f'Grille "{self.object.titre}" créée avec succès ! '
                f'({self.object.criteres.count()} critères ajoutés)'
            )
        else:
            messages.warning(
                self.request,
                'Grille créée mais certains critères ont des erreurs. '
                'Vous pouvez les modifier depuis la page de détail.'
            )
        
        return redirect('grilles:detail', pk=self.object.pk)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs dans le formulaire.')
        return super().form_invalid(form)


class GrilleEvaluationUpdateView(LoginRequiredMixin, UpdateView):
    """Vue pour modifier une grille d'évaluation"""
    model = GrilleEvaluation
    form_class = GrilleEvaluationForm
    template_name = 'evaluations/grilles/modifier.html'
    
    def get_queryset(self):
        return GrilleEvaluation.objects.select_related('type_grille', 'cours', 'classe', 'createur')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['critere_formset'] = CritereFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['critere_formset'] = CritereFormSet(instance=self.object)
        
        # Ajouter les données nécessaires
        from .models_grilles import TypeGrilleEvaluation
        from apps.utilisateurs.models_formation import Classe, Cours, Competence
        
        context['types_grilles'] = TypeGrilleEvaluation.objects.filter(actif=True)
        context['classes'] = Classe.objects.all()
        context['cours'] = Cours.objects.filter(actif=True)
        context['competences'] = Competence.objects.all()
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        critere_formset = context['critere_formset']
        
        # Sauvegarder la grille
        self.object = form.save()
        
        # Sauvegarder les critères
        if critere_formset.is_valid():
            critere_formset.save()
            messages.success(
                self.request,
                f'Grille "{self.object.titre}" modifiée avec succès !'
            )
        else:
            messages.warning(
                self.request,
                'Grille modifiée mais certains critères ont des erreurs.'
            )
        
        return redirect('grilles:detail', pk=self.object.pk)
