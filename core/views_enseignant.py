# core/views_enseignant.py
"""
Vues pour les enseignants - Interface publique de téléversement de cours
Accessible uniquement aux enseignants (non superutilisateurs)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django import forms
from apps.utilisateurs.models_formation import Cours, Lecon
from apps.utilisateurs.forms_upload import UploadCoursForm, UploadLeconForm


def enseignant_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est enseignant (mais pas superutilisateur)"""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.est_enseignant():
            messages.error(request, "Accès réservé aux enseignants.")
            return redirect('accueil')
        if request.user.is_superuser:
            messages.error(request, "Les superutilisateurs doivent utiliser l'interface d'administration.")
            return redirect('accueil')
        return view_func(request, *args, **kwargs)
    return wrapper


@enseignant_required
def upload_cours_lecons_enseignant(request):
    """Interface pour téléverser des cours et leçons - Version enseignants"""
    # Statistiques pour les cours de cet enseignant
    mes_cours = Cours.objects.filter(enseignant=request.user, actif=True)
    total_cours = mes_cours.count()
    total_lecons = Lecon.objects.filter(cours__enseignant=request.user, actif=True).count()
    cours_recent = mes_cours.order_by('-date_creation')[:5]
    lecons_recentes = Lecon.objects.filter(
        cours__enseignant=request.user, actif=True
    ).order_by('-date_creation')[:5]
    
    context = {
        'total_cours': total_cours,
        'total_lecons': total_lecons,
        'cours_recent': cours_recent,
        'lecons_recentes': lecons_recentes,
    }
    
    return render(request, 'enseignant/upload_cours_lecons.html', context)


@enseignant_required
def upload_cours_enseignant(request):
    """Vue pour téléverser un fichier de cours - Version enseignants"""
    if request.method == 'POST':
        form = UploadCoursForm(request.POST, request.FILES)
        if form.is_valid():
            classe = form.cleaned_data['classe']
            titre = form.cleaned_data['titre']
            code = form.cleaned_data['code']
            description = form.cleaned_data.get('description', '')
            fichier_cours = form.cleaned_data['fichier_cours']
            ordre = form.cleaned_data.get('ordre', 0)
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')
            methodes_pedagogiques = form.cleaned_data.get('methodes_pedagogiques', [])
            description_methodes = form.cleaned_data.get('description_methodes', '')
            
            # L'enseignant connecté est automatiquement assigné comme enseignant
            enseignant = request.user
            
            # Vérifier si un cours avec ce code existe déjà dans cette classe
            cours_existant = Cours.objects.filter(classe=classe, code=code).first()
            
            if cours_existant:
                # Mettre à jour le cours existant (seulement si c'est le même enseignant)
                if cours_existant.enseignant != enseignant:
                    messages.error(request, "Vous ne pouvez modifier que vos propres cours.")
                    form = UploadCoursForm()
                    form.fields['enseignant'].queryset = None  # Cacher le champ enseignant
                    return render(request, 'enseignant/upload_form.html', {
                        'form': form,
                        'type': 'cours',
                    })
                
                cours_existant.titre = titre
                cours_existant.description = description
                cours_existant.enseignant = enseignant
                if date_debut:
                    cours_existant.date_debut = date_debut
                if date_fin:
                    cours_existant.date_fin = date_fin
                cours_existant.ordre = ordre
                cours_existant.actif = True
                if description_methodes:
                    cours_existant.description_methodes = description_methodes
                cours_existant.save()
                
                # Mettre à jour les méthodes pédagogiques
                if methodes_pedagogiques:
                    cours_existant.methodes_pedagogiques.set(methodes_pedagogiques)
                
                messages.success(request, f"Cours '{titre}' mis à jour avec succès.")
            else:
                # Créer un nouveau cours
                cours = Cours.objects.create(
                    classe=classe,
                    titre=titre,
                    code=code,
                    description=description or f"Cours {titre}",
                    contenu=f"Contenu du cours disponible dans le fichier téléversé.",
                    enseignant=enseignant,
                    ordre=ordre,
                    date_debut=date_debut or timezone.now().date(),
                    date_fin=date_fin or timezone.now().date(),
                    description_methodes=description_methodes,
                    actif=True
                )
                
                # Ajouter les méthodes pédagogiques
                if methodes_pedagogiques:
                    cours.methodes_pedagogiques.set(methodes_pedagogiques)
                
                messages.success(request, f"Cours '{titre}' créé avec succès.")
            
            # Stocker le fichier dans le système de fichiers Django
            cours_final = cours_existant if cours_existant else cours
            if cours_final:
                # Utiliser le système de fichiers Django pour sauvegarder le fichier
                from django.core.files.storage import default_storage
                from django.core.files.base import ContentFile
                
                # Créer un nom de fichier unique pour éviter les collisions
                file_name = f"cours_{cours_final.id}_{timezone.now().strftime('%Y%m%d_%H%M%S')}_{fichier_cours.name}"
                file_path = default_storage.save(f'cours/fichiers/{file_name}', ContentFile(fichier_cours.read()))
                
                # Enregistrer le chemin du fichier dans les ressources pédagogiques
                file_url = default_storage.url(file_path)
                ressources = cours_final.ressources_pedagogiques or ""
                fichier_info = f"\n📎 Fichier téléversé: <a href='{file_url}' target='_blank'>{fichier_cours.name}</a> (le {timezone.now().strftime('%d/%m/%Y à %H:%M')})"
                cours_final.ressources_pedagogiques = ressources + fichier_info
                cours_final.save()
            
            messages.success(request, f"Fichier '{fichier_cours.name}' téléversé avec succès. Le fichier est disponible dans les ressources pédagogiques du cours.")
            return redirect('upload_cours_lecons_enseignant')
    else:
        form = UploadCoursForm()
        # Cacher le champ enseignant - il sera automatiquement assigné
        if 'enseignant' in form.fields:
            form.fields['enseignant'].widget = forms.HiddenInput()
            form.fields['enseignant'].required = False
            form.fields['enseignant'].initial = request.user
    
    context = {
        'form': form,
        'type': 'cours',
    }
    
    return render(request, 'enseignant/upload_form.html', context)


@enseignant_required
def upload_lecon_enseignant(request):
    """Vue pour téléverser un fichier de leçon - Version enseignants"""
    if request.method == 'POST':
        form = UploadLeconForm(request.POST, request.FILES)
        if form.is_valid():
            cours = form.cleaned_data['cours']
            titre = form.cleaned_data['titre']
            numero = form.cleaned_data.get('numero', 1)
            type_lecon = form.cleaned_data.get('type_lecon', 'lecon')
            description = form.cleaned_data.get('description', '')
            fichier_lecon = form.cleaned_data['fichier_lecon']
            ordre = form.cleaned_data.get('ordre', 0)
            duree_estimee = form.cleaned_data.get('duree_estimee', 0)
            date_dispensation = form.cleaned_data.get('date_dispensation')
            
            # Vérifier que l'enseignant est bien l'enseignant du cours
            if cours.enseignant != request.user:
                messages.error(request, "Vous ne pouvez ajouter des leçons qu'à vos propres cours.")
                form = UploadLeconForm()
                # Filtrer les cours pour ne montrer que ceux de l'enseignant
                form.fields['cours'].queryset = Cours.objects.filter(
                    enseignant=request.user, actif=True
                )
                return render(request, 'enseignant/upload_form.html', {
                    'form': form,
                    'type': 'lecon',
                })
            
            # Vérifier si une leçon avec ce numéro existe déjà pour ce cours
            lecon_existante = Lecon.objects.filter(cours=cours, numero=numero).first()
            
            if lecon_existante:
                # Mettre à jour la leçon existante
                lecon_existante.titre = titre
                lecon_existante.type_lecon = type_lecon
                lecon_existante.contenu = description or f"Leçon {numero}: {titre}"
                lecon_existante.fichier_contenu = fichier_lecon
                lecon_existante.ordre = ordre
                lecon_existante.duree_estimee = duree_estimee
                if date_dispensation:
                    lecon_existante.date_dispensation = date_dispensation
                lecon_existante.actif = True
                lecon_existante.save()
                
                messages.success(request, f"Leçon '{titre}' mise à jour avec succès et fichier téléversé.")
            else:
                # Créer une nouvelle leçon avec le fichier
                lecon = Lecon.objects.create(
                    cours=cours,
                    titre=titre,
                    numero=numero,
                    type_lecon=type_lecon,
                    contenu=description or f"Leçon {numero}: {titre}",
                    fichier_contenu=fichier_lecon,
                    ordre=ordre,
                    duree_estimee=duree_estimee,
                    date_dispensation=date_dispensation,
                    actif=True
                )
                
                messages.success(request, f"Leçon '{titre}' créée avec succès et fichier téléversé.")
            
            return redirect('upload_cours_lecons_enseignant')
    else:
        form = UploadLeconForm()
        # Filtrer les cours pour ne montrer que ceux de l'enseignant
        form.fields['cours'].queryset = Cours.objects.filter(
            enseignant=request.user, actif=True
        )
    
    context = {
        'form': form,
        'type': 'lecon',
    }
    
    return render(request, 'enseignant/upload_form.html', context)


@enseignant_required
def ajouter_lecon(request, cours_id):
    """Ajouter une leçon à un cours depuis la page de modification"""
    cours = get_object_or_404(Cours, pk=cours_id, actif=True)
    
    # Vérifier que l'enseignant est propriétaire ou co-enseignant
    if cours.enseignant != request.user and request.user not in cours.co_enseignants.all():
        messages.error(request, "Vous n'avez pas le droit d'ajouter des leçons à ce cours.")
        return redirect('modifier_cours', cours_id=cours.id)
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        numero = int(request.POST.get('numero', 1))
        type_lecon = request.POST.get('type_lecon', 'lecon')
        contenu = request.POST.get('contenu', '')
        ordre = int(request.POST.get('ordre', 0))
        duree_estimee = int(request.POST.get('duree_estimee', 0))
        date_dispensation = request.POST.get('date_dispensation') or None
        fichier_contenu = request.FILES.get('fichier_contenu')
        
        if not titre or not fichier_contenu:
            messages.error(request, "Le titre et le fichier sont obligatoires.")
            return redirect('modifier_cours', cours_id=cours.id)
        
        # Vérifier si une leçon avec ce numéro existe déjà
        lecon_existante = Lecon.objects.filter(cours=cours, numero=numero).first()
        if lecon_existante:
            messages.error(request, f"Une leçon avec le numéro {numero} existe déjà pour ce cours.")
            return redirect('modifier_cours', cours_id=cours.id)
        
        # Créer la nouvelle leçon
        lecon = Lecon.objects.create(
            cours=cours,
            titre=titre,
            numero=numero,
            type_lecon=type_lecon,
            contenu=contenu or f"Leçon {numero}: {titre}",
            fichier_contenu=fichier_contenu,
            ordre=ordre,
            duree_estimee=duree_estimee,
            date_dispensation=date_dispensation,
            actif=True
        )
        
        messages.success(request, f"Leçon '{titre}' ajoutée avec succès.")
        return redirect('modifier_cours', cours_id=cours.id)
    
    return redirect('modifier_cours', cours_id=cours.id)


@enseignant_required
def modifier_lecon(request, cours_id, lecon_id):
    """Modifier une leçon depuis la page de modification du cours"""
    cours = get_object_or_404(Cours, pk=cours_id, actif=True)
    lecon = get_object_or_404(Lecon, pk=lecon_id, cours=cours, actif=True)
    
    # Vérifier que l'enseignant est propriétaire ou co-enseignant
    if cours.enseignant != request.user and request.user not in cours.co_enseignants.all():
        messages.error(request, "Vous n'avez pas le droit de modifier les leçons de ce cours.")
        return redirect('modifier_cours', cours_id=cours.id)
    
    if request.method == 'POST':
        titre = request.POST.get('titre')
        numero = int(request.POST.get('numero', lecon.numero))
        type_lecon = request.POST.get('type_lecon', lecon.type_lecon)
        contenu = request.POST.get('contenu', lecon.contenu)
        ordre = int(request.POST.get('ordre', lecon.ordre))
        duree_estimee = int(request.POST.get('duree_estimee', lecon.duree_estimee))
        date_dispensation = request.POST.get('date_dispensation') or None
        fichier_contenu = request.FILES.get('fichier_contenu')
        
        if not titre:
            messages.error(request, "Le titre est obligatoire.")
            return redirect('modifier_cours', cours_id=cours.id)
        
        # Vérifier si une autre leçon avec ce numéro existe déjà
        if numero != lecon.numero:
            lecon_existante = Lecon.objects.filter(cours=cours, numero=numero).exclude(pk=lecon.id).first()
            if lecon_existante:
                messages.error(request, f"Une leçon avec le numéro {numero} existe déjà pour ce cours.")
                return redirect('modifier_cours', cours_id=cours.id)
        
        # Mettre à jour la leçon
        lecon.titre = titre
        lecon.numero = numero
        lecon.type_lecon = type_lecon
        lecon.contenu = contenu
        lecon.ordre = ordre
        lecon.duree_estimee = duree_estimee
        if date_dispensation:
            lecon.date_dispensation = date_dispensation
        elif date_dispensation == '':
            lecon.date_dispensation = None
        
        # Mettre à jour le fichier seulement si un nouveau fichier est fourni
        if fichier_contenu:
            lecon.fichier_contenu = fichier_contenu
        
        lecon.save()
        
        messages.success(request, f"Leçon '{titre}' modifiée avec succès.")
        return redirect('modifier_cours', cours_id=cours.id)
    
    return redirect('modifier_cours', cours_id=cours.id)


@enseignant_required
def supprimer_lecon(request, cours_id, lecon_id):
    """Supprimer une leçon depuis la page de modification du cours"""
    cours = get_object_or_404(Cours, pk=cours_id, actif=True)
    lecon = get_object_or_404(Lecon, pk=lecon_id, cours=cours, actif=True)
    
    # Vérifier que l'enseignant est propriétaire ou co-enseignant
    if cours.enseignant != request.user and request.user not in cours.co_enseignants.all():
        messages.error(request, "Vous n'avez pas le droit de supprimer les leçons de ce cours.")
        return redirect('modifier_cours', cours_id=cours.id)
    
    if request.method == 'POST':
        titre = lecon.titre
        lecon.actif = False  # Soft delete
        lecon.save()
        messages.success(request, f"Leçon '{titre}' supprimée avec succès.")
    
    return redirect('modifier_cours', cours_id=cours.id)
