# core/views_carnet_stage.py
"""
Vues pour le carnet de stage du DESMFMC
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator

from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_carnet_stage import (
    CarnetStage, EvaluationStage, EvaluationCompetence,
    TableauEvaluationClasse, EvaluationCompetenceTableau
)
from apps.utilisateurs.forms_carnet_stage import (
    CarnetStageForm, EvaluationStageForm, EvaluationCompetenceForm,
    TableauEvaluationClasseForm, EvaluationCompetenceTableauForm
)
from apps.utilisateurs.models_programme_desmfmc import JalonProgramme, StageRotationDES
from apps.utilisateurs.models_formation import Competence, Classe


@login_required
def mon_carnet_stage(request):
    """Vue pour afficher le carnet de stage de l'étudiant connecté"""
    from apps.utilisateurs.models_carnet_stage import ProclamationResultats
    
    if request.user.type_utilisateur != 'etudiant':
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    try:
        carnet = CarnetStage.objects.get(etudiant=request.user, actif=True)
    except CarnetStage.DoesNotExist:
        messages.info(request, "Vous n'avez pas encore de carnet de stage. Contactez la coordination pour en créer un.")
        return redirect('dashboard_etudiant')
    
    # Récupérer la classe de l'étudiant
    classe_etudiant = request.user.get_classe_obj()
    
    # Vérifier si les résultats sont proclamés pour cette classe
    resultats_proclames = False
    if classe_etudiant:
        proclamation = ProclamationResultats.objects.filter(
            classe=classe_etudiant,
            annee_scolaire=carnet.annee_scolaire,
            actif=True
        ).first()
        resultats_proclames = proclamation is not None
    
    # Filtrer les tableaux d'évaluation selon la classe de l'étudiant
    if classe_etudiant:
        tableaux = carnet.tableaux_evaluation.filter(
            classe=classe_etudiant
        ).order_by('annee', 'classe__nom')
    else:
        tableaux = carnet.tableaux_evaluation.all().order_by('annee', 'classe__nom')
    
    # Récupérer toutes les évaluations de stages par année
    stages_annee_1 = carnet.get_stages_annee_1()
    stages_annee_2 = carnet.get_stages_annee_2()
    stages_annee_3 = carnet.get_stages_annee_3()
    stages_annee_4 = carnet.get_stages_annee_4()
    
    # Récupérer les stages ruraux et urbains depuis StageRotationDES
    stages_rotation_annee_2 = StageRotationDES.objects.filter(
        etudiant=carnet.etudiant,
        annee=2
    ).select_related('centre').order_by('periode')
    
    stages_rotation_annee_3 = StageRotationDES.objects.filter(
        etudiant=carnet.etudiant,
        annee=3
    ).select_related('centre').order_by('periode')
    
    # Séparer les stages urbains et ruraux
    stages_urbains_annee_2 = stages_rotation_annee_2.filter(centre__type_centre='urbain')
    stages_ruraux_annee_2 = stages_rotation_annee_2.filter(centre__type_centre='rural')
    stages_urbains_annee_3 = stages_rotation_annee_3.filter(centre__type_centre='urbain')
    stages_ruraux_annee_3 = stages_rotation_annee_3.filter(centre__type_centre='rural')
    
    # Créer un dictionnaire pour mapper les stages rotation aux évaluations existantes
    evaluations_stage_rotation_map = {}
    for eval_stage in carnet.evaluations_stages.filter(stage_rotation__isnull=False).select_related('stage_rotation'):
        if eval_stage.stage_rotation:
            evaluations_stage_rotation_map[eval_stage.stage_rotation.id] = eval_stage.id
    
    # Statistiques
    total_stages = carnet.evaluations_stages.count()
    stages_valides = carnet.evaluations_stages.filter(valide=True).count()
    
    # Compter les stages rotation
    total_stages_rotation = stages_rotation_annee_2.count() + stages_rotation_annee_3.count()
    
    context = {
        'carnet': carnet,
        'classe_etudiant': classe_etudiant,
        'resultats_proclames': resultats_proclames,
        'stages_annee_1': stages_annee_1,
        'stages_annee_2': stages_annee_2,
        'stages_annee_3': stages_annee_3,
        'stages_annee_4': stages_annee_4,
        'stages_urbains_annee_2': stages_urbains_annee_2,
        'stages_ruraux_annee_2': stages_ruraux_annee_2,
        'stages_urbains_annee_3': stages_urbains_annee_3,
        'stages_ruraux_annee_3': stages_ruraux_annee_3,
        'evaluations_stage_rotation_map': evaluations_stage_rotation_map,
        'tableaux': tableaux,
        'total_stages': total_stages,
        'stages_valides': stages_valides,
        'total_stages_rotation': total_stages_rotation,
    }
    
    return render(request, 'carnet_stage/mon_carnet.html', context)


@login_required
def detail_evaluation_stage(request, evaluation_id):
    """Vue pour afficher le détail d'une évaluation de stage"""
    from apps.utilisateurs.models_carnet_stage import ProclamationResultats
    
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    # Vérifier les permissions
    if request.user.type_utilisateur == 'etudiant':
        if evaluation.carnet.etudiant != request.user:
            messages.error(request, "Vous n'avez pas accès à cette évaluation.")
            return redirect('mon_carnet_stage')
        
        # Vérifier si les résultats sont proclamés pour cette classe
        classe_etudiant = request.user.get_classe_obj()
        resultats_proclames = False
        if classe_etudiant:
            proclamation = ProclamationResultats.objects.filter(
                classe=classe_etudiant,
                annee_scolaire=evaluation.carnet.annee_scolaire,
                actif=True
            ).first()
            resultats_proclames = proclamation is not None
        
        if not resultats_proclames:
            messages.info(request, "Les résultats n'ont pas encore été proclamés. Vous pouvez consulter les grilles d'évaluation pour connaître les compétences à acquérir.")
            return redirect('mon_carnet_stage')
    
    # Récupérer les évaluations de compétences
    evaluations_competences = evaluation.evaluations_competences.all().order_by('competence__libelle')
    
    context = {
        'evaluation': evaluation,
        'evaluations_competences': evaluations_competences,
    }
    
    return render(request, 'carnet_stage/detail_evaluation_stage.html', context)


@login_required
def ajouter_evaluation_stage(request, carnet_id):
    """Vue pour ajouter une évaluation de stage"""
    from apps.utilisateurs.models_programme_desmfmc import StageRotationDES
    
    carnet = get_object_or_404(CarnetStage, pk=carnet_id)
    
    # Vérifier les permissions
    if request.user.type_utilisateur == 'etudiant' and carnet.etudiant != request.user:
        messages.error(request, "Vous n'avez pas accès à ce carnet.")
        return redirect('mon_carnet_stage')
    
    if request.method == 'POST':
        form = EvaluationStageForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.carnet = carnet
            evaluation.save()
            messages.success(request, "Évaluation de stage ajoutée avec succès.")
            return redirect('detail_evaluation_stage', evaluation_id=evaluation.id)
    else:
        form = EvaluationStageForm()
        
        # Vérifier si un stage_rotation est passé en paramètre (pour les stages ruraux/urbains)
        stage_rotation_id = request.GET.get('stage_rotation')
        if stage_rotation_id:
            try:
                stage_rotation = StageRotationDES.objects.select_related('centre').get(
                    pk=stage_rotation_id,
                    etudiant=carnet.etudiant
                )
                # Pré-remplir le formulaire avec les informations du stage rotation
                form.fields['stage_rotation'].initial = stage_rotation
                form.fields['annee'].initial = stage_rotation.annee
                
                # Déterminer le type de stage selon le type de centre
                if stage_rotation.centre.type_centre == 'urbain':
                    form.fields['type_stage'].initial = 'cscom_urbain'
                elif stage_rotation.centre.type_centre == 'rural':
                    form.fields['type_stage'].initial = 'cscom_rural'
                
                # Pré-remplir le lieu du stage
                form.fields['lieu_stage'].initial = stage_rotation.centre.nom
                
                # Pré-remplir les dates si disponibles
                if stage_rotation.date_debut:
                    form.fields['date_debut'].initial = stage_rotation.date_debut
                if stage_rotation.date_fin:
                    form.fields['date_fin'].initial = stage_rotation.date_fin
                
            except StageRotationDES.DoesNotExist:
                messages.warning(request, "Le stage rotation spécifié n'existe pas ou ne vous appartient pas.")
        else:
            # Pré-remplir l'année si possible (pour les autres types de stages)
            if carnet.evaluations_stages.exists():
                derniere_annee = carnet.evaluations_stages.order_by('-annee').first().annee
                form.fields['annee'].initial = derniere_annee
    
    context = {
        'form': form,
        'carnet': carnet,
    }
    
    return render(request, 'carnet_stage/ajouter_evaluation_stage.html', context)


@login_required
def modifier_evaluation_stage(request, evaluation_id):
    """Vue pour modifier une évaluation de stage"""
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    # Vérifier les permissions
    if request.user.type_utilisateur == 'etudiant' and evaluation.carnet.etudiant != request.user:
        messages.error(request, "Vous n'avez pas accès à cette évaluation.")
        return redirect('mon_carnet_stage')
    
    if request.method == 'POST':
        form = EvaluationStageForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, "Évaluation de stage modifiée avec succès.")
            return redirect('detail_evaluation_stage', evaluation_id=evaluation.id)
    else:
        form = EvaluationStageForm(instance=evaluation)
    
    context = {
        'form': form,
        'evaluation': evaluation,
    }
    
    return render(request, 'carnet_stage/modifier_evaluation_stage.html', context)


@login_required
def ajouter_evaluation_competence(request, evaluation_id):
    """Vue pour ajouter une évaluation de compétence à un stage"""
    evaluation = get_object_or_404(EvaluationStage, pk=evaluation_id)
    
    # Vérifier les permissions
    if request.user.type_utilisateur == 'etudiant' and evaluation.carnet.etudiant != request.user:
        messages.error(request, "Vous n'avez pas accès à cette évaluation.")
        return redirect('mon_carnet_stage')
    
    if request.method == 'POST':
        form = EvaluationCompetenceForm(request.POST)
        if form.is_valid():
            eval_competence = form.save(commit=False)
            eval_competence.evaluation_stage = evaluation
            eval_competence.save()
            messages.success(request, "Évaluation de compétence ajoutée avec succès.")
            return redirect('detail_evaluation_stage', evaluation_id=evaluation.id)
    else:
        form = EvaluationCompetenceForm()
        # Pré-remplir le jalon si possible
        if evaluation.annee:
            jalon = JalonProgramme.objects.filter(annee=evaluation.annee).first()
            if jalon:
                form.fields['jalon'].initial = jalon
    
    # Récupérer les compétences déjà évaluées
    competences_evaluees = evaluation.evaluations_competences.values_list('competence_id', flat=True)
    
    context = {
        'form': form,
        'evaluation': evaluation,
        'competences_evaluees': competences_evaluees,
    }
    
    return render(request, 'carnet_stage/ajouter_evaluation_competence.html', context)


@login_required
def tableau_evaluation_classe(request, tableau_id):
    """Vue pour afficher et modifier un tableau d'évaluation par classe"""
    tableau = get_object_or_404(TableauEvaluationClasse, pk=tableau_id)
    
    # Vérifier les permissions
    if request.user.type_utilisateur == 'etudiant' and tableau.carnet.etudiant != request.user:
        messages.error(request, "Vous n'avez pas accès à ce tableau.")
        return redirect('mon_carnet_stage')
    
    # Récupérer les évaluations de compétences dans ce tableau
    evaluations = tableau.evaluations_competences_tableau.all().order_by('competence__libelle')
    
    context = {
        'tableau': tableau,
        'evaluations': evaluations,
    }
    
    return render(request, 'carnet_stage/tableau_evaluation_classe.html', context)


@login_required
def ajouter_tableau_evaluation(request, carnet_id):
    """Vue pour ajouter un tableau d'évaluation par classe"""
    carnet = get_object_or_404(CarnetStage, pk=carnet_id)
    
    # Vérifier les permissions
    if request.user.type_utilisateur == 'etudiant' and carnet.etudiant != request.user:
        messages.error(request, "Vous n'avez pas accès à ce carnet.")
        return redirect('mon_carnet_stage')
    
    if request.method == 'POST':
        form = TableauEvaluationClasseForm(request.POST)
        if form.is_valid():
            tableau = form.save(commit=False)
            tableau.carnet = carnet
            tableau.save()
            form.save_m2m()  # Sauvegarder les compétences
            
            # Créer les évaluations de compétences pour chaque compétence
            for competence in form.cleaned_data['competences']:
                EvaluationCompetenceTableau.objects.get_or_create(
                    tableau=tableau,
                    competence=competence
                )
            
            messages.success(request, "Tableau d'évaluation créé avec succès.")
            return redirect('tableau_evaluation_classe', tableau_id=tableau.id)
    else:
        form = TableauEvaluationClasseForm()
    
    context = {
        'form': form,
        'carnet': carnet,
    }
    
    return render(request, 'carnet_stage/ajouter_tableau_evaluation.html', context)


@login_required
def imprimer_tableau_evaluation(request, tableau_id):
    """Vue pour imprimer un tableau d'évaluation en PDF"""
    from core.utils_pdf import generate_pdf_response
    
    tableau = get_object_or_404(TableauEvaluationClasse, pk=tableau_id)
    
    # Vérifier les permissions
    if request.user.type_utilisateur == 'etudiant' and tableau.carnet.etudiant != request.user:
        messages.error(request, "Vous n'avez pas accès à ce tableau.")
        return redirect('mon_carnet_stage')
    
    # Récupérer les évaluations de compétences dans ce tableau
    evaluations = tableau.evaluations_competences_tableau.all().order_by('competence__libelle')
    
    context = {
        'tableau': tableau,
        'evaluations': evaluations,
    }
    
    html_content = render_to_string('carnet_stage/pdf_tableau_evaluation.html', context)
    filename = f"tableau_evaluation_{tableau.classe.nom}_{tableau.annee}.pdf"
    
    return generate_pdf_response(html_content, filename)

