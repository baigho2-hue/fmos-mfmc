# core/urls.py
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core import views_administration
from core import views_lecons
from core import views_med6
from core import views_carnet_stage
from core import views_superviseur_stage
from core import views_2fa
from core import views_setup  # noqa: F401 - Vues temporaires pour la configuration Render
from django.urls import include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Pages principales
    path('', views.index, name='index'),
    path('accueil/', views.accueil, name='accueil'),
    path('activites/', views.activites, name='activites'),
    path('formations/', views.formations, name='formations'),
    # Routes spécifiques programme/ doivent être AVANT la route générale programme/
    # Gérer les deux cas : avec et sans slash final
    path('programme/desmfmc/', views.desmfmc_public, name='programme_desmfmc'),
    path('programme/desmfmc', views.desmfmc_public, name='programme_desmfmc_no_slash'),
    path('programme/sante-communautaire/', views.sante_communautaire_public, name='programme_sante_communautaire'),
    path('programme/sante-communautaire', views.sante_communautaire_public, name='programme_sante_communautaire_no_slash'),
    path('programme/recherche/', views.recherche_public, name='programme_recherche'),
    path('programme/recherche', views.recherche_public, name='programme_recherche_no_slash'),
    path('programme/logiciels-analyse/', views.logiciels_analyse_public, name='programme_logiciels_analyse'),
    path('programme/logiciels-analyse', views.logiciels_analyse_public, name='programme_logiciels_analyse_no_slash'),
    path('programme/echographie-base/', views.echographie_base_public, name='programme_echographie_base'),
    path('programme/echographie-base', views.echographie_base_public, name='programme_echographie_base_no_slash'),
    path('programme/pedagogie-sante/', views.pedagogie_sante_public, name='programme_pedagogie_sante'),
    path('programme/pedagogie-sante', views.pedagogie_sante_public, name='programme_pedagogie_sante_no_slash'),
    path('programme/', views.programmes, name='programmes'),
    path('cours/', views.cours, name='cours'),
    path('enseignants/', views.enseignants, name='enseignants'),
    path('etudiants/', views.etudiants, name='etudiants'),
    path('contact/', views.contact, name='contact'),
    path('inscription/', views.inscription, name='inscription'),
    
    # Messagerie interne
    path('messagerie/', include('apps.communications.urls')),
    path('login/', views.login_view, name='login'),
    path('login/med6/', views_med6.login_med6, name='login_med6'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/etudiant/', views.dashboard_etudiant, name='dashboard_etudiant'),
    path('dashboard/enseignant/', views.dashboard_enseignant, name='dashboard_enseignant'),
    path('etudiant/cours/', views.mes_cours, name='mes_cours'),
    path('etudiant/cours/<int:cours_id>/', views.detail_cours, name='detail_cours'),
    path('etudiant/progression/', views.ma_progression, name='ma_progression'),
    path('etudiant/planification/', views.ma_planification, name='ma_planification'),
    
    # Vues pour les leçons
    path('lecon/<int:lecon_id>/marquer-vue/', views_lecons.marquer_lecon_vue, name='marquer_lecon_vue'),
    path('lecon/<int:lecon_id>/commenter/', views_lecons.ajouter_commentaire_lecon, name='ajouter_commentaire_lecon'),
    path('quiz/<int:quiz_id>/passer/', views_lecons.passer_quiz, name='passer_quiz'),
    path('quiz/<int:quiz_id>/resultat/', views_lecons.resultat_quiz, name='resultat_quiz'),
    
    # Vues pour enseignants
    path('enseignant/cours/', views.mes_cours_enseignant, name='mes_cours_enseignant'),
    path('enseignant/cours/<int:cours_id>/modifier/', views.modifier_cours, name='modifier_cours'),
    path('enseignant/cours/<int:cours_id>/session/creer/', views.creer_session_cours, name='creer_session_cours'),
    path('enseignant/session-cours/<int:session_id>/', views.session_cours_detail, name='session_cours_detail'),
    path('enseignant/session-cours/<int:session_id>/demarrer/', views.demarrer_session_cours, name='demarrer_session_cours'),
    path('enseignant/evaluations/', views.mes_evaluations_enseignant, name='mes_evaluations_enseignant'),
    path('enseignant/evaluation/<int:evaluation_id>/session/creer/', views.creer_session_evaluation, name='creer_session_evaluation'),
    path('enseignant/session-evaluation/<int:session_id>/', views.session_evaluation_detail, name='session_evaluation_detail'),
    path('enseignant/session-evaluation/<int:session_id>/demarrer/', views.demarrer_session_evaluation, name='demarrer_session_evaluation'),
    
    # Vues pour étudiants
    path('etudiant/session-evaluation/<int:session_id>/rejoindre/', views.rejoindre_session_evaluation, name='rejoindre_session_evaluation'),
    
    # Programme DESMFMC structuré
    path('programme/desmfmc/complet/', views.programme_desmfmc_complet, name='programme_desmfmc_complet'),
    path('programme/jalon/<int:jalon_id>/', views.detail_jalon, name='detail_jalon'),
    path('etudiant/progression-programme/', views.ma_progression_programme, name='ma_progression_programme'),
    
    # Administration - Coordination DESMFMC
    path('administration/', views_administration.dashboard_administration, name='dashboard_administration'),
    path('administration/agenda/', views_administration.agenda_administration, name='agenda_administration'),
    path('administration/notes/', views_administration.notes_classes, name='notes_classes'),
    path('administration/notes/classe/<int:classe_id>/', views_administration.detail_notes_classe, name='detail_notes_classe'),
    path('administration/alertes/', views_administration.alertes_agenda, name='alertes_agenda'),
    path('administration/resultats/', views_administration.resultats_evaluations, name='resultats_evaluations'),
    path('administration/inscriptions/', views_administration.gestion_inscriptions, name='gestion_inscriptions'),
    path('administration/inscriptions/formation/<int:formation_id>/', views_administration.detail_inscriptions_formation, name='detail_inscriptions_formation'),
    path('administration/stages-cscom/', views_administration.gestion_stages_cscom, name='gestion_stages_cscom'),
    path('administration/stages-cscom/tirage/', views_administration.tirage_au_sort_stages, name='tirage_au_sort_stages'),
    path('administration/bulletins/classe/<int:classe_id>/', views_administration.bulletins_classe, name='bulletins_classe'),
    # Export PDF et Email
    path('administration/pdf/liste-etudiants/', views_administration.pdf_liste_etudiants, name='pdf_liste_etudiants'),
    path('administration/pdf/liste-etudiants/classe/<int:classe_id>/', views_administration.pdf_liste_etudiants, name='pdf_liste_etudiants_classe'),
    path('administration/pdf/stages/', views_administration.pdf_stages, name='pdf_stages'),
    path('administration/pdf/stages/annee/<int:annee>/', views_administration.pdf_stages, name='pdf_stages_annee'),
    path('administration/pdf/bulletins/classe/<int:classe_id>/', views_administration.pdf_bulletins, name='pdf_bulletins'),
    path('administration/pdf/lettre-information/<int:lettre_id>/', views_administration.pdf_lettre_information, name='pdf_lettre_information'),
    path('administration/pdf/lettres-informations/', views_administration.pdf_lettres_informations, name='pdf_lettres_informations'),
    path('administration/envoyer-pdf/', views_administration.envoyer_pdf_par_email, name='envoyer_pdf_par_email'),
    
    # Vues pour étudiants
    path('etudiant/bulletin/download/', views_administration.etudiant_download_bulletin, name='etudiant_download_bulletin'),
    path('etudiant/lettre/<int:lettre_id>/download/', views_administration.etudiant_download_lettre, name='etudiant_download_lettre'),
    
    # Vues pour enseignants
    path('enseignant/stages/download/', views_administration.enseignant_download_stages, name='enseignant_download_stages'),
    path('enseignant/stages/<int:annee>/download/', views_administration.enseignant_download_stages, name='enseignant_download_stages_annee'),
    path('enseignant/lettre/<int:lettre_id>/download/', views_administration.enseignant_download_lettre, name='enseignant_download_lettre'),
    path('enseignant/modeles-pedagogiques/', views_administration.enseignant_liste_modeles_pedagogiques, name='enseignant_liste_modeles_pedagogiques'),
    path('enseignant/modele-pedagogique/<int:modele_id>/download/', views_administration.enseignant_download_modele_pedagogique, name='enseignant_download_modele_pedagogique'),
    
    # Gestion signature coordination
    path('administration/signature-coordination/', views_administration.gestion_signature_coordination, name='gestion_signature_coordination'),
    
    # Upload cours et leçons
    path('administration/upload-cours-lecons/', views_administration.upload_cours_lecons, name='upload_cours_lecons'),
    path('administration/upload-cours/', views_administration.upload_cours, name='upload_cours'),
    path('administration/upload-lecon/', views_administration.upload_lecon, name='upload_lecon'),
    
    # API pour l'admin Django - Récupérer les cours d'une classe
    path('admin/utilisateurs/cours/get-cours-by-classe/', views_administration.get_cours_by_classe_json, name='get_cours_by_classe_json'),
    
    # Carnet de stage DESMFMC
    path('etudiant/carnet-stage/', views_carnet_stage.mon_carnet_stage, name='mon_carnet_stage'),
    path('etudiant/carnet-stage/evaluation/<int:evaluation_id>/', views_carnet_stage.detail_evaluation_stage, name='detail_evaluation_stage'),
    path('etudiant/carnet-stage/<int:carnet_id>/ajouter-evaluation/', views_carnet_stage.ajouter_evaluation_stage, name='ajouter_evaluation_stage'),
    path('etudiant/carnet-stage/evaluation/<int:evaluation_id>/modifier/', views_carnet_stage.modifier_evaluation_stage, name='modifier_evaluation_stage'),
    path('etudiant/carnet-stage/evaluation/<int:evaluation_id>/ajouter-competence/', views_carnet_stage.ajouter_evaluation_competence, name='ajouter_evaluation_competence'),
    path('etudiant/carnet-stage/tableau/<int:tableau_id>/', views_carnet_stage.tableau_evaluation_classe, name='tableau_evaluation_classe'),
    path('etudiant/carnet-stage/tableau/<int:tableau_id>/imprimer/', views_carnet_stage.imprimer_tableau_evaluation, name='imprimer_tableau_evaluation'),
    path('etudiant/carnet-stage/<int:carnet_id>/ajouter-tableau/', views_carnet_stage.ajouter_tableau_evaluation, name='ajouter_tableau_evaluation'),
    
    # Vues pour superviseurs/CEC
    path('superviseur/evaluations-stages/', views_superviseur_stage.liste_evaluations_superviseur, name='liste_evaluations_superviseur'),
    path('superviseur/evaluations-stages/<int:evaluation_id>/remplir/', views_superviseur_stage.remplir_evaluation_stage, name='remplir_evaluation_stage'),
    path('superviseur/evaluations-stages/<int:evaluation_id>/ajouter-competence/', views_superviseur_stage.ajouter_evaluation_competence_superviseur, name='ajouter_evaluation_competence_superviseur'),
    
    # Vues pour coordination - Évaluations de stages
    path('administration/evaluations-stages/', views_administration.evaluations_stages_coordination, name='evaluations_stages_coordination'),
    
    # Double authentification (2FA)
    path('2fa/activer/', views_2fa.activer_2fa, name='activer_2fa'),
    path('2fa/verifier/', views_2fa.verifier_code_2fa_view, name='verifier_code_2fa'),
    path('2fa/desactiver/', views_2fa.desactiver_2fa, name='desactiver_2fa'),
    path('2fa/verifier-session/', views_2fa.verifier_2fa_session, name='verifier_2fa_session'),
    
    # Gestion des enseignants
    path('administration/enseignants/', views_administration.gestion_enseignants, name='gestion_enseignants'),
    path('administration/enseignants/ajouter/', views_administration.ajouter_enseignant, name='ajouter_enseignant'),
    path('administration/enseignants/<int:enseignant_id>/', views_administration.detail_enseignant, name='detail_enseignant'),
    path('administration/enseignants/<int:enseignant_id>/modifier/', views_administration.modifier_enseignant, name='modifier_enseignant'),
    path('administration/enseignants/<int:enseignant_id>/assigner-cours/', views_administration.assigner_cours_enseignant, name='assigner_cours_enseignant'),
    
    # Inscription aux formations
    path('formations/inscrire/', views.inscription_formations, name='inscription_formations'),
    path('formations/inscrire/<str:formation_slug>/', views.inscription_formations, name='inscrire_formation'),
    path('formations/mes-formations/', views.mes_formations, name='mes_formations'),
    
    # ⚠️ VUES TEMPORAIRES POUR CONFIGURATION RENDER - À SUPPRIMER APRÈS CONFIGURATION
    # noqa: F401 - Code temporaire pour configuration initiale Render
    path('setup/', views_setup.setup_dashboard, name='setup_dashboard'),
    path('setup/migrate/', views_setup.setup_migrate, name='setup_migrate'),
    path('setup/create-superuser/', views_setup.setup_create_superuser, name='setup_create_superuser'),
    path('setup/init-programme/', views_setup.setup_init_programme, name='setup_init_programme'),
    path('setup/status/', views_setup.setup_status, name='setup_status'),
]

# Ajouter les vues de formation pour éviter les erreurs Reverse
formation_vues = [
    'desmfmc', 'sante_communautaire', 'recherche', 'echographie_base',
    'pedagogie_sante', 'autres_programmes',
    'logiciels_analyse_certif', 'logiciels_analyse_noncertif',
    'base_pedagogie', 'cours_med6', 'habilites_cliniques'
]

for vue in formation_vues:
    urlpatterns.append(path(f'formations/{vue}/', getattr(views, vue), name=vue))

# Servir les fichiers statiques et media en debug
if settings.DEBUG:
    # En développement, servir depuis STATICFILES_DIRS (dossier static)
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handlers d'erreurs
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
