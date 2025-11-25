""" 
Vues pour la gestion des admissions et demandes de candidature
"""
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, Http404, HttpResponse
from django.utils import timezone
from django.db import transaction
from django.db.models import Count, Q
from django.utils.dateparse import parse_date
from django.contrib.auth import get_user_model, login

from apps.utilisateurs.models_formation import Formation
from .models import (
    DossierCandidature,
    DocumentDossier,
    DocumentRequis,
    Inscription,
    DecisionAdmission,
    PaiementAnneeDES,
    SANTE_COMMUNAUTAIRE_CODE,
)
from .forms import (
    DossierCandidatureForm,
    DocumentUploadForm,
    InscriptionForm,
    InscriptionPaiementForm,
)
from apps.utilisateurs.models_programme_desmfmc import ResultatAnneeDES


def _get_document_type_for_code(formation_code: str) -> str:
    if not formation_code:
        return 'autre'
    mapping = {
        'DESMFMC': 'DESMFMC',
        SANTE_COMMUNAUTAIRE_CODE: SANTE_COMMUNAUTAIRE_CODE,
    }
    return mapping.get(formation_code, 'autre')


def creer_dossier(request):
    """Vue pour créer un nouveau dossier de candidature."""
    if request.method == 'POST':
        form = DossierCandidatureForm(request.POST, candidat=request.user if request.user.is_authenticated else None, user=request.user)
        if form.is_valid():
            with transaction.atomic():
                if not request.user.is_authenticated:
                    UserModel = get_user_model()
                    email = form.cleaned_data['email']
                    username = email
                    counter = 1
                    while UserModel.objects.filter(username=username).exists():
                        username = f"{email.split('@')[0]}{counter}"
                        counter += 1
                    new_user = UserModel.objects.create_user(
                        username=username,
                        email=email,
                        password=form.cleaned_data['password1'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                    )
                    telephone = form.cleaned_data.get('telephone')
                    if telephone:
                        new_user.telephone = telephone
                    new_user.type_utilisateur = 'etudiant'
                    new_user.save()
                    login(request, new_user)

                formation = form.cleaned_data['formation']
                formation_code = formation.code or 'DOS'
                annee = timezone.now().year
                prefix = f"{formation_code}-{annee}"
                dernier_numero = DossierCandidature.objects.filter(
                    reference__startswith=f"{prefix}-"
                ).count()
                reference = f"{prefix}-{str(dernier_numero + 1).zfill(3)}"
                
                dossier = form.save(commit=False)
                if request.user.is_authenticated:
                    dossier.candidat = request.user
                dossier.reference = reference
                dossier.statut = 'soumis'
                dossier.save()
                
                messages.success(
                    request,
                    f"Demande déposée avec succès. Référence : {reference}. Conservez-la pour vos échanges."
                )
                return redirect('admissions:voir_dossier', dossier_id=dossier.id)
    else:
        form = DossierCandidatureForm(candidat=request.user if request.user.is_authenticated else None, user=request.user)
    
    # Récupérer les documents requis selon la formation sélectionnée
    formation_code = request.GET.get('formation', '')
    documents_requis = []
    if formation_code:
        try:
            formation = Formation.objects.get(code=formation_code, actif=True)
            type_formation = _get_document_type_for_code(formation.code)
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
def suivi_dossiers_formation(request):
    """Interface de suivi des dossiers par formation (coordination / staff)."""
    if not request.user.is_authenticated:
        return redirect('login')

    est_coordination = getattr(request.user, 'est_membre_coordination', lambda: False)()
    if not (request.user.is_staff or est_coordination):
        messages.error(request, "Accès réservé à la coordination ou au personnel autorisé.")
        return redirect('accueil')

    formations = Formation.objects.filter(actif=True).order_by('nom')
    formation_code = request.GET.get('formation') or (formations.first().code if formations else None)
    search_query = request.GET.get('q', '').strip()
    start_date_param = request.GET.get('start_date', '').strip()
    end_date_param = request.GET.get('end_date', '').strip()
    export_format = request.GET.get('export')
    start_date = parse_date(start_date_param) if start_date_param else None
    end_date = parse_date(end_date_param) if end_date_param else None
    dossiers_data = []
    stats = None
    documents_requis = []
    formation_selectionnee = None

    if formation_code:
        try:
            formation_selectionnee = Formation.objects.get(code=formation_code, actif=True)
        except Formation.DoesNotExist:
            formation_selectionnee = None
            messages.error(request, "Formation sélectionnée introuvable.")

    if formation_selectionnee:
        type_docs = _get_document_type_for_code(formation_selectionnee.code)
        documents_requis = list(
            DocumentRequis.objects.filter(type_formation=type_docs, actif=True).order_by('ordre')
        )
        dossiers_queryset = (
            DossierCandidature.objects.filter(formation=formation_selectionnee)
            .select_related('candidat')
            .prefetch_related('documents', 'inscriptions')
            .order_by('-date_depot')
        )
        if search_query:
            dossiers_queryset = dossiers_queryset.filter(
                Q(candidat__username__icontains=search_query)
                | Q(candidat__first_name__icontains=search_query)
                | Q(candidat__last_name__icontains=search_query)
                | Q(reference__icontains=search_query)
            )
        if start_date:
            dossiers_queryset = dossiers_queryset.filter(date_depot__gte=start_date)
        if end_date:
            dossiers_queryset = dossiers_queryset.filter(date_depot__lte=end_date)

        stats = dossiers_queryset.aggregate(
            total=Count('id'),
            soumis=Count('id', filter=Q(statut='soumis')),
            incomplets=Count('id', filter=Q(statut='incomplet')),
            verifies=Count('id', filter=Q(statut='verifie')),
            rejetes=Count('id', filter=Q(statut='rejete')),
        )

        for dossier in dossiers_queryset:
            docs_manquants = dossier.get_documents_manquants()
            decision = getattr(dossier, 'decision_admission', None)
            inscription = dossier.inscriptions.first()

            dossiers_data.append(
                {
                    'dossier': dossier,
                    'complet': dossier.verifier_completude(),
                    'documents_manquants': docs_manquants,
                    'decision': decision,
                    'inscription': inscription,
                }
            )

        if export_format == 'csv' and dossiers_queryset.exists():
            return _export_dossiers_csv(dossiers_queryset, formation_selectionnee)

    context = {
        'formations': formations,
        'formation_selectionnee': formation_selectionnee,
        'formation_code': formation_code,
        'dossiers_data': dossiers_data,
        'stats': stats,
        'documents_requis': documents_requis,
        'search_query': search_query,
        'start_date': start_date_param,
        'end_date': end_date_param,
    }
    return render(request, 'admissions/suivi_dossiers.html', context)


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
    """Vue pour suivre la demande après admission (uniquement 1ère année pour DESMFMC)."""
    dossier = get_object_or_404(
        DossierCandidature,
        id=dossier_id,
        candidat=request.user
    )
    
    # Pour DESMFMC, l'inscription n'est valable que pour la 1ère année
    if dossier.est_desmfmc():
        # Vérifier si l'étudiant a déjà une demande finalisée et dans quelle année
        inscription_existante = Inscription.objects.filter(
            dossier=dossier
        ).first()
        
        if inscription_existante and inscription_existante.est_complete:
            # Vérifier l'année actuelle de l'étudiant
            resultat_actuel = ResultatAnneeDES.objects.filter(
                etudiant=request.user,
                formation=dossier.formation
            ).order_by('-annee').first()
            
            if resultat_actuel and resultat_actuel.annee > 1:
                messages.info(
                    request,
                    f"Votre demande pour le DESMFMC est déjà validée. Pour l'année {resultat_actuel.annee}, "
                    f"veuillez utiliser le système de paiements annuels."
                )
                return redirect('admissions:paiements_annee_des')
    
    # Vérifier qu'il y a une décision d'admission positive
    try:
        decision = dossier.decision_admission
        if decision.decision != 'admis':
            messages.warning(
                request,
                "Vous devez être admis pour suivre cette demande."
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
            # Formulaire de suivi standard
            form_inscription = InscriptionForm(request.POST, instance=inscription_obj)
            form_paiement = InscriptionPaiementForm(instance=inscription_obj)
            
            if form_inscription.is_valid():
                form_inscription.save()
                messages.success(request, "Demande mise à jour.")
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
        type_formation = _get_document_type_for_code(formation.code)
        
        documents = DocumentRequis.objects.filter(
            type_formation=type_formation,
            actif=True
        ).order_by('ordre').values('id', 'nom', 'description', 'obligatoire', 'ordre')
        
        return JsonResponse({
            'documents': list(documents)
        })
    except Formation.DoesNotExist:
        return JsonResponse({'error': 'Formation non trouvée'}, status=404)


@login_required
def paiements_annee_des(request):
    """Vue pour lister les paiements annuels DESMFMC d'un étudiant."""
    if not request.user.est_etudiant():
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    # Récupérer la formation DESMFMC
    try:
        formation_desmfmc = Formation.objects.get(code='DESMFMC', actif=True)
    except Formation.DoesNotExist:
        messages.error(request, "La formation DESMFMC n'est pas configurée.")
        return redirect('dashboard_etudiant')
    
    # Récupérer les paiements annuels
    paiements = PaiementAnneeDES.objects.filter(
        etudiant=request.user,
        formation=formation_desmfmc
    ).order_by('-annee', '-date_creation')
    
    # Récupérer les résultats annuels pour vérifier les conditions
    resultats = ResultatAnneeDES.objects.filter(
        etudiant=request.user,
        formation=formation_desmfmc
    ).order_by('annee')
    
    resultats_dict = {r.annee: r for r in resultats}
    paiements_dict = {p.annee: p for p in paiements}
    
    # Préparer les données pour les années disponibles (2, 3, 4)
    annees_disponibles = []
    for annee_num in [2, 3, 4]:
        annee_prec = annee_num - 1
        resultat_prec = resultats_dict.get(annee_prec)
        paiement = paiements_dict.get(annee_num)
        
        annees_disponibles.append({
            'annee': annee_num,
            'annee_precedente': annee_prec,
            'resultat_precedent': resultat_prec,
            'resultat_valide': resultat_prec and resultat_prec.decision == 'admis',
            'paiement': paiement,
            'peut_payer': resultat_prec and resultat_prec.decision == 'admis',
        })
    
    context = {
        'paiements': paiements,
        'paiements_dict': paiements_dict,
        'resultats': resultats,
        'resultats_dict': resultats_dict,
        'annees_disponibles': annees_disponibles,
        'formation': formation_desmfmc,
    }
    return render(request, 'admissions/paiements_annee_des.html', context)


@login_required
def creer_paiement_annee_des(request, annee):
    """Vue pour créer/déposer un paiement annuel pour une année donnée (2, 3 ou 4)."""
    if not request.user.est_etudiant():
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    if annee not in [2, 3, 4]:
        messages.error(request, "Les paiements annuels concernent uniquement les années 2, 3 et 4.")
        return redirect('admissions:paiements_annee_des')
    
    # Récupérer la formation DESMFMC
    try:
        formation_desmfmc = Formation.objects.get(code='DESMFMC', actif=True)
    except Formation.DoesNotExist:
        messages.error(request, "La formation DESMFMC n'est pas configurée.")
        return redirect('dashboard_etudiant')
    
    # Vérifier que l'année précédente est validée
    annee_precedente = annee - 1
    resultat_precedent = ResultatAnneeDES.objects.filter(
        etudiant=request.user,
        formation=formation_desmfmc,
        annee=annee_precedente
    ).first()
    
    if not resultat_precedent:
        messages.error(
            request,
            f"Vous devez d'abord valider l'année {annee_precedente} avant de pouvoir payer pour l'année {annee}."
        )
        return redirect('admissions:paiements_annee_des')
    
    if resultat_precedent.decision != 'admis':
        messages.error(
            request,
            f"L'année {annee_precedente} n'est pas encore validée. Vous devez être admis pour accéder à l'année {annee}."
        )
        return redirect('admissions:paiements_annee_des')
    
    # Vérifier si un paiement existe déjà
    paiement_existant = PaiementAnneeDES.objects.filter(
        etudiant=request.user,
        formation=formation_desmfmc,
        annee=annee
    ).first()
    
    if request.method == 'POST':
        if paiement_existant and paiement_existant.statut == 'paiement_valide':
            messages.warning(request, "Le paiement pour cette année est déjà validé.")
            return redirect('admissions:paiements_annee_des')
        
        mode_paiement = request.POST.get('mode_paiement')
        reference_paiement = request.POST.get('reference_paiement', '')
        preuve_paiement = request.FILES.get('preuve_paiement')
        montant = request.POST.get('montant')
        
        if not mode_paiement or not montant:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
        else:
            with transaction.atomic():
                if paiement_existant:
                    # Mettre à jour le paiement existant
                    paiement_existant.mode_paiement = mode_paiement
                    paiement_existant.reference_paiement = reference_paiement
                    paiement_existant.montant = montant
                    if preuve_paiement:
                        paiement_existant.preuve_paiement = preuve_paiement
                    paiement_existant.statut = 'paiement_effectue'
                    paiement_existant.date_paiement = timezone.now()
                    paiement_existant.resultat_annee = resultat_precedent
                    paiement_existant.save()
                    messages.success(request, "Informations de paiement mises à jour. En attente de validation.")
                else:
                    # Créer un nouveau paiement
                    paiement = PaiementAnneeDES.objects.create(
                        etudiant=request.user,
                        formation=formation_desmfmc,
                        annee=annee,
                        montant=montant,
                        mode_paiement=mode_paiement,
                        reference_paiement=reference_paiement,
                        preuve_paiement=preuve_paiement,
                        statut='paiement_effectue',
                        date_paiement=timezone.now(),
                        resultat_annee=resultat_precedent,
                    )
                    messages.success(request, "Paiement déposé avec succès. En attente de validation.")
                
                return redirect('admissions:paiements_annee_des')
    
    # Récupérer le résultat de l'année 4 si on est en année 4
    resultat_annee_4 = None
    if annee == 4:
        resultat_annee_4 = ResultatAnneeDES.objects.filter(
            etudiant=request.user,
            formation=formation_desmfmc,
            annee=4
        ).first()
    
    context = {
        'annee': annee,
        'annee_precedente': annee_precedente,
        'resultat_precedent': resultat_precedent,
        'resultat_annee_4': resultat_annee_4,
        'paiement_existant': paiement_existant,
        'formation': formation_desmfmc,
    }
    return render(request, 'admissions/creer_paiement_annee_des.html', context)


@login_required
def validation_passage_annee(request, annee):
    """Vue pour afficher le statut de validation du passage à l'année suivante."""
    if not request.user.est_etudiant():
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    if annee not in [2, 3, 4]:
        messages.error(request, "La validation concerne uniquement les années 2, 3 et 4.")
        return redirect('admissions:paiements_annee_des')
    
    # Récupérer la formation DESMFMC
    try:
        formation_desmfmc = Formation.objects.get(code='DESMFMC', actif=True)
    except Formation.DoesNotExist:
        messages.error(request, "La formation DESMFMC n'est pas configurée.")
        return redirect('dashboard_etudiant')
    
    # Récupérer le résultat de l'année précédente
    annee_precedente = annee - 1
    resultat_precedent = ResultatAnneeDES.objects.filter(
        etudiant=request.user,
        formation=formation_desmfmc,
        annee=annee_precedente
    ).first()
    
    # Récupérer le paiement pour l'année
    paiement = PaiementAnneeDES.objects.filter(
        etudiant=request.user,
        formation=formation_desmfmc,
        annee=annee
    ).first()
    
    # Vérifier si l'accès est possible
    peut_acceder = False
    conditions_remplies = []
    conditions_manquantes = []
    
    if resultat_precedent and resultat_precedent.decision == 'admis':
        conditions_remplies.append(f"✅ Année {annee_precedente} validée (admis)")
    else:
        conditions_manquantes.append(f"❌ Année {annee_precedente} non validée")
    
    if paiement and paiement.statut == 'paiement_valide':
        conditions_remplies.append(f"✅ Paiement des frais d'inscription annuels validé")
    else:
        conditions_manquantes.append(f"❌ Paiement des frais d'inscription annuels non validé")
    
    if paiement and paiement.peut_valider_passage():
        peut_acceder = True
    
    # Pour l'année 4, vérifier aussi le mémoire
    resultat_annee_4 = None
    if annee == 4:
        resultat_annee_4 = ResultatAnneeDES.objects.filter(
            etudiant=request.user,
            formation=formation_desmfmc,
            annee=4
        ).first()
        if resultat_annee_4 and resultat_annee_4.memoire_valide:
            conditions_remplies.append("✅ Mémoire de fin de formation validé")
        else:
            conditions_manquantes.append("❌ Mémoire de fin de formation non validé")
    
    context = {
        'annee': annee,
        'annee_precedente': annee_precedente,
        'resultat_precedent': resultat_precedent,
        'resultat_annee_4': resultat_annee_4,
        'paiement': paiement,
        'peut_acceder': peut_acceder,
        'conditions_remplies': conditions_remplies,
        'conditions_manquantes': conditions_manquantes,
        'formation': formation_desmfmc,
    }
    return render(request, 'admissions/validation_passage_annee.html', context)


def _export_dossiers_csv(dossiers_queryset, formation):
    """Exporte la liste des dossiers en CSV."""
    response = HttpResponse(content_type='text/csv')
    filename = f"dossiers_{formation.code.lower()}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Référence', 'Candidat', 'Email', 'Date dépôt', 'Statut', 'Complet', 'Décision', 'Suivi administratif (DES)'])

    for dossier in dossiers_queryset:
        decision = getattr(dossier, 'decision_admission', None)
        inscription = dossier.inscriptions.first()
        writer.writerow([
            dossier.reference,
            dossier.candidat.get_full_name() or dossier.candidat.username,
            dossier.candidat.email,
            dossier.date_depot.strftime('%Y-%m-%d'),
            dossier.get_statut_display(),
            'Oui' if dossier.verifier_completude() else 'Non',
            decision.get_decision_display() if decision else '',
            inscription.get_statut_display() if inscription else '',
        ])

    return response
