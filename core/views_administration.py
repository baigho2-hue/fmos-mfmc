# core/views_administration.py
"""
Vues pour le menu Administration - Accessible uniquement aux membres de la coordination DESMFMC
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, Avg, Max, Min
from datetime import timedelta, datetime
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Formation, Classe, Cours, Planification, ProgressionEtudiant, Lecon, Competence
from apps.utilisateurs.models_programme_desmfmc import CSComUCentre, StageRotationDES, JalonProgramme
from apps.utilisateurs.models_documents import LettreInformation, ModelePedagogique
from apps.utilisateurs.utils import attribuer_stages_cscom_aleatoire
from apps.evaluations.models import Evaluation, ResultatEvaluation, EvaluationEnseignant, TypeEvaluation
from apps.utilisateurs.forms import InscriptionEnseignantForm
from decimal import Decimal
from core.utils_pdf import generate_pdf_from_template, send_pdf_by_email
from django.http import JsonResponse, HttpResponse, FileResponse
from django.views.decorators.http import require_http_methods


def coordination_required(view_func):
    """Décorateur pour vérifier que l'utilisateur est membre de la coordination"""
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if not request.user.est_membre_coordination():
            messages.error(request, "Accès réservé aux membres de la coordination DESMFMC.")
            return redirect('accueil')
        return view_func(request, *args, **kwargs)
    return wrapper


@coordination_required
def dashboard_administration(request):
    """Tableau de bord de l'administration"""
    # Statistiques générales
    total_etudiants = Utilisateur.objects.filter(type_utilisateur='etudiant', is_active=True).count()
    total_enseignants = Utilisateur.objects.filter(type_utilisateur='enseignant', is_active=True).count()
    total_formations = Formation.objects.filter(actif=True).count()
    total_classes = Classe.objects.filter(actif=True).count()
    
    # Alertes (activités à venir dans les 7 prochains jours)
    date_limite = timezone.now() + timedelta(days=7)
    alertes_agenda = Planification.objects.filter(
        actif=True,
        date_debut__gte=timezone.now(),
        date_debut__lte=date_limite
    ).order_by('date_debut')[:10]
    
    # Inscriptions en attente (à implémenter selon votre modèle d'inscription)
    # inscriptions_en_attente = ...
    
    context = {
        'total_etudiants': total_etudiants,
        'total_enseignants': total_enseignants,
        'total_formations': total_formations,
        'total_classes': total_classes,
        'alertes_agenda': alertes_agenda,
    }
    
    return render(request, 'administration/dashboard.html', context)


@coordination_required
def agenda_administration(request):
    """Agenda administratif - Vue d'ensemble de toutes les activités"""
    # Récupérer les planifications (mois en cours et suivant)
    date_debut = timezone.now()
    date_fin = date_debut + timedelta(days=60)
    
    planifications = Planification.objects.filter(
        actif=True,
        date_debut__gte=date_debut,
        date_debut__lte=date_fin
    ).select_related('classe', 'cours_lie').order_by('date_debut')
    
    # Grouper par date
    planifications_par_date = {}
    for planif in planifications:
        date_key = planif.date_debut.date()
        if date_key not in planifications_par_date:
            planifications_par_date[date_key] = []
        planifications_par_date[date_key].append(planif)
    
    # Alertes (activités à venir dans les 3 prochains jours)
    date_limite_alerte = timezone.now() + timedelta(days=3)
    alertes = Planification.objects.filter(
        actif=True,
        date_debut__gte=timezone.now(),
        date_debut__lte=date_limite_alerte
    ).order_by('date_debut')
    
    context = {
        'planifications': planifications,
        'planifications_par_date': planifications_par_date,
        'alertes': alertes,
    }
    
    return render(request, 'administration/agenda.html', context)


@coordination_required
def notes_classes(request):
    """Notes et évaluations par classe"""
    classes = Classe.objects.filter(actif=True).select_related('formation').order_by('formation__nom', 'nom')
    
    # Statistiques par classe
    stats_classes = []
    for classe in classes:
        etudiants = Utilisateur.objects.filter(
            type_utilisateur='etudiant',
            classe__icontains=classe.nom,
            is_active=True
        )
        
        cours_classe = Cours.objects.filter(classe=classe, actif=True)
        progressions = ProgressionEtudiant.objects.filter(cours__in=cours_classe)
        
        stats_classes.append({
            'classe': classe,
            'nb_etudiants': etudiants.count(),
            'nb_cours': cours_classe.count(),
            'moyenne_progression': progressions.aggregate(Avg('pourcentage_completion'))['pourcentage_completion__avg'] or 0,
        })
    
    context = {
        'classes': classes,
        'stats_classes': stats_classes,
    }
    
    return render(request, 'administration/notes_classes.html', context)


@coordination_required
def detail_notes_classe(request, classe_id):
    """Détail des notes pour une classe spécifique"""
    classe = get_object_or_404(Classe, pk=classe_id)
    
    # Étudiants de la classe
    etudiants = Utilisateur.objects.filter(
        type_utilisateur='etudiant',
        classe__icontains=classe.nom,
        is_active=True
    ).order_by('last_name', 'first_name')
    
    # Cours de la classe
    cours_list = Cours.objects.filter(classe=classe, actif=True).order_by('ordre', 'date_debut')
    
    # Progressions des étudiants
    progressions_par_etudiant = {}
    for etudiant in etudiants:
        progressions = ProgressionEtudiant.objects.filter(
            etudiant=etudiant,
            cours__in=cours_list
        ).select_related('cours')
        
        progressions_par_etudiant[etudiant.id] = {
            'etudiant': etudiant,
            'progressions': {p.cours_id: p for p in progressions},
            'moyenne': progressions.aggregate(Avg('pourcentage_completion'))['pourcentage_completion__avg'] or 0,
        }
    
    context = {
        'classe': classe,
        'etudiants': etudiants,
        'cours_list': cours_list,
        'progressions_par_etudiant': progressions_par_etudiant,
    }
    
    return render(request, 'administration/detail_notes_classe.html', context)


@coordination_required
def alertes_agenda(request):
    """Alertes pour les activités sur l'agenda"""
    # Alertes pour les activités à venir (3 prochains jours)
    date_limite = timezone.now() + timedelta(days=3)
    alertes_prochaines = Planification.objects.filter(
        actif=True,
        date_debut__gte=timezone.now(),
        date_debut__lte=date_limite
    ).select_related('classe', 'cours_lie').order_by('date_debut')
    
    # Alertes pour les activités passées sans suivi
    date_limite_passee = timezone.now() - timedelta(days=7)
    alertes_passees = Planification.objects.filter(
        actif=True,
        date_debut__lte=timezone.now(),
        date_debut__gte=date_limite_passee
    ).select_related('classe', 'cours_lie').order_by('-date_debut')
    
    context = {
        'alertes_prochaines': alertes_prochaines,
        'alertes_passees': alertes_passees,
    }
    
    return render(request, 'administration/alertes_agenda.html', context)


@coordination_required
def resultats_evaluations(request):
    """Résultats des évaluations"""
    # Évaluations avec résultats
    evaluations = Evaluation.objects.filter(actif=True).select_related('cours').order_by('-date_creation')
    
    # Statistiques par évaluation
    stats_evaluations = []
    for evaluation in evaluations:
        resultats = ResultatEvaluation.objects.filter(evaluation=evaluation)
        
        stats_evaluations.append({
            'evaluation': evaluation,
            'nb_participants': resultats.count(),
            'moyenne': resultats.aggregate(Avg('note'))['note__avg'] or 0,
            'note_max': resultats.aggregate(Max('note'))['note__max'] or 0,
            'note_min': resultats.aggregate(Min('note'))['note__min'] or 0,
        })
    
    # Évaluations des enseignants
    evaluations_enseignants = EvaluationEnseignant.objects.all().select_related('enseignant', 'etudiant').order_by('-date_evaluation')
    
    context = {
        'stats_evaluations': stats_evaluations,
        'evaluations_enseignants': evaluations_enseignants[:50],  # Limiter à 50
    }
    
    return render(request, 'administration/resultats_evaluations.html', context)


@coordination_required
def liste_etudiants_par_formation(request):
    """Liste complète de tous les étudiants organisés par formation et classe"""
    # Filtres
    formation_id = request.GET.get('formation')
    classe_id = request.GET.get('classe')
    recherche = request.GET.get('recherche', '').strip()
    
    # Récupérer toutes les formations actives
    formations = Formation.objects.filter(actif=True).order_by('nom')
    
    # Filtrer par formation si spécifié
    if formation_id:
        formations = formations.filter(pk=formation_id)
    
    # Organiser les données par formation
    formations_data = []
    total_etudiants_global = 0
    
    for formation in formations:
        classes = Classe.objects.filter(formation=formation, actif=True).order_by('nom', 'annee')
        
        # Filtrer par classe si spécifié
        if classe_id:
            classes = classes.filter(pk=classe_id)
        
        classes_data = []
        total_etudiants_formation = 0
        
        for classe in classes:
            # Récupérer les étudiants de cette classe
            etudiants_query = Utilisateur.objects.filter(
                type_utilisateur='etudiant',
                classe__icontains=classe.nom,
                is_active=True
            )
            
            # Recherche par nom, prénom, email
            if recherche:
                etudiants_query = etudiants_query.filter(
                    Q(first_name__icontains=recherche) |
                    Q(last_name__icontains=recherche) |
                    Q(username__icontains=recherche) |
                    Q(email__icontains=recherche)
                )
            
            etudiants = etudiants_query.order_by('last_name', 'first_name')
            nb_etudiants = etudiants.count()
            total_etudiants_formation += nb_etudiants
            
            # Statistiques pour cette classe
            cours_classe = Cours.objects.filter(classe=classe, actif=True)
            progressions = ProgressionEtudiant.objects.filter(cours__in=cours_classe)
            moyenne_progression = progressions.aggregate(Avg('pourcentage_completion'))['pourcentage_completion__avg'] or 0
            
            classes_data.append({
                'classe': classe,
                'etudiants': etudiants,
                'nb_etudiants': nb_etudiants,
                'nb_cours': cours_classe.count(),
                'moyenne_progression': round(moyenne_progression, 1),
            })
        
        if classes_data or not classe_id:  # Afficher même si pas d'étudiants
            formations_data.append({
                'formation': formation,
                'classes': classes_data,
                'total_etudiants': total_etudiants_formation,
                'total_classes': len(classes_data),
            })
            total_etudiants_global += total_etudiants_formation
    
    context = {
        'formations_data': formations_data,
        'total_etudiants_global': total_etudiants_global,
        'toutes_formations': Formation.objects.filter(actif=True).order_by('nom'),
        'formation_filtre': int(formation_id) if formation_id else None,
        'classe_filtre': int(classe_id) if classe_id else None,
        'recherche': recherche,
    }
    
    return render(request, 'administration/liste_etudiants_par_formation.html', context)


@coordination_required
def gestion_inscriptions(request):
    """Gestion des inscriptions aux formations"""
    formations = Formation.objects.filter(actif=True).order_by('nom')
    
    # Statistiques par formation
    stats_formations = []
    for formation in formations:
        classes = Classe.objects.filter(formation=formation, actif=True)
        etudiants = Utilisateur.objects.filter(
            type_utilisateur='etudiant',
            is_active=True
        )
        
        # Compter les étudiants par classe de cette formation
        nb_etudiants = 0
        for classe in classes:
            nb_etudiants += etudiants.filter(classe__icontains=classe.nom).count()
        
        stats_formations.append({
            'formation': formation,
            'nb_classes': classes.count(),
            'nb_etudiants': nb_etudiants,
        })
    
    context = {
        'formations': formations,
        'stats_formations': stats_formations,
    }
    
    return render(request, 'administration/gestion_inscriptions.html', context)


@coordination_required
def detail_inscriptions_formation(request, formation_id):
    """Détail des inscriptions pour une formation spécifique"""
    formation = get_object_or_404(Formation, pk=formation_id)
    classes = Classe.objects.filter(formation=formation, actif=True).order_by('nom')
    
    # Étudiants par classe
    etudiants_par_classe = {}
    for classe in classes:
        etudiants = Utilisateur.objects.filter(
            type_utilisateur='etudiant',
            classe__icontains=classe.nom,
            is_active=True
        ).order_by('last_name', 'first_name')
        
        etudiants_par_classe[classe.id] = {
            'classe': classe,
            'etudiants': etudiants,
            'nb_etudiants': etudiants.count(),
        }
    
    context = {
        'formation': formation,
        'classes': classes,
        'etudiants_par_classe': etudiants_par_classe,
    }
    
    return render(request, 'administration/detail_inscriptions_formation.html', context)


@coordination_required
def gestion_stages_cscom(request):
    """Gestion des stages CSCom-U pour les années 2 et 3"""
    # Récupérer les CSCom-U disponibles
    cscom_urbains = CSComUCentre.objects.filter(type_centre='urbain', actif=True).order_by('nom')
    cscom_ruraux = CSComUCentre.objects.filter(type_centre='rural', actif=True).order_by('nom')
    
    # Récupérer les stages existants
    stages = StageRotationDES.objects.select_related('etudiant', 'centre').order_by('annee', 'periode', 'etudiant__username')
    
    # Statistiques par année
    stats_annees = {}
    for annee in [2, 3]:
        stages_annee = stages.filter(annee=annee)
        stats_annees[annee] = {
            'periode_1': stages_annee.filter(periode=1).count(),
            'periode_2': stages_annee.filter(periode=2).count(),
            'total': stages_annee.count(),
        }
    
    context = {
        'cscom_urbains': cscom_urbains,
        'cscom_ruraux': cscom_ruraux,
        'stages': stages,
        'stats_annees': stats_annees,
    }
    
    return render(request, 'administration/gestion_stages_cscom.html', context)


@coordination_required
def tirage_au_sort_stages(request):
    """Tirage au sort des stages CSCom-U"""
    if request.method == 'POST':
        annee = int(request.POST.get('annee'))
        periode = int(request.POST.get('periode'))
        
        # Récupérer les étudiants de l'année correspondante
        # On suppose que les étudiants ont une classe qui indique leur année
        formation_desmfmc = Formation.objects.filter(code__icontains='DESMFMC').first()
        if not formation_desmfmc:
            messages.error(request, "Formation DESMFMC introuvable.")
            return redirect('gestion_stages_cscom')
        
        # Récupérer la classe correspondant à l'année
        classe = Classe.objects.filter(
            formation=formation_desmfmc,
            annee=annee
        ).first()
        
        if not classe:
            messages.error(request, f"Classe pour l'année {annee} introuvable.")
            return redirect('gestion_stages_cscom')
        
        # Récupérer les étudiants de cette classe
        etudiants = Utilisateur.objects.filter(
            type_utilisateur='etudiant',
            classe__icontains=classe.nom,
            is_active=True
        )
        
        if not etudiants.exists():
            messages.error(request, f"Aucun étudiant trouvé pour l'année {annee}.")
            return redirect('gestion_stages_cscom')
        
        # Dates optionnelles
        date_debut = None
        date_fin = None
        if request.POST.get('date_debut'):
            try:
                date_debut = datetime.strptime(request.POST.get('date_debut'), '%Y-%m-%d').date()
            except ValueError:
                pass
        if request.POST.get('date_fin'):
            try:
                date_fin = datetime.strptime(request.POST.get('date_fin'), '%Y-%m-%d').date()
            except ValueError:
                pass
        
        # Effectuer le tirage au sort
        resultat = attribuer_stages_cscom_aleatoire(etudiants, annee, periode, date_debut, date_fin)
        
        if resultat['reussite']:
            messages.success(
                request,
                f"Tirage au sort effectué avec succès ! {len(resultat['attributions'])} stages attribués."
            )
        else:
            messages.warning(
                request,
                f"Tirage au sort partiellement effectué. Erreurs : {', '.join(resultat['erreurs'])}"
            )
        
        return redirect('gestion_stages_cscom')
    
    return redirect('gestion_stages_cscom')


@coordination_required
def bulletins_classe(request, classe_id):
    """Génère les bulletins de notes au format A4 pour une classe"""
    classe = get_object_or_404(Classe, pk=classe_id, actif=True)
    
    # Récupérer tous les étudiants de la classe
    etudiants = Utilisateur.objects.filter(
        type_utilisateur='etudiant',
        is_active=True,
        classe__icontains=classe.nom
    ).order_by('last_name', 'first_name')
    
    # Récupérer les évaluations finales (sommative ou certificative)
    type_eval_finale = TypeEvaluation.objects.filter(
        nature__in=['sommative', 'certificative']
    ).first()
    
    if not type_eval_finale:
        # Si aucun type n'existe, prendre toutes les évaluations actives
        evaluations = Evaluation.objects.filter(
            cours__classe=classe,
            actif=True
        ).select_related('cours', 'type_evaluation').order_by('cours__ordre', 'date_evaluation')
    else:
        evaluations = Evaluation.objects.filter(
            cours__classe=classe,
            type_evaluation=type_eval_finale,
            actif=True
        ).select_related('cours', 'type_evaluation').order_by('cours__ordre', 'date_evaluation')
    
    # Organiser les données par étudiant
    bulletins_data = []
    
    for etudiant in etudiants:
        # Récupérer tous les résultats de cet étudiant
        resultats = ResultatEvaluation.objects.filter(
            etudiant=etudiant,
            evaluation__in=evaluations,
            note_obtenue__isnull=False
        ).select_related('evaluation', 'evaluation__cours').order_by('evaluation__cours__ordre', 'evaluation__date_evaluation')
        
        # Organiser par cours
        cours_notes = {}
        total_points = Decimal('0.00')
        total_coefficient = Decimal('0.00')
        
        for resultat in resultats:
            cours = resultat.evaluation.cours
            coeff = resultat.evaluation.coefficient
            note = resultat.note_obtenue
            note_sur = resultat.note_sur or resultat.evaluation.note_maximale
            
            # Normaliser la note sur 20
            note_normalisee = (note / note_sur) * Decimal('20.00') if note_sur > 0 else Decimal('0.00')
            points_ponderes = note_normalisee * coeff
            
            if cours.id not in cours_notes:
                cours_notes[cours.id] = {
                    'cours': cours,
                    'evaluations': [],
                    'total_points': Decimal('0.00'),
                    'total_coefficient': Decimal('0.00'),
                }
            
            cours_notes[cours.id]['evaluations'].append({
                'evaluation': resultat.evaluation,
                'note': note,
                'note_sur': note_sur,
                'note_normalisee': note_normalisee,
                'coefficient': coeff,
                'date': resultat.date_evaluation or resultat.evaluation.date_evaluation,
            })
            
            cours_notes[cours.id]['total_points'] += points_ponderes
            cours_notes[cours.id]['total_coefficient'] += coeff
            total_points += points_ponderes
            total_coefficient += coeff
        
        # Calculer les moyennes par cours
        cours_moyennes = []
        for cours_id, data in cours_notes.items():
            moyenne_cours = (data['total_points'] / data['total_coefficient']) if data['total_coefficient'] > 0 else None
            cours_moyennes.append({
                'cours': data['cours'],
                'evaluations': data['evaluations'],
                'moyenne': moyenne_cours,
                'coefficient': data['total_coefficient'],
            })
        
        # Trier par ordre du cours
        cours_moyennes.sort(key=lambda x: x['cours'].ordre if x['cours'].ordre else 999)
        
        # Calculer la moyenne générale
        moyenne_generale = (total_points / total_coefficient) if total_coefficient > 0 else None
        
        bulletins_data.append({
            'etudiant': etudiant,
            'cours_moyennes': cours_moyennes,
            'moyenne_generale': moyenne_generale,
            'total_coefficient': total_coefficient,
            'nb_evaluations': resultats.count(),
        })
    
    context = {
        'classe': classe,
        'bulletins_data': bulletins_data,
        'annee_scolaire': timezone.now().year,
        'date_emission': timezone.now().date(),
    }
    
    return render(request, 'administration/bulletins_classe.html', context)


@coordination_required
def gestion_enseignants(request):
    """Gestion des enseignants - Liste avec leurs spécialités, cours et leçons"""
    # Récupérer tous les enseignants actifs avec statistiques
    enseignants = Utilisateur.objects.filter(
        type_utilisateur='enseignant',
        is_active=True
    ).annotate(
        nb_cours_principaux=Count('cours_enseignes', filter=Q(cours_enseignes__actif=True)),
        nb_cours_co=Count('cours_co_enseignes', filter=Q(cours_co_enseignes__actif=True))
    ).order_by('last_name', 'first_name')
    
    # Calculer le nombre de leçons pour chaque enseignant
    for enseignant in enseignants:
        cours_ids = list(
            enseignant.cours_enseignes.filter(actif=True).values_list('id', flat=True)
        ) + list(
            enseignant.cours_co_enseignes.filter(actif=True).values_list('id', flat=True)
        )
        enseignant.nb_lecons = Lecon.objects.filter(
            cours__id__in=cours_ids,
            actif=True
        ).count() if cours_ids else 0
    
    # Recherche par nom, email ou spécialité
    recherche = request.GET.get('recherche', '')
    if recherche:
        enseignants = enseignants.filter(
            Q(first_name__icontains=recherche) |
            Q(last_name__icontains=recherche) |
            Q(username__icontains=recherche) |
            Q(email__icontains=recherche) |
            Q(matieres__icontains=recherche)
        )
    
    # Préparer les données pour chaque enseignant
    enseignants_list = []
    for enseignant in enseignants:
        specialites = []
        if enseignant.matieres:
            specialites = [m.strip() for m in enseignant.matieres.split(',') if m.strip()]
        
        # Le nombre de leçons est déjà calculé dans la boucle précédente
        enseignants_list.append({
            'enseignant': enseignant,
            'specialites': specialites,
        })
    
    context = {
        'enseignants_list': enseignants_list,
        'recherche': recherche,
    }
    
    return render(request, 'administration/gestion_enseignants.html', context)


@coordination_required
def detail_enseignant(request, enseignant_id):
    """Détail d'un enseignant avec ses cours, leçons et informations"""
    enseignant = get_object_or_404(
        Utilisateur,
        pk=enseignant_id,
        type_utilisateur='enseignant',
        is_active=True
    )
    
    # Cours où l'enseignant est responsable principal
    cours_principaux = Cours.objects.filter(
        enseignant=enseignant,
        actif=True
    ).select_related('classe', 'classe__formation').order_by('classe', 'ordre', 'date_debut')
    
    # Cours où l'enseignant est co-enseignant
    cours_co = Cours.objects.filter(
        co_enseignants=enseignant,
        actif=True
    ).select_related('classe', 'classe__formation').order_by('classe', 'ordre', 'date_debut')
    
    # Toutes les leçons des cours où l'enseignant enseigne
    cours_ids = list(cours_principaux.values_list('id', flat=True)) + list(cours_co.values_list('id', flat=True))
    lecons = Lecon.objects.filter(
        cours__id__in=cours_ids,
        actif=True
    ).select_related('cours', 'cours__classe').order_by('cours', 'ordre', 'numero')
    
    # Statistiques
    stats = {
        'nb_cours_principaux': cours_principaux.count(),
        'nb_cours_co': cours_co.count(),
        'nb_lecons': lecons.count(),
        'nb_classes': Classe.objects.filter(
            Q(cours__enseignant=enseignant) | Q(cours__co_enseignants=enseignant),
            actif=True
        ).distinct().count(),
    }
    
    # Spécialités (matières enseignées)
    specialites = []
    if enseignant.matieres:
        specialites = [m.strip() for m in enseignant.matieres.split(',') if m.strip()]
    
    context = {
        'enseignant': enseignant,
        'cours_principaux': cours_principaux,
        'cours_co': cours_co,
        'lecons': lecons,
        'stats': stats,
        'specialites': specialites,
    }
    
    return render(request, 'administration/detail_enseignant.html', context)


@coordination_required
def modifier_enseignant(request, enseignant_id):
    """Modifier les informations d'un enseignant"""
    enseignant = get_object_or_404(
        Utilisateur,
        pk=enseignant_id,
        type_utilisateur='enseignant',
        is_active=True
    )
    
    if request.method == 'POST':
        # Mettre à jour les informations
        enseignant.first_name = request.POST.get('first_name', enseignant.first_name)
        enseignant.last_name = request.POST.get('last_name', enseignant.last_name)
        enseignant.email = request.POST.get('email', enseignant.email)
        enseignant.telephone = request.POST.get('telephone', enseignant.telephone)
        enseignant.adresse = request.POST.get('adresse', enseignant.adresse)
        enseignant.matieres = request.POST.get('matieres', enseignant.matieres)
        enseignant.niveau_acces = request.POST.get('niveau_acces', enseignant.niveau_acces)
        
        # Vérifier si l'email est unique (sauf pour cet utilisateur)
        email_existant = Utilisateur.objects.filter(email=enseignant.email).exclude(pk=enseignant_id).exists()
        if email_existant:
            messages.error(request, f"L'email {enseignant.email} est déjà utilisé par un autre utilisateur.")
        else:
            enseignant.save()
            messages.success(request, f"Les informations de {enseignant.get_full_name()} ont été mises à jour avec succès.")
            return redirect('detail_enseignant', enseignant_id=enseignant_id)
    
    context = {
        'enseignant': enseignant,
    }
    
    return render(request, 'administration/modifier_enseignant.html', context)


@coordination_required
def assigner_cours_enseignant(request, enseignant_id):
    """Assigner ou réassigner des cours à un enseignant"""
    enseignant = get_object_or_404(
        Utilisateur,
        pk=enseignant_id,
        type_utilisateur='enseignant',
        is_active=True
    )
    
    if request.method == 'POST':
        action = request.POST.get('action')
        cours_id = request.POST.get('cours_id')
        
        try:
            cours = Cours.objects.get(pk=cours_id, actif=True)
            
            if action == 'assigner_principal':
                # Assigner comme enseignant principal
                cours.enseignant = enseignant
                cours.save()
                messages.success(request, f"{cours.titre} a été assigné à {enseignant.get_full_name()} comme enseignant principal.")
            
            elif action == 'assigner_co':
                # Ajouter comme co-enseignant
                cours.co_enseignants.add(enseignant)
                messages.success(request, f"{enseignant.get_full_name()} a été ajouté comme co-enseignant pour {cours.titre}.")
            
            elif action == 'retirer_co':
                # Retirer comme co-enseignant
                cours.co_enseignants.remove(enseignant)
                messages.success(request, f"{enseignant.get_full_name()} a été retiré comme co-enseignant pour {cours.titre}.")
            
            elif action == 'retirer_principal':
                # Retirer comme enseignant principal
                cours.enseignant = None
                cours.save()
                messages.success(request, f"{enseignant.get_full_name()} a été retiré comme enseignant principal de {cours.titre}.")
        
        except Cours.DoesNotExist:
            messages.error(request, "Cours introuvable.")
        
        return redirect('detail_enseignant', enseignant_id=enseignant_id)
    
    # Récupérer tous les cours actifs pour l'assignation
    tous_cours = Cours.objects.filter(actif=True).select_related('classe', 'classe__formation', 'enseignant').order_by('classe', 'titre')
    
    # Cours déjà assignés
    cours_principaux = enseignant.cours_enseignes.filter(actif=True)
    cours_co = enseignant.cours_co_enseignes.filter(actif=True)
    cours_principaux_ids = set(cours_principaux.values_list('id', flat=True))
    cours_co_ids = set(cours_co.values_list('id', flat=True))
    
    # Préparer les cours avec leur statut d'assignation
    cours_list = []
    for cours in tous_cours:
        cours_list.append({
            'cours': cours,
            'est_principal': cours.id in cours_principaux_ids,
            'est_co': cours.id in cours_co_ids,
        })
    
    context = {
        'enseignant': enseignant,
        'cours_list': cours_list,
        'cours_principaux': cours_principaux,
        'cours_co': cours_co,
    }
    
    return render(request, 'administration/assigner_cours_enseignant.html', context)


@coordination_required
def ajouter_enseignant(request):
    """Ajouter un nouvel enseignant"""
    if request.method == 'POST':
        form = InscriptionEnseignantForm(request.POST)
        if form.is_valid():
            enseignant = form.save(commit=False)
            # Récupérer les données supplémentaires du formulaire
            enseignant.telephone = request.POST.get('telephone', '')
            enseignant.adresse = request.POST.get('adresse', '')
            enseignant.niveau_acces = request.POST.get('niveau_acces', 'standard')
            # Pour l'administration, on peut marquer l'email comme vérifié
            enseignant.email_verifie = True
            enseignant.is_active = True
            enseignant.save()
            
            messages.success(
                request, 
                f"L'enseignant {enseignant.get_full_name()} a été créé avec succès !"
            )
            return redirect('detail_enseignant', enseignant_id=enseignant.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = InscriptionEnseignantForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'administration/ajouter_enseignant.html', context)


# ==================== VUES PDF ET EXPORT ====================

@coordination_required
def pdf_liste_etudiants(request, classe_id=None):
    """Génère un PDF de la liste des étudiants"""
    if classe_id:
        classe = get_object_or_404(Classe, pk=classe_id, actif=True)
        etudiants = Utilisateur.objects.filter(
            type_utilisateur='etudiant',
            is_active=True,
            classe__icontains=classe.nom
        ).order_by('last_name', 'first_name')
        filename = f"liste_etudiants_{classe.nom.replace(' ', '_')}.pdf"
    else:
        classe = None
        etudiants = Utilisateur.objects.filter(
            type_utilisateur='etudiant',
            is_active=True
        ).order_by('last_name', 'first_name')
        filename = "liste_etudiants_complete.pdf"
    
    context = {
        'etudiants': etudiants,
        'classe': classe,
        'date_emission': timezone.now().date(),
    }
    
    return generate_pdf_from_template(
        'pdf/liste_etudiants.html',
        context,
        filename
    )


@coordination_required
def pdf_stages(request, annee=None):
    """Génère un PDF de la liste des stages"""
    stages = StageRotationDES.objects.select_related('etudiant', 'centre').order_by('annee', 'periode', 'etudiant__username')
    
    if annee:
        stages = stages.filter(annee=annee)
        filename = f"liste_stages_annee_{annee}.pdf"
    else:
        filename = "liste_stages_complete.pdf"
    
    # Grouper par année et période
    stages_par_annee = {}
    for stage in stages:
        if stage.annee not in stages_par_annee:
            stages_par_annee[stage.annee] = {}
        if stage.periode not in stages_par_annee[stage.annee]:
            stages_par_annee[stage.annee][stage.periode] = []
        stages_par_annee[stage.annee][stage.periode].append(stage)
    
    context = {
        'stages_par_annee': stages_par_annee,
        'date_emission': timezone.now().date(),
    }
    
    return generate_pdf_from_template(
        'pdf/liste_stages.html',
        context,
        filename
    )


@coordination_required
def pdf_bulletins(request, classe_id):
    """Génère un PDF des bulletins de notes pour une classe"""
    classe = get_object_or_404(Classe, pk=classe_id, actif=True)
    
    # Réutiliser la logique de bulletins_classe
    etudiants = Utilisateur.objects.filter(
        type_utilisateur='etudiant',
        is_active=True,
        classe__icontains=classe.nom
    ).order_by('last_name', 'first_name')
    
    type_eval_finale = TypeEvaluation.objects.filter(
        nature__in=['sommative', 'certificative']
    ).first()
    
    if not type_eval_finale:
        evaluations = Evaluation.objects.filter(
            cours__classe=classe,
            actif=True
        ).select_related('cours', 'type_evaluation').order_by('cours__ordre', 'date_evaluation')
    else:
        evaluations = Evaluation.objects.filter(
            cours__classe=classe,
            type_evaluation=type_eval_finale,
            actif=True
        ).select_related('cours', 'type_evaluation').order_by('cours__ordre', 'date_evaluation')
    
    bulletins_data = []
    
    for etudiant in etudiants:
        resultats = ResultatEvaluation.objects.filter(
            etudiant=etudiant,
            evaluation__in=evaluations,
            note_obtenue__isnull=False
        ).select_related('evaluation', 'evaluation__cours').order_by('evaluation__cours__ordre', 'evaluation__date_evaluation')
        
        cours_notes = {}
        total_points = Decimal('0.00')
        total_coefficient = Decimal('0.00')
        
        for resultat in resultats:
            cours = resultat.evaluation.cours
            coeff = resultat.evaluation.coefficient
            note = resultat.note_obtenue
            note_sur = resultat.note_sur or resultat.evaluation.note_maximale
            
            note_normalisee = (note / note_sur) * Decimal('20.00') if note_sur > 0 else Decimal('0.00')
            points_ponderes = note_normalisee * coeff
            
            if cours.id not in cours_notes:
                cours_notes[cours.id] = {
                    'cours': cours,
                    'evaluations': [],
                    'total_points': Decimal('0.00'),
                    'total_coefficient': Decimal('0.00'),
                }
            
            cours_notes[cours.id]['evaluations'].append({
                'evaluation': resultat.evaluation,
                'note': note,
                'note_sur': note_sur,
                'note_normalisee': note_normalisee,
                'coefficient': coeff,
                'date': resultat.date_evaluation or resultat.evaluation.date_evaluation,
            })
            
            cours_notes[cours.id]['total_points'] += points_ponderes
            cours_notes[cours.id]['total_coefficient'] += coeff
            total_points += points_ponderes
            total_coefficient += coeff
        
        cours_moyennes = []
        for cours_id, data in cours_notes.items():
            moyenne_cours = (data['total_points'] / data['total_coefficient']) if data['total_coefficient'] > 0 else None
            cours_moyennes.append({
                'cours': data['cours'],
                'evaluations': data['evaluations'],
                'moyenne': moyenne_cours,
                'coefficient': data['total_coefficient'],
            })
        
        cours_moyennes.sort(key=lambda x: x['cours'].ordre if x['cours'].ordre else 999)
        moyenne_generale = (total_points / total_coefficient) if total_coefficient > 0 else None
        
        bulletins_data.append({
            'etudiant': etudiant,
            'cours_moyennes': cours_moyennes,
            'moyenne_generale': moyenne_generale,
            'total_coefficient': total_coefficient,
            'nb_evaluations': resultats.count(),
        })
    
    context = {
        'classe': classe,
        'bulletins_data': bulletins_data,
        'annee_scolaire': timezone.now().year,
        'date_emission': timezone.now().date(),
    }
    
    filename = f"bulletins_{classe.nom.replace(' ', '_')}.pdf"
    return generate_pdf_from_template(
        'pdf/bulletins_classe.html',
        context,
        filename
    )


@coordination_required
def envoyer_pdf_par_email(request):
    """Envoie un PDF par email"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    doc_type = request.POST.get('doc_type')
    recipient_email = request.POST.get('email')
    classe_id = request.POST.get('classe_id')
    annee = request.POST.get('annee')
    
    if not recipient_email:
        return JsonResponse({'success': False, 'error': 'Email requis'})
    
    try:
        if doc_type == 'liste_etudiants':
            if classe_id:
                classe = get_object_or_404(Classe, pk=classe_id)
                etudiants = Utilisateur.objects.filter(
                    type_utilisateur='etudiant',
                    is_active=True,
                    classe__icontains=classe.nom
                ).order_by('last_name', 'first_name')
                filename = f"liste_etudiants_{classe.nom.replace(' ', '_')}.pdf"
                context = {'etudiants': etudiants, 'classe': classe, 'date_emission': timezone.now().date()}
                template = 'pdf/liste_etudiants.html'
            else:
                return JsonResponse({'success': False, 'error': 'Classe requise'})
        
        elif doc_type == 'stages':
            stages = StageRotationDES.objects.select_related('etudiant', 'centre')
            if annee:
                stages = stages.filter(annee=annee)
            stages_par_annee = {}
            for stage in stages:
                if stage.annee not in stages_par_annee:
                    stages_par_annee[stage.annee] = {}
                if stage.periode not in stages_par_annee[stage.annee]:
                    stages_par_annee[stage.annee][stage.periode] = []
                stages_par_annee[stage.annee][stage.periode].append(stage)
            filename = f"liste_stages_annee_{annee}.pdf" if annee else "liste_stages_complete.pdf"
            context = {'stages_par_annee': stages_par_annee, 'date_emission': timezone.now()}
            template = 'pdf/liste_stages.html'
        
        elif doc_type == 'bulletins':
            if not classe_id:
                return JsonResponse({'success': False, 'error': 'Classe requise'})
            # Réutiliser la logique de pdf_bulletins
            response = pdf_bulletins(request, classe_id)
            pdf_content = response.content
            filename = f"bulletins_{Classe.objects.get(pk=classe_id).nom.replace(' ', '_')}.pdf"
            subject = f"Bulletins de notes - {Classe.objects.get(pk=classe_id).nom}"
            message = f"Veuillez trouver ci-joint les bulletins de notes pour la classe {Classe.objects.get(pk=classe_id).nom}."
            success = send_pdf_by_email(pdf_content, filename, subject, message, recipient_email)
            return JsonResponse({'success': success})
        
        else:
            return JsonResponse({'success': False, 'error': 'Type de document invalide'})
        
        # Générer le PDF
        response = generate_pdf_from_template(template, context, filename)
        pdf_content = response.content
        
        # Envoyer par email
        subject_map = {
            'liste_etudiants': f"Liste des étudiants - {classe.nom if classe_id else 'Toutes les classes'}",
            'stages': f"Liste des stages - Année {annee}" if annee else "Liste complète des stages",
        }
        subject = subject_map.get(doc_type, 'Document PDF')
        message = f"Veuillez trouver ci-joint le document demandé."
        
        success = send_pdf_by_email(pdf_content, filename, subject, message, recipient_email)
        return JsonResponse({'success': success})
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# ==================== VUES PDF LETTRES D'INFORMATIONS ====================

@coordination_required
def pdf_lettre_information(request, lettre_id):
    """Génère un PDF d'une lettre d'information"""
    lettre = get_object_or_404(LettreInformation, pk=lettre_id, actif=True)
    
    destinataires = lettre.get_destinataires_list()
    
    context = {
        'lettre': lettre,
        'destinataires': destinataires,
        'date_emission': timezone.now().date(),
    }
    
    filename = f"lettre_information_{lettre.id}_{lettre.titre[:30].replace(' ', '_')}.pdf"
    return generate_pdf_from_template(
        'pdf/lettre_information.html',
        context,
        filename
    )


@coordination_required
def pdf_lettres_informations(request):
    """Génère un PDF de toutes les lettres d'informations actives"""
    lettres = LettreInformation.objects.filter(actif=True).order_by('-date_envoi')
    
    context = {
        'lettres': lettres,
        'date_emission': timezone.now().date(),
    }
    
    filename = "lettres_informations_complete.pdf"
    return generate_pdf_from_template(
        'pdf/lettres_informations.html',
        context,
        filename
    )


# ==================== VUES POUR ÉTUDIANTS ====================

@login_required(login_url='login')
def etudiant_download_bulletin(request):
    """Permet à un étudiant de télécharger son propre bulletin"""
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    etudiant = request.user
    
    # Récupérer la classe de l'étudiant
    classe_obj = etudiant.get_classe_obj()
    if not classe_obj:
        messages.error(request, "Aucune classe associée.")
        return redirect('dashboard_etudiant')
    
    # Réutiliser la logique de pdf_bulletins mais pour un seul étudiant
    type_eval_finale = TypeEvaluation.objects.filter(
        nature__in=['sommative', 'certificative']
    ).first()
    
    if not type_eval_finale:
        evaluations = Evaluation.objects.filter(
            cours__classe=classe_obj,
            actif=True
        ).select_related('cours', 'type_evaluation').order_by('cours__ordre', 'date_evaluation')
    else:
        evaluations = Evaluation.objects.filter(
            cours__classe=classe_obj,
            type_evaluation=type_eval_finale,
            actif=True
        ).select_related('cours', 'type_evaluation').order_by('cours__ordre', 'date_evaluation')
    
    resultats = ResultatEvaluation.objects.filter(
        etudiant=etudiant,
        evaluation__in=evaluations,
        note_obtenue__isnull=False
    ).select_related('evaluation', 'evaluation__cours').order_by('evaluation__cours__ordre', 'evaluation__date_evaluation')
    
    cours_notes = {}
    total_points = Decimal('0.00')
    total_coefficient = Decimal('0.00')
    
    for resultat in resultats:
        cours = resultat.evaluation.cours
        coeff = resultat.evaluation.coefficient
        note = resultat.note_obtenue
        note_sur = resultat.note_sur or resultat.evaluation.note_maximale
        
        note_normalisee = (note / note_sur) * Decimal('20.00') if note_sur > 0 else Decimal('0.00')
        points_ponderes = note_normalisee * coeff
        
        if cours.id not in cours_notes:
            cours_notes[cours.id] = {
                'cours': cours,
                'evaluations': [],
                'total_points': Decimal('0.00'),
                'total_coefficient': Decimal('0.00'),
            }
        
        cours_notes[cours.id]['evaluations'].append({
            'evaluation': resultat.evaluation,
            'note': note,
            'note_sur': note_sur,
            'note_normalisee': note_normalisee,
            'coefficient': coeff,
            'date': resultat.date_evaluation or resultat.evaluation.date_evaluation,
        })
        
        cours_notes[cours.id]['total_points'] += points_ponderes
        cours_notes[cours.id]['total_coefficient'] += coeff
        total_points += points_ponderes
        total_coefficient += coeff
    
    cours_moyennes = []
    for cours_id, data in cours_notes.items():
        moyenne_cours = (data['total_points'] / data['total_coefficient']) if data['total_coefficient'] > 0 else None
        cours_moyennes.append({
            'cours': data['cours'],
            'evaluations': data['evaluations'],
            'moyenne': moyenne_cours,
            'coefficient': data['total_coefficient'],
        })
    
    cours_moyennes.sort(key=lambda x: x['cours'].ordre if x['cours'].ordre else 999)
    moyenne_generale = (total_points / total_coefficient) if total_coefficient > 0 else None
    
    bulletin_data = {
        'etudiant': etudiant,
        'cours_moyennes': cours_moyennes,
        'moyenne_generale': moyenne_generale,
        'total_coefficient': total_coefficient,
        'nb_evaluations': resultats.count(),
    }
    
    context = {
        'classe': classe_obj,
        'bulletins_data': [bulletin_data],
        'annee_scolaire': timezone.now().year,
        'date_emission': timezone.now().date(),
    }
    
    filename = f"bulletin_{etudiant.username}_{classe_obj.nom.replace(' ', '_')}.pdf"
    return generate_pdf_from_template(
        'pdf/bulletins_classe.html',
        context,
        filename
    )


@login_required(login_url='login')
def etudiant_download_lettre(request, lettre_id):
    """Permet à un étudiant de télécharger une lettre d'information qui lui est destinée"""
    if not request.user.est_etudiant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux étudiants.")
        return redirect('accueil')
    
    lettre = get_object_or_404(LettreInformation, pk=lettre_id, actif=True)
    etudiant = request.user
    
    # Vérifier que l'étudiant est destinataire
    destinataires = lettre.get_destinataires_list()
    if etudiant not in destinataires and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas accès à cette lettre.")
        return redirect('dashboard_etudiant')
    
    context = {
        'lettre': lettre,
        'destinataires': [etudiant],
        'date_emission': timezone.now().date(),
    }
    
    filename = f"lettre_{lettre.id}_{lettre.titre[:30].replace(' ', '_')}.pdf"
    return generate_pdf_from_template(
        'pdf/lettre_information.html',
        context,
        filename
    )


# ==================== VUES POUR ENSEIGNANTS ====================

@login_required(login_url='login')
def enseignant_download_stages(request, annee=None):
    """Permet à un enseignant de télécharger la liste des stages"""
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    stages = StageRotationDES.objects.select_related('etudiant', 'centre').order_by('annee', 'periode', 'etudiant__username')
    
    if annee:
        stages = stages.filter(annee=annee)
        filename = f"liste_stages_annee_{annee}.pdf"
    else:
        filename = "liste_stages_complete.pdf"
    
    # Grouper par année et période
    stages_par_annee = {}
    for stage in stages:
        if stage.annee not in stages_par_annee:
            stages_par_annee[stage.annee] = {}
        if stage.periode not in stages_par_annee[stage.annee]:
            stages_par_annee[stage.annee][stage.periode] = []
        stages_par_annee[stage.annee][stage.periode].append(stage)
    
    context = {
        'stages_par_annee': stages_par_annee,
        'date_emission': timezone.now(),
    }
    
    return generate_pdf_from_template(
        'pdf/liste_stages.html',
        context,
        filename
    )


@login_required(login_url='login')
def enseignant_download_lettre(request, lettre_id):
    """Permet à un enseignant de télécharger une lettre d'information"""
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    lettre = get_object_or_404(LettreInformation, pk=lettre_id, actif=True)
    
    # Les enseignants peuvent voir toutes les lettres d'information
    destinataires = lettre.get_destinataires_list()
    
    context = {
        'lettre': lettre,
        'destinataires': destinataires,
        'date_emission': timezone.now().date(),
    }
    
    filename = f"lettre_{lettre.id}_{lettre.titre[:30].replace(' ', '_')}.pdf"
    return generate_pdf_from_template(
        'pdf/lettre_information.html',
        context,
        filename
    )


@login_required(login_url='login')
def enseignant_download_modele_pedagogique(request, modele_id):
    """Permet à un enseignant de télécharger un modèle pédagogique"""
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    modele = get_object_or_404(ModelePedagogique, pk=modele_id, actif=True, visible_enseignants=True)
    
    if not modele.fichier:
        messages.error(request, "Aucun fichier disponible pour ce modèle.")
        return redirect('dashboard_enseignant')
    
    return FileResponse(
        modele.fichier.open(),
        as_attachment=True,
        filename=modele.fichier.name.split('/')[-1]
    )


@login_required(login_url='login')
def enseignant_liste_modeles_pedagogiques(request):
    """Liste des modèles pédagogiques disponibles pour les enseignants"""
    if not request.user.est_enseignant() and not request.user.is_superuser:
        messages.error(request, "Accès réservé aux enseignants.")
        return redirect('accueil')
    
    modeles = ModelePedagogique.objects.filter(
        actif=True,
        visible_enseignants=True
    ).order_by('-date_creation')
    
    context = {
        'modeles': modeles,
    }
    
    return render(request, 'enseignant/modeles_pedagogiques.html', context)


# ==================== GESTION SIGNATURE COORDINATION ====================

@coordination_required
def gestion_signature_coordination(request):
    """Gestion de la signature de la coordination pour les documents administratifs"""
    from apps.utilisateurs.models_documents import SignatureCoordination
    
    signature = SignatureCoordination.get_signature_active()
    
    if request.method == 'POST':
        if signature:
            # Mettre à jour la signature existante
            signature.nom_signataire = request.POST.get('nom_signataire', '')
            signature.prenom_signataire = request.POST.get('prenom_signataire', '')
            signature.titre_signataire = request.POST.get('titre_signataire', 'Coordonnateur DESMFMC')
            signature.est_directeur = request.POST.get('est_directeur') == 'on'
            signature.actif = request.POST.get('actif') == 'on'
            
            if 'cachet' in request.FILES:
                signature.cachet = request.FILES['cachet']
            
            # Si on active cette signature, désactiver les autres (sauf si c'est le directeur)
            if signature.actif:
                if signature.est_directeur:
                    # Le directeur a toujours la priorité, désactiver les autres directeurs
                    SignatureCoordination.objects.filter(actif=True, est_directeur=True).exclude(pk=signature.pk).update(est_directeur=False)
                else:
                    # Si ce n'est pas le directeur, ne pas désactiver les autres
                    pass
            
            signature.save()
            messages.success(request, "Signature mise à jour avec succès.")
        else:
            # Créer une nouvelle signature
            signature = SignatureCoordination.objects.create(
                nom_signataire=request.POST.get('nom_signataire', ''),
                prenom_signataire=request.POST.get('prenom_signataire', ''),
                titre_signataire=request.POST.get('titre_signataire', 'Coordonnateur DESMFMC'),
                est_directeur=request.POST.get('est_directeur') == 'on',
                actif=True
            )
            
            if 'cachet' in request.FILES:
                signature.cachet = request.FILES['cachet']
                signature.save()
            
            # Si c'est le directeur, désactiver les autres directeurs
            if signature.est_directeur:
                SignatureCoordination.objects.filter(est_directeur=True).exclude(pk=signature.pk).update(est_directeur=False)
            
            messages.success(request, "Signature créée avec succès.")
        
        return redirect('gestion_signature_coordination')
    
    context = {
        'signature': signature,
    }
    
    return render(request, 'administration/gestion_signature_coordination.html', context)


# ==================== UPLOAD COURS ET LEÇONS ====================

@coordination_required
def upload_cours_lecons(request):
    """Interface pour téléverser des cours et leçons directement"""
    from apps.utilisateurs.forms_upload import UploadCoursForm, UploadLeconForm
    from apps.utilisateurs.models_formation import Cours, Lecon
    
    # Statistiques
    total_cours = Cours.objects.filter(actif=True).count()
    total_lecons = Lecon.objects.filter(actif=True).count()
    cours_recent = Cours.objects.filter(actif=True).order_by('-date_creation')[:5]
    lecons_recentes = Lecon.objects.filter(actif=True).order_by('-date_creation')[:5]
    
    context = {
        'total_cours': total_cours,
        'total_lecons': total_lecons,
        'cours_recent': cours_recent,
        'lecons_recentes': lecons_recentes,
    }
    
    return render(request, 'administration/upload_cours_lecons.html', context)


@coordination_required
def upload_cours(request):
    """Vue pour téléverser un fichier de cours"""
    from apps.utilisateurs.forms_upload import UploadCoursForm
    from apps.utilisateurs.models_formation import Cours
    
    if request.method == 'POST':
        form = UploadCoursForm(request.POST, request.FILES)
        if form.is_valid():
            classe = form.cleaned_data['classe']
            titre = form.cleaned_data['titre']
            code = form.cleaned_data['code']
            description = form.cleaned_data.get('description', '')
            fichier_cours = form.cleaned_data['fichier_cours']
            enseignant = form.cleaned_data.get('enseignant')
            ordre = form.cleaned_data.get('ordre', 0)
            date_debut = form.cleaned_data.get('date_debut')
            date_fin = form.cleaned_data.get('date_fin')
            methodes_pedagogiques = form.cleaned_data.get('methodes_pedagogiques', [])
            description_methodes = form.cleaned_data.get('description_methodes', '')
            
            # Vérifier si un cours avec ce code existe déjà dans cette classe
            cours_existant = Cours.objects.filter(classe=classe, code=code).first()
            
            if cours_existant:
                # Mettre à jour le cours existant
                cours_existant.titre = titre
                cours_existant.description = description
                if enseignant:
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
            return redirect('upload_cours_lecons')
    else:
        form = UploadCoursForm()
    
    context = {
        'form': form,
        'type': 'cours',
    }
    
    return render(request, 'administration/upload_form.html', context)


@coordination_required
def upload_lecon(request):
    """Vue pour téléverser un fichier de leçon"""
    from apps.utilisateurs.forms_upload import UploadLeconForm
    from apps.utilisateurs.models_formation import Lecon
    
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
            
            return redirect('upload_cours_lecons')
    else:
        form = UploadLeconForm()
    
    context = {
        'form': form,
        'type': 'lecon',
    }
    
    return render(request, 'administration/upload_form.html', context)


# ==================== API POUR ADMIN DJANGO ====================

def get_cours_by_classe_json(request):
    """API JSON pour récupérer les cours d'une classe (utilisé par l'admin Django)"""
    from apps.utilisateurs.models_formation import Classe, Cours
    
    classe_id = request.GET.get('classe_id')
    
    if not classe_id:
        return JsonResponse({'cours': []})
    
    try:
        classe_id = int(classe_id)
        classe = Classe.objects.get(pk=classe_id, actif=True)
        cours_list = Cours.objects.filter(
            classe=classe, 
            actif=True
        ).select_related('classe', 'classe__formation').order_by('ordre', 'date_debut')
        
        cours_data = []
        for cours in cours_list:
            cours_data.append({
                'id': cours.id,
                'code': cours.code or '',
                'titre': cours.titre or '',
                'nombre_lecons': cours.lecons.filter(actif=True).count()
            })
        
        return JsonResponse({'cours': cours_data})
    except (Classe.DoesNotExist, ValueError, TypeError):
        return JsonResponse({'cours': []})
    except Exception as e:
        # En production, ne pas exposer l'erreur détaillée
        return JsonResponse({'error': 'Erreur lors de la récupération des cours'}, status=500)


@coordination_required
def evaluations_stages_coordination(request):
    """Vue pour la coordination pour voir toutes les évaluations de stage"""
    from apps.utilisateurs.models_carnet_stage import (
        EvaluationStage, CarnetStage, ProclamationResultats
    )
    from django.core.paginator import Paginator
    
    # Filtrer par classe si spécifié
    classe_id = request.GET.get('classe')
    classe_selected = None
    evaluations = EvaluationStage.objects.select_related(
        'carnet', 'carnet__etudiant', 'evalue_par_superviseur'
    ).all()
    
    if classe_id:
        try:
            classe_selected = Classe.objects.get(pk=classe_id, actif=True)
            # Récupérer les étudiants de cette classe
            etudiants_classe = Utilisateur.objects.filter(
                type_utilisateur='etudiant'
            ).filter(
                Q(classe__icontains=classe_selected.nom) | 
                Q(classe__icontains=classe_selected.nom.replace('DESMFMC', '').strip())
            )
            carnets = CarnetStage.objects.filter(etudiant__in=etudiants_classe, actif=True)
            evaluations = evaluations.filter(carnet__in=carnets)
        except Classe.DoesNotExist:
            messages.error(request, "Classe introuvable.")
    
    # Trier par date de création (plus récentes en premier)
    evaluations = evaluations.order_by('-date_creation', 'carnet__etudiant__username')
    
    # Pagination
    paginator = Paginator(evaluations, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Récupérer toutes les classes du DESMFMC
    classes_desmfmc = Classe.objects.filter(
        formation__nom__icontains='DESMFMC',
        actif=True
    ).order_by('nom')
    
    # Statistiques
    total_evaluations = evaluations.count()
    evaluations_completes = evaluations.filter(
        evalue_par_superviseur__isnull=False
    ).count()
    evaluations_validees = evaluations.filter(valide=True).count()
    
    context = {
        'evaluations': page_obj,
        'classes_desmfmc': classes_desmfmc,
        'classe_selected': classe_selected,
        'total_evaluations': total_evaluations,
        'evaluations_completes': evaluations_completes,
        'evaluations_validees': evaluations_validees,
    }
    
    return render(request, 'administration/evaluations_stages_coordination.html', context)


@coordination_required
def competences_par_jalon_classe(request):
    """Vue pour afficher les compétences organisées par jalon et classe"""
    
    # Filtres
    formation_id = request.GET.get('formation')
    annee = request.GET.get('annee')
    classe_id = request.GET.get('classe')
    
    # Récupérer la formation DESMFMC par défaut
    formation_desmfmc = Formation.objects.filter(code='DESMFMC', actif=True).first()
    if formation_id:
        formation_selected = Formation.objects.filter(pk=formation_id, actif=True).first()
    else:
        formation_selected = formation_desmfmc
    
    # Organiser par jalons
    jalons_data = []
    if formation_selected:
        jalons_query = JalonProgramme.objects.filter(
            formation=formation_selected
        ).order_by('annee', 'ordre')
        
        if annee:
            jalons_query = jalons_query.filter(annee=int(annee))
        
        for jalon in jalons_query:
            # Récupérer les compétences de ce jalon
            competences_jalon = Competence.objects.filter(jalons=jalon).distinct()
            
            # Récupérer les modules du jalon avec leurs compétences
            modules = jalon.modules.filter(actif=True).prefetch_related('competences_module').order_by('ordre')
            competences_modules = Competence.objects.filter(modules__in=modules).distinct()
            
            # Combiner les compétences (directes + via modules)
            toutes_competences = (competences_jalon | competences_modules).distinct()
            
            jalons_data.append({
                'jalon': jalon,
                'competences': toutes_competences,
                'nb_competences': toutes_competences.count(),
                'modules': modules,
            })
    
    # Organiser par classes
    classes_data = []
    if formation_selected:
        classes_query = Classe.objects.filter(
            formation=formation_selected,
            actif=True
        ).order_by('annee', 'nom')
        
        if classe_id:
            classes_query = classes_query.filter(pk=classe_id)
        
        for classe in classes_query:
            # Récupérer les compétences de cette classe
            competences_classe = Competence.objects.filter(classes=classe).distinct()
            
            # Récupérer les compétences via les cours de la classe
            cours_classe = Cours.objects.filter(classe=classe, actif=True)
            competences_cours = Competence.objects.filter(cours__in=cours_classe).distinct()
            
            # Combiner les compétences
            toutes_competences = (competences_classe | competences_cours).distinct()
            
            classes_data.append({
                'classe': classe,
                'competences': toutes_competences,
                'nb_competences': toutes_competences.count(),
                'nb_cours': cours_classe.count(),
            })
    
    # Les 7 compétences de base MFMC
    competences_base = Competence.objects.filter(
        libelle__in=['Expert médical', 'Communicateur', 'Collaborateur', 
                     'Promoteur de la santé', 'Gestionnaire', 'Érudit', 'Professionnel']
    )
    
    context = {
        'formation_selected': formation_selected,
        'jalons_data': jalons_data,
        'classes_data': classes_data,
        'competences_base': competences_base,
        'toutes_formations': Formation.objects.filter(actif=True).order_by('nom'),
        'formation_filtre': int(formation_id) if formation_id else None,
        'annee_filtre': int(annee) if annee else None,
        'classe_filtre': int(classe_id) if classe_id else None,
    }
    
    return render(request, 'administration/competences_par_jalon_classe.html', context)

