# apps/evaluations/views_stage.py
"""
Vues pour les évaluations de stage basées sur les jalons
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Prefetch
from django.views.decorators.http import require_http_methods
from .models_stage import EvaluationStage, EvaluationJalonStage
from .forms_stage import EvaluationStageForm, EvaluationJalonStageFormSet
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Classe, CompetenceJalon
from apps.utilisateurs.models_programme_desmfmc import StageRotationDES, CSComUCentre
from .utils_pdf import generate_evaluation_stage_pdf, generate_blank_evaluation_stage_pdf


def enseignant_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est un enseignant"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.est_enseignant() and not request.user.is_superuser:
            messages.error(request, "Accès réservé aux enseignants.")
            return redirect('accueil')
        return view_func(request, *args, **kwargs)
    return wrapper


def coordination_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est membre de la coordination"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        # TODO: Ajouter une vérification spécifique pour les membres de la coordination
        if not request.user.is_superuser:
            messages.error(request, "Accès réservé à la coordination.")
            return redirect('accueil')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@enseignant_required
def liste_evaluations_stage(request):
    """Liste des évaluations de stage créées par l'enseignant"""
    evaluations = EvaluationStage.objects.filter(
        enseignant=request.user
    ).select_related(
        'etudiant', 'classe', 'structure_stage', 'stage_rotation', 'stage_rotation__centre'
    ).prefetch_related(
        'evaluations_jalons__jalon__competence'
    ).order_by('-date_evaluation', '-date_creation')
    
    return render(request, 'evaluations/stage/liste_evaluations.html', {
        'evaluations': evaluations,
    })


@login_required
@enseignant_required
def creer_evaluation_stage(request):
    """Créer une nouvelle évaluation de stage"""
    if request.method == 'POST':
        form = EvaluationStageForm(request.POST, request.FILES, user=request.user)
        formset = EvaluationJalonStageFormSet(request.POST, instance=None)
        
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.enseignant = request.user
            evaluation.statut = 'brouillon'
            evaluation.save()
            
            # Récupérer les jalons de la classe
            classe = evaluation.classe
            jalons = CompetenceJalon.objects.filter(
                classe=classe,
                actif=True
            ).select_related('competence').order_by('competence__libelle', 'ordre', 'titre')
            
            # Créer les évaluations de jalons
            ordre = 0
            for jalon in jalons:
                EvaluationJalonStage.objects.create(
                    evaluation_stage=evaluation,
                    jalon=jalon,
                    ordre=ordre
                )
                ordre += 1
            
            messages.success(request, "Évaluation de stage créée avec succès.")
            return redirect('modifier_evaluation_stage', evaluation_id=evaluation.id)
    else:
        form = EvaluationStageForm(user=request.user)
        formset = EvaluationJalonStageFormSet(instance=None)
    
    # Récupérer les classes disponibles
    classes = Classe.objects.filter(actif=True).order_by('formation__nom', 'annee')
    
    return render(request, 'evaluations/stage/creer_evaluation.html', {
        'form': form,
        'formset': formset,
        'classes': classes,
    })


@login_required
@enseignant_required
def modifier_evaluation_stage(request, evaluation_id):
    """Modifier une évaluation de stage"""
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    # Vérifier les permissions
    if not evaluation.peut_etre_modifiee(request.user):
        messages.error(request, "Vous n'avez pas le droit de modifier cette évaluation.")
        return redirect('liste_evaluations_stage')
    
    # Récupérer ou créer les évaluations de jalons
    if not evaluation.evaluations_jalons.exists():
        classe = evaluation.classe
        jalons = CompetenceJalon.objects.filter(
            classe=classe,
            actif=True
        ).select_related('competence').order_by('competence__libelle', 'ordre', 'titre')
        
        ordre = 0
        for jalon in jalons:
            EvaluationJalonStage.objects.get_or_create(
                evaluation_stage=evaluation,
                jalon=jalon,
                defaults={'ordre': ordre}
            )
            ordre += 1
    
    if request.method == 'POST':
        form = EvaluationStageForm(request.POST, request.FILES, instance=evaluation, user=request.user)
        formset = EvaluationJalonStageFormSet(request.POST, instance=evaluation)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            # Gérer le statut selon l'action
            action = request.POST.get('action', '')
            if action == 'soumettre':
                evaluation.statut = 'soumis'
                evaluation.save()
                messages.success(request, "Évaluation soumise pour vérification.")
            else:
                messages.success(request, "Évaluation enregistrée.")
            
            return redirect('modifier_evaluation_stage', evaluation_id=evaluation.id)
    else:
        form = EvaluationStageForm(instance=evaluation, user=request.user)
        formset = EvaluationJalonStageFormSet(instance=evaluation)
    
    # Organiser les jalons par compétence pour l'affichage
    evaluations_jalons = evaluation.evaluations_jalons.select_related(
        'jalon', 'jalon__competence'
    ).order_by('jalon__competence__libelle', 'jalon__ordre', 'ordre')
    
    # Grouper par compétence
    competences_data = {}
    for eval_jalon in evaluations_jalons:
        competence = eval_jalon.jalon.competence
        if competence not in competences_data:
            competences_data[competence] = []
        competences_data[competence].append(eval_jalon)
    
    return render(request, 'evaluations/stage/modifier_evaluation.html', {
        'form': form,
        'formset': formset,
        'evaluation': evaluation,
        'competences_data': competences_data,
    })


@login_required
@enseignant_required
def supprimer_evaluation_stage(request, evaluation_id):
    """Supprimer une évaluation de stage"""
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    if not evaluation.peut_etre_modifiee(request.user):
        messages.error(request, "Vous n'avez pas le droit de supprimer cette évaluation.")
        return redirect('liste_evaluations_stage')
    
    if request.method == 'POST':
        evaluation.delete()
        messages.success(request, "Évaluation supprimée avec succès.")
        return redirect('liste_evaluations_stage')
    
    return render(request, 'evaluations/stage/supprimer_evaluation.html', {
        'evaluation': evaluation,
    })


@login_required
@coordination_required
def liste_evaluations_a_verifier(request):
    """Liste des évaluations à vérifier par la coordination"""
    evaluations = EvaluationStage.objects.filter(
        statut__in=['soumis', 'rejete']
    ).select_related(
        'etudiant', 'classe', 'structure_stage', 'enseignant', 'stage_rotation', 'stage_rotation__centre'
    ).order_by('-date_creation')
    
    return render(request, 'evaluations/stage/liste_a_verifier.html', {
        'evaluations': evaluations,
    })


@login_required
@coordination_required
def verifier_evaluation_stage(request, evaluation_id):
    """Vérifier une évaluation de stage"""
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    if not evaluation.peut_etre_verifiee(request.user):
        messages.error(request, "Vous n'avez pas le droit de vérifier cette évaluation.")
        return redirect('liste_evaluations_a_verifier')
    
    if request.method == 'POST':
        action = request.POST.get('action', '')
        commentaire = request.POST.get('commentaire_verification', '')
        
        if action == 'valider':
            evaluation.statut = 'verifie'
            evaluation.verifie_par = request.user
            from django.utils import timezone
            evaluation.date_verification = timezone.now()
            evaluation.commentaire_verification = commentaire
            evaluation.save()
            
            # Rendre disponible pour l'étudiant
            evaluation.statut = 'disponible'
            evaluation.save()
            
            messages.success(request, "Évaluation validée et mise à disposition de l'étudiant.")
        elif action == 'rejeter':
            evaluation.statut = 'rejete'
            evaluation.verifie_par = request.user
            from django.utils import timezone
            evaluation.date_verification = timezone.now()
            evaluation.commentaire_verification = commentaire
            evaluation.save()
            messages.warning(request, "Évaluation rejetée.")
        
        return redirect('liste_evaluations_a_verifier')
    
    # Organiser les jalons par compétence
    evaluations_jalons = evaluation.evaluations_jalons.select_related(
        'jalon', 'jalon__competence'
    ).order_by('jalon__competence__libelle', 'jalon__ordre', 'ordre')
    
    competences_data = {}
    for eval_jalon in evaluations_jalons:
        competence = eval_jalon.jalon.competence
        if competence not in competences_data:
            competences_data[competence] = []
        competences_data[competence].append(eval_jalon)
    
    return render(request, 'evaluations/stage/verifier_evaluation.html', {
        'evaluation': evaluation,
        'competences_data': competences_data,
    })


@login_required
def mes_evaluations_stage_etudiant(request):
    """Liste des évaluations de stage disponibles pour l'étudiant"""
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    evaluations = EvaluationStage.objects.filter(
        etudiant=request.user,
        statut='disponible'
    ).select_related(
        'classe', 'structure_stage', 'enseignant', 'stage_rotation', 'stage_rotation__centre'
    ).prefetch_related(
        'evaluations_jalons__jalon__competence'
    ).order_by('-date_evaluation')
    
    return render(request, 'evaluations/stage/mes_evaluations_etudiant.html', {
        'evaluations': evaluations,
    })


@login_required
def detail_evaluation_stage_etudiant(request, evaluation_id):
    """Détail d'une évaluation de stage pour l'étudiant"""
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    # Vérifier que l'étudiant peut voir cette évaluation
    if evaluation.etudiant != request.user and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas accès à cette évaluation.")
        return redirect('mes_evaluations_stage_etudiant')
    
    if evaluation.statut != 'disponible' and not request.user.is_superuser:
        messages.error(request, "Cette évaluation n'est pas encore disponible.")
        return redirect('mes_evaluations_stage_etudiant')
    
    # Organiser les jalons par compétence
    evaluations_jalons = evaluation.evaluations_jalons.select_related(
        'jalon', 'jalon__competence'
    ).order_by('jalon__competence__libelle', 'jalon__ordre', 'ordre')
    
    competences_data = {}
    for eval_jalon in evaluations_jalons:
        competence = eval_jalon.jalon.competence
        if competence not in competences_data:
            competences_data[competence] = []
        competences_data[competence].append(eval_jalon)
    
    return render(request, 'evaluations/stage/detail_evaluation_etudiant.html', {
        'evaluation': evaluation,
        'competences_data': competences_data,
    })


@login_required
def telecharger_evaluation_stage_pdf(request, evaluation_id):
    """Télécharger une évaluation de stage en PDF"""
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    # Vérifier les permissions
    if not request.user.is_superuser:
        if request.user.est_etudiant() and evaluation.etudiant != request.user:
            messages.error(request, "Vous n'avez pas accès à cette évaluation.")
            return redirect('mes_evaluations_stage_etudiant')
        elif request.user.est_enseignant() and evaluation.enseignant != request.user:
            messages.error(request, "Vous n'avez pas accès à cette évaluation.")
            return redirect('liste_evaluations_stage')
    
    # Générer le PDF
    pdf = generate_evaluation_stage_pdf(evaluation)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="evaluation_stage_{evaluation.id}.pdf"'
    return response


@login_required
@enseignant_required
def telecharger_grille_vierge_pdf(request, classe_id):
    """Télécharger une grille d'évaluation vierge en PDF"""
    classe = get_object_or_404(Classe, pk=classe_id)
    
    # Générer le PDF vierge
    pdf = generate_blank_evaluation_stage_pdf(classe)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="grille_evaluation_vierge_{classe.code}.pdf"'
    return response


@login_required
@require_http_methods(["GET"])
def get_etudiants_classe(request):
    """API pour récupérer les étudiants d'une classe (AJAX)"""
    classe_id = request.GET.get('classe_id')
    if not classe_id:
        return JsonResponse({'error': 'classe_id manquant'}, status=400)
    
    try:
        classe = Classe.objects.get(pk=classe_id)
        etudiants = Utilisateur.objects.filter(
            type_utilisateur='etudiant',
            classe=classe.nom
        ).order_by('last_name', 'first_name')
        
        data = [{
            'id': etudiant.id,
            'nom': etudiant.get_full_name() or etudiant.username,
            'username': etudiant.username
        } for etudiant in etudiants]
        
        return JsonResponse({'etudiants': data})
    except Classe.DoesNotExist:
        return JsonResponse({'error': 'Classe introuvable'}, status=404)


@login_required
@require_http_methods(["GET"])
def get_stages_etudiant(request):
    """API pour récupérer les stages d'un étudiant (AJAX)"""
    etudiant_id = request.GET.get('etudiant_id')
    if not etudiant_id:
        return JsonResponse({'error': 'etudiant_id manquant'}, status=400)
    
    try:
        etudiant = Utilisateur.objects.get(pk=etudiant_id)
        stages = StageRotationDES.objects.filter(
            etudiant=etudiant
        ).select_related('centre').order_by('-annee', '-periode')
        
        data = [{
            'id': stage.id,
            'annee': stage.annee,
            'periode': stage.get_periode_display(),
            'centre': str(stage.centre),
            'date_debut': stage.date_debut.strftime('%d/%m/%Y') if stage.date_debut else '',
            'date_fin': stage.date_fin.strftime('%d/%m/%Y') if stage.date_fin else '',
        } for stage in stages]
        
        return JsonResponse({'stages': data})
    except Utilisateur.DoesNotExist:
        return JsonResponse({'error': 'Étudiant introuvable'}, status=404)

