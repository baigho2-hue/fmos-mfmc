# core/context_processors.py
"""
Context processors pour rendre des variables disponibles dans tous les templates
"""
from django.urls import reverse


def navigation_menu(request):
    """
    Génère le menu de navigation en fonction du type d'utilisateur
    """
    user = request.user if hasattr(request, 'user') else None
    
    menu_items = []
    
    # Menu pour utilisateurs non authentifiés
    if not user or not user.is_authenticated:
        menu_items = [
            {
                'title': 'Accueil',
                'url': reverse('accueil'),
                'icon': '🏠',
                'active': request.resolver_match.url_name == 'accueil' if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Activités',
                'url': reverse('activites'),
                'icon': '📋',
                'active': request.resolver_match.url_name == 'activites' if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Formations',
                'url': reverse('formations'),
                'icon': '🎓',
                'submenu': [
                    {
                        'title': 'Certifiantes',
                        'items': [
                            {'title': 'DESMFMC', 'url': reverse('programme_desmfmc')},
                            {'title': 'Santé Communautaire', 'url': reverse('programme_sante_communautaire')},
                            {'title': 'Recherche', 'url': reverse('programme_recherche')},
                            {'title': 'Logiciels d\'analyse', 'url': reverse('programme_logiciels_analyse')},
                            {'title': 'Échographie de base', 'url': reverse('programme_echographie_base')},
                            {'title': 'Pédagogie en santé', 'url': reverse('programme_pedagogie_sante')},
                        ]
                    },
                    {
                        'title': 'Non Certifiantes',
                        'items': [
                            {'title': 'Cours Médecine 6', 'url': reverse('cours_med6')},
                            {'title': 'Habilités Cliniques', 'url': reverse('habilites_cliniques')},
                            {'title': 'Logiciels d\'analyse', 'url': reverse('logiciels_analyse_noncertif')},
                            {'title': 'Base en pédagogie', 'url': reverse('base_pedagogie')},
                            {'title': 'Autres', 'url': reverse('autres_programmes')},
                        ]
                    }
                ],
                'active': request.resolver_match.url_name in ['formations', 'programme_desmfmc', 'programme_sante_communautaire'] if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Programmes',
                'url': reverse('programmes'),
                'icon': '📚',
                'submenu': [
                    {'title': 'Programme DES', 'url': reverse('programme_desmfmc')},
                    {'title': 'Programme Santé Communautaire', 'url': reverse('programme_sante_communautaire')},
                    {'title': 'Programme Recherche', 'url': reverse('programme_recherche')},
                    {'title': 'Programme Logiciels d\'Analyse', 'url': reverse('programme_logiciels_analyse')},
                    {'title': 'Programme Pédagogie', 'url': reverse('programme_pedagogie_sante')},
                ],
                'active': request.resolver_match.url_name == 'programmes' if hasattr(request, 'resolver_match') else False
            },
        ]
    
    # Menu pour étudiants
    elif user.is_authenticated and hasattr(user, 'est_etudiant') and user.est_etudiant():
        menu_items = [
            {
                'title': 'Mon Espace',
                'url': reverse('dashboard_etudiant'),
                'icon': '🏠',
                'active': request.resolver_match.url_name == 'dashboard_etudiant' if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Mes Cours',
                'url': reverse('mes_cours'),
                'icon': '📖',
                'active': request.resolver_match.url_name in ['mes_cours', 'detail_cours'] if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Mes Formations',
                'url': reverse('mes_formations'),
                'icon': '🎓',
                'active': request.resolver_match.url_name == 'mes_formations' if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Mon Progression',
                'url': reverse('ma_progression'),
                'icon': '📊',
                'submenu': [
                    {'title': 'Progression générale', 'url': reverse('ma_progression')},
                    {'title': 'Progression programme', 'url': reverse('ma_progression_programme')},
                    {'title': 'Planification', 'url': reverse('ma_planification')},
                ],
                'active': request.resolver_match.url_name in ['ma_progression', 'ma_progression_programme', 'ma_planification'] if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Carnet de Stage',
                'url': reverse('mon_carnet_stage'),
                'icon': '📝',
                'active': request.resolver_match.url_name in ['mon_carnet_stage', 'detail_evaluation_stage'] if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Messagerie',
                'url': reverse('communications:messagerie_liste'),
                'icon': '💬',
                'active': 'messagerie' in request.resolver_match.url_name if hasattr(request, 'resolver_match') else False
            },
        ]
    
    # Menu pour enseignants
    elif user.is_authenticated and hasattr(user, 'est_enseignant') and user.est_enseignant():
        menu_items = [
            {
                'title': 'Tableau de bord',
                'url': reverse('dashboard_enseignant'),
                'icon': '🏠',
                'active': request.resolver_match.url_name == 'dashboard_enseignant' if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Mes Cours',
                'url': reverse('mes_cours_enseignant'),
                'icon': '📚',
                'submenu': [
                    {'title': 'Liste des cours', 'url': reverse('mes_cours_enseignant')},
                    {'title': 'Mes évaluations', 'url': reverse('mes_evaluations_enseignant')},
                ],
                'active': request.resolver_match.url_name in ['mes_cours_enseignant', 'modifier_cours', 'mes_evaluations_enseignant'] if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Grilles d\'évaluation',
                'url': reverse('grilles:liste'),
                'icon': '📋',
                'submenu': [
                    {'title': 'Liste des grilles', 'url': reverse('grilles:liste')},
                    {'title': 'Créer une grille', 'url': reverse('grilles:creer')},
                    {'title': 'Importer depuis Word', 'url': reverse('grilles:import_word')},
                ],
                'active': 'grilles' in request.resolver_match.url_name if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Évaluations de Stage',
                'url': reverse('evaluations_stage:liste_evaluations_stage'),
                'icon': '📝',
                'active': 'evaluations_stage' in request.resolver_match.url_name if hasattr(request, 'resolver_match') else False
            },
            {
                'title': 'Messagerie',
                'url': reverse('communications:messagerie_liste'),
                'icon': '💬',
                'active': 'messagerie' in request.resolver_match.url_name if hasattr(request, 'resolver_match') else False
            },
        ]
        
        # Ajouter menu superviseur si applicable
        if hasattr(user, 'est_superviseur_cec') and user.est_superviseur_cec():
            menu_items.append({
                'title': 'Supervision',
                'url': reverse('liste_evaluations_superviseur'),
                'icon': '👨‍⚕️',
                'active': 'superviseur' in request.resolver_match.url_name if hasattr(request, 'resolver_match') else False
            })
    
    # Menu pour coordination
    if user and user.is_authenticated and hasattr(user, 'est_membre_coordination') and user.est_membre_coordination():
        menu_items.append({
            'title': 'Administration',
            'url': reverse('dashboard_administration'),
            'icon': '⚙️',
            'submenu': [
                {
                    'title': 'Tableau de bord',
                    'url': reverse('dashboard_administration'),
                    'icon': '📊'
                },
                {
                    'title': 'Planning & Agenda',
                    'items': [
                        {'title': 'Agenda', 'url': reverse('agenda_administration')},
                        {'title': 'Alertes', 'url': reverse('alertes_agenda')},
                    ]
                },
                {
                    'title': 'Gestion des personnes',
                    'items': [
                        {'title': 'Gestion enseignants', 'url': reverse('gestion_enseignants')},
                        {'title': 'Gestion inscriptions', 'url': reverse('gestion_inscriptions')},
                        {'title': 'Liste étudiants', 'url': reverse('liste_etudiants_par_formation')},
                    ]
                },
                {
                    'title': 'Pédagogie & Évaluations',
                    'items': [
                        {'title': 'Notes des classes', 'url': reverse('notes_classes')},
                        {'title': 'Résultats évaluations', 'url': reverse('resultats_evaluations')},
                        {'title': 'Grilles d\'évaluation', 'url': reverse('grilles:liste')},
                        {'title': 'Téléverser cours/leçons', 'url': reverse('upload_cours_lecons')},
                    ]
                },
                {
                    'title': 'Stages & Évaluations',
                    'items': [
                        {'title': 'Stages CSCom-U', 'url': reverse('gestion_stages_cscom')},
                        {'title': 'Évaluations de stages', 'url': reverse('evaluations_stages_coordination')},
                    ]
                },
                {
                    'title': 'Configuration',
                    'items': [
                        {'title': 'Signature coordination', 'url': reverse('gestion_signature_coordination')},
                        {'title': 'Admin Django', 'url': reverse('admin:index'), 'external': True},
                    ]
                },
            ],
            'active': 'administration' in request.resolver_match.url_name if hasattr(request, 'resolver_match') else False
        })
    
    return {
        'navigation_menu': menu_items,
        'current_url': request.resolver_match.url_name if hasattr(request, 'resolver_match') else None,
    }

