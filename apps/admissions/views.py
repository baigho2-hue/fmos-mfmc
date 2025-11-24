"""
Vues pour la gestion des admissions et inscriptions
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.db import transaction

from apps.utilisateurs.models_formation import Formation
from .models import (
    DossierCandidature,
    DocumentDossier,
    DocumentRequis,
    Inscription,
    DecisionAdmission,
)
from .forms import (
    DossierCandidatureForm,
    DocumentUploadForm,
    InscriptionForm,
    InscriptionPaiementForm,
)


@login_required
def creer_dossier(request):
    """Vue pour créer un nouveau dossier de candidature."""
    if request.method == 'POST':
        form = DossierCandidatureForm(request.POST, candidat=request.user)
        if form.is_valid():
            with transaction.atomic():
                # Générer une référence unique
                annee = timezone.now().year
                dernier_numero = DossierCandidature.objects.filter(
                    reference__startswith=f"DOS-{annee}-"
                ).count()
                reference = f"DOS-{annee}-{str(dernier_numero + 1).zfill(3)}"
                
                dossier = form.save(commit=False)
                dossier.candidat = request.user
                dossier.reference = reference
                dossier.statut = 'soumis'
                dossier.save()
                
                messages.success(
                    request,
                    f"Dossier créé avec succès. Référence: {reference}"
                )
                return redirect('admissions:voir_dossier', dossier_id=dossier.id)
    else:
        form = DossierCandidatureForm(candidat=request.user)
    
    # Récupérer les documents requis selon la formation sélectionnée
    formation_code = request.GET.get('formation', '')
    documents_requis = []
    if formation_code:
        try:
            formation = Formation.objects.get(code=formation_code, actif=True)
            type_formation = 'DESMFMC' if formation_code == 'DESMFMC' else 'autre'
            documents_requis = DocumentRequis.objects.filter(
                type_formation=type_formation,
                actif=True
            ).order_by('ordre')
        except Formation.DoesNotExist:
            pass
    
    context = {
        'form': form,
        'documents_requis': documents_requis,
        'formation_code': formation_code,
    }
    return render(request, 'admissions/creer_dossier.html', context)


@login_required
def voir_dossier(request, dossier_id):
    """Vue pour voir les détails d'un dossier de candidature."""
    dossier = get_object_or_404(
        DossierCandidature,
        id=dossier_id,
        candidat=request.user
    )
    
    # Récupérer les documents uploadés
    documents_uploades = dossier.documents.all().select_related('document_requis')
    
    # Récupérer les documents requis manquants
    documents_manquants = dossier.get_documents_manquants()
    
    # Vérifier la complétude
    est_complet = dossier.verifier_completude()
    
    # Récupérer la décision d'admission si elle existe
    decision = getattr(dossier, 'decision_admission', None)
    
    # Récupérer l'inscription si elle existe
    inscription = dossier.inscriptions.first()
    
    context = {
        'dossier': dossier,
        'documents_uploades': documents_uploades,
        'documents_manquants': documents_manquants,
        'est_complet': est_complet,
        'decision': decision,
        'inscription': inscription,
    }
    return render(request, 'admissions/voir_dossier.html', context)


@login_required
def uploader_document(request, dossier_id):
    """Vue pour uploader un document pour un dossier."""
    dossier = get_object_or_404(
        DossierCandidature,
        id=dossier_id,
        candidat=request.user
    )
    
    document_requis_id = request.GET.get('document_requis_id')
    if not document_requis_id:
        messages.error(request, "Document requis non spécifié.")
        return redirect('admissions:voir_dossier', dossier_id=dossier_id)
    
    document_requis = get_object_or_404(DocumentRequis, id=document_requis_id)
    
    if request.method == 'POST':
        # Vérifier si un document existe déjà
        document_existant = DocumentDossier.objects.filter(
            dossier=dossier,
            document_requis=document_requis
        ).first()
        
        form = DocumentUploadForm(
            request.POST,
            request.FILES,
            dossier=dossier,
            document_requis=document_requis
        )
        
        if form.is_valid():
            if document_existant:
                # Mettre à jour le document existant
                document_existant.fichier = form.cleaned_data['fichier']
                document_existant.valide = False  # Réinitialiser la validation
                document_existant.save()
                messages.success(request, "Document mis à jour avec succès.")
            else:
                # Créer un nouveau document
                form.save()
                messages.success(request, "Document uploadé avec succès.")
            
            return redirect('admissions:voir_dossier', dossier_id=dossier_id)
    else:
        form = DocumentUploadForm(
            dossier=dossier,
            document_requis=document_requis
        )
    
    context = {
        'form': form,
        'dossier': dossier,
        'document_requis': document_requis,
    }
    return render(request, 'admissions/uploader_document.html', context)


@login_required
def mes_dossiers(request):
    """Vue pour lister tous les dossiers d'un candidat."""
    dossiers = DossierCandidature.objects.filter(
        candidat=request.user
    ).select_related('formation').order_by('-date_depot')
    
    context = {
        'dossiers': dossiers,
    }
    return render(request, 'admissions/mes_dossiers.html', context)


@login_required
def inscription(request, dossier_id):
    """Vue pour gérer l'inscription après admission."""
    dossier = get_object_or_404(
        DossierCandidature,
        id=dossier_id,
        candidat=request.user
    )
    
    # Vérifier qu'il y a une décision d'admission positive
    try:
        decision = dossier.decision_admission
        if decision.decision != 'admis':
            messages.warning(
                request,
                "Vous devez être admis pour accéder à l'inscription."
            )
            return redirect('admissions:voir_dossier', dossier_id=dossier_id)
    except DecisionAdmission.DoesNotExist:
        messages.warning(
            request,
            "Aucune décision d'admission disponible."
        )
        return redirect('admissions:voir_dossier', dossier_id=dossier_id)
    
    # Récupérer ou créer l'inscription
    inscription_obj, created = Inscription.objects.get_or_create(
        dossier=dossier,
        defaults={
            'formation': dossier.formation,
            'decision_admission': decision,
        }
    )
    
    if request.method == 'POST':
        if inscription_obj.est_certifiante and not inscription_obj.paiement_valide:
            # Formulaire de paiement pour les formations certifiantes
            form_paiement = InscriptionPaiementForm(
                request.POST,
                request.FILES,
                instance=inscription_obj
            )
            form_inscription = InscriptionForm(instance=inscription_obj)
            
            if form_paiement.is_valid():
                inscription_obj = form_paiement.save(commit=False)
                inscription_obj.date_paiement = timezone.now()
                inscription_obj.save()
                messages.success(
                    request,
                    "Informations de paiement enregistrées. En attente de validation."
                )
                return redirect('admissions:inscription', dossier_id=dossier_id)
        else:
            # Formulaire d'inscription standard
            form_inscription = InscriptionForm(request.POST, instance=inscription_obj)
            form_paiement = InscriptionPaiementForm(instance=inscription_obj)
            
            if form_inscription.is_valid():
                form_inscription.save()
                messages.success(request, "Inscription mise à jour.")
                return redirect('admissions:inscription', dossier_id=dossier_id)
    else:
        form_inscription = InscriptionForm(instance=inscription_obj)
        form_paiement = InscriptionPaiementForm(instance=inscription_obj)
    
    context = {
        'dossier': dossier,
        'decision': decision,
        'inscription': inscription_obj,
        'form_inscription': form_inscription,
        'form_paiement': form_paiement,
    }
    return render(request, 'admissions/inscription.html', context)


@login_required
def ajax_documents_requis(request):
    """Vue AJAX pour récupérer les documents requis selon la formation."""
    formation_code = request.GET.get('formation_code', '')
    
    if not formation_code:
        return JsonResponse({'documents': []})
    
    try:
        formation = Formation.objects.get(code=formation_code, actif=True)
        type_formation = 'DESMFMC' if formation_code == 'DESMFMC' else 'autre'
        
        documents = DocumentRequis.objects.filter(
            type_formation=type_formation,
            actif=True
        ).order_by('ordre').values('id', 'nom', 'description', 'obligatoire', 'ordre')
        
        return JsonResponse({
            'documents': list(documents)
        })
    except Formation.DoesNotExist:
        return JsonResponse({'error': 'Formation non trouvée'}, status=404)
