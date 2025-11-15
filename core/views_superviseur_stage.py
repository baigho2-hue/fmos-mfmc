# core/views_superviseur_stage.py
"""
Vues pour les superviseurs cliniques et CEC pour remplir les évaluations de stage
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_carnet_stage import (
    CarnetStage, EvaluationStage, EvaluationCompetence,
    TableauEvaluationClasse, ProclamationResultats
)
from apps.utilisateurs.models_formation import Classe
from apps.utilisateurs.models_programme_desmfmc import CSComUCentre, StageRotationDES
from apps.utilisateurs.forms_carnet_stage import (
    EvaluationStageForm, EvaluationCompetenceForm
)
from core.views_2fa import deux_facteurs_required


def superviseur_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est connecté et est un superviseur/CEC"""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        # Vérifier que l'utilisateur est authentifié
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour accéder à cette page.")
            return redirect('login')
        
        # Vérifier que l'utilisateur est un enseignant ET superviseur/CEC
        if not request.user.est_enseignant():
            messages.error(request, "Accès réservé aux enseignants.")
            return redirect('accueil')
        
        if not request.user.est_superviseur_cec():
            messages.error(request, "Accès réservé aux superviseurs cliniques et CEC. Veuillez contacter l'administration pour obtenir ce statut.")
            return redirect('accueil')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@superviseur_required
@deux_facteurs_required
def liste_evaluations_superviseur(request):
    """Liste des évaluations de stage que le superviseur peut remplir"""
    # Récupérer toutes les classes du DESMFMC
    classes_desmfmc = Classe.objects.filter(
        formation__nom__icontains='DESMFMC',
        actif=True
    ).order_by('nom')
    
    # Récupérer tous les centres CSCom-U actifs
    centres_cscom = CSComUCentre.objects.filter(actif=True).order_by('type_centre', 'nom')
    
    # Récupérer toutes les répartitions de stages
    repartitions_stages = StageRotationDES.objects.select_related(
        'etudiant', 'centre'
    ).order_by('annee', 'periode', 'centre__nom')
    
    # Déterminer la période actuelle selon le calendrier de l'année scolaire
    periode_actuelle = StageRotationDES.get_periode_actuelle()
    annee_scolaire_actuelle = StageRotationDES.get_annee_scolaire_actuelle()
    
    # Filtres
    classe_id = request.GET.get('classe')
    centre_id = request.GET.get('centre')
    repartition_id = request.GET.get('repartition')
    
    classe_selected = None
    centre_selected = None
    repartition_selected = None
    evaluations = EvaluationStage.objects.none()
    
    # Vérifier si le superviseur a un centre de supervision assigné
    centre_superviseur = request.user.centre_supervision
    filtre_automatique_centre = False
    
    # Construire la requête de base
    evaluations_query = EvaluationStage.objects.select_related(
        'carnet', 'carnet__etudiant', 'evalue_par_superviseur',
        'stage_rotation', 'stage_rotation__centre'
    )
    
    # Filtrer par répartition de stage (priorité la plus élevée)
    if repartition_id:
        try:
            repartition_selected = StageRotationDES.objects.get(pk=repartition_id)
            # Récupérer les évaluations liées à cette répartition
            evaluations_query = evaluations_query.filter(stage_rotation=repartition_selected)
        except StageRotationDES.DoesNotExist:
            messages.error(request, "Répartition de stage introuvable.")
    
    # Filtrer par centre/lieu
    elif centre_id:
        try:
            centre_selected = CSComUCentre.objects.get(pk=centre_id, actif=True)
            # Récupérer les répartitions pour ce centre
            repartitions_centre = StageRotationDES.objects.filter(centre=centre_selected)
            # Récupérer les évaluations liées à ces répartitions
            evaluations_query = evaluations_query.filter(stage_rotation__in=repartitions_centre)
        except CSComUCentre.DoesNotExist:
            messages.error(request, "Centre introuvable.")
    
    # Filtrer par classe
    elif classe_id:
        try:
            classe_selected = Classe.objects.get(pk=classe_id, actif=True)
            # Récupérer les carnets de stage des étudiants de cette classe
            etudiants_classe = Utilisateur.objects.filter(
                type_utilisateur='etudiant'
            ).filter(
                Q(classe__icontains=classe_selected.nom) | 
                Q(classe__icontains=classe_selected.nom.replace('DESMFMC', '').strip())
            )
            carnets = CarnetStage.objects.filter(
                etudiant__in=etudiants_classe,
                actif=True
            )
            evaluations_query = evaluations_query.filter(carnet__in=carnets)
        except Classe.DoesNotExist:
            messages.error(request, "Classe introuvable.")
    
    # Si aucun filtre n'est sélectionné, filtrer automatiquement par le centre du superviseur
    # et optionnellement par la période actuelle
    elif centre_superviseur:
        centre_selected = centre_superviseur
        filtre_automatique_centre = True
        # Récupérer les répartitions pour ce centre
        repartitions_centre = StageRotationDES.objects.filter(centre=centre_superviseur)
        
        # Filtrer également par la période actuelle si elle est définie
        if periode_actuelle:
            repartitions_centre = repartitions_centre.filter(periode=periode_actuelle)
            messages.info(request, f"Affichage automatique des évaluations pour votre centre de supervision ({centre_superviseur.nom}) - Période {periode_actuelle}")
        else:
            messages.info(request, f"Affichage automatique des évaluations pour votre centre de supervision : {centre_superviseur.nom}")
        
        # Récupérer les évaluations liées à ces répartitions
        evaluations_query = evaluations_query.filter(stage_rotation__in=repartitions_centre)
    
    # Si aucun filtre n'est sélectionné et pas de centre assigné, afficher toutes les évaluations
    else:
        evaluations_query = EvaluationStage.objects.select_related(
            'carnet', 'carnet__etudiant', 'evalue_par_superviseur',
            'stage_rotation', 'stage_rotation__centre'
        ).all()
    
    # Trier les résultats
    evaluations = evaluations_query.order_by(
        '-date_creation', 'carnet__etudiant__username'
    )
    
    # Pagination
    paginator = Paginator(evaluations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'classes_desmfmc': classes_desmfmc,
        'centres_cscom': centres_cscom,
        'repartitions_stages': repartitions_stages,
        'classe_selected': classe_selected,
        'centre_selected': centre_selected,
        'repartition_selected': repartition_selected,
        'filtre_automatique_centre': filtre_automatique_centre,
        'centre_superviseur': centre_superviseur,
        'periode_actuelle': periode_actuelle,
        'annee_scolaire_actuelle': annee_scolaire_actuelle,
        'evaluations': page_obj,
    }
    
    return render(request, 'superviseur_stage/liste_evaluations.html', context)


@superviseur_required
@deux_facteurs_required
def remplir_evaluation_stage(request, evaluation_id):
    """Vue pour remplir une évaluation de stage (superviseur/CEC)"""
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    if request.method == 'POST':
        form = EvaluationStageForm(request.POST, instance=evaluation)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.evalue_par_superviseur = request.user
            from django.utils import timezone
            evaluation.date_evaluation_superviseur = timezone.now()
            evaluation.save()
            messages.success(request, "Évaluation remplie avec succès.")
            return redirect('liste_evaluations_superviseur')
    else:
        form = EvaluationStageForm(instance=evaluation)
    
    # Récupérer les compétences à évaluer pour cette classe et année
    classe_etudiant = evaluation.carnet.etudiant.get_classe_obj()
    competences = []
    if classe_etudiant:
        # Récupérer les compétences du tableau d'évaluation pour cette classe et année
        tableau = TableauEvaluationClasse.objects.filter(
            carnet=evaluation.carnet,
            classe=classe_etudiant,
            annee=evaluation.annee
        ).first()
        if tableau:
            competences = tableau.competences.all()
    
    # Récupérer les évaluations de compétences existantes
    evaluations_competences = evaluation.evaluations_competences.all()
    
    context = {
        'evaluation': evaluation,
        'form': form,
        'competences': competences,
        'evaluations_competences': evaluations_competences,
    }
    
    return render(request, 'superviseur_stage/remplir_evaluation.html', context)


@superviseur_required
@deux_facteurs_required
def ajouter_evaluation_competence_superviseur(request, evaluation_id):
    """Ajouter une évaluation de compétence (superviseur)"""
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    if request.method == 'POST':
        form = EvaluationCompetenceForm(request.POST)
        if form.is_valid():
            eval_comp = form.save(commit=False)
            eval_comp.evaluation_stage = evaluation
            eval_comp.evalue_par_maitre = True
            from django.utils import timezone
            eval_comp.date_evaluation = timezone.now().date()
            eval_comp.save()
            messages.success(request, "Évaluation de compétence ajoutée avec succès.")
            return redirect('remplir_evaluation_stage', evaluation_id=evaluation.id)
    else:
        form = EvaluationCompetenceForm()
        # Pré-remplir avec les compétences du tableau d'évaluation
        classe_etudiant = evaluation.carnet.etudiant.get_classe_obj()
        if classe_etudiant:
            tableau = TableauEvaluationClasse.objects.filter(
                carnet=evaluation.carnet,
                classe=classe_etudiant,
                annee=evaluation.annee
            ).first()
            if tableau:
                # Filtrer les compétences déjà évaluées
                competences_evaluees = evaluation.evaluations_competences.values_list('competence_id', flat=True)
                form.fields['competence'].queryset = tableau.competences.exclude(id__in=competences_evaluees)
    
    context = {
        'evaluation': evaluation,
        'form': form,
    }
    
    return render(request, 'superviseur_stage/ajouter_evaluation_competence.html', context)

