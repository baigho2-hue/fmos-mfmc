# core/urls_enseignant.py
"""
URLs pour l'espace enseignant
"""
from django.urls import path
from core import views, views_enseignant, views_administration

urlpatterns = [
    # Dashboard
    path('dashboard/enseignant/', views.dashboard_enseignant, name='dashboard_enseignant'),
    
    # Cours
    path('enseignant/cours/', views.mes_cours_enseignant, name='mes_cours_enseignant'),
    path('enseignant/cours/<int:cours_id>/modifier/', views.modifier_cours, name='modifier_cours'),
    path('enseignant/cours/<int:cours_id>/lecon/ajouter/', views_enseignant.ajouter_lecon, name='ajouter_lecon'),
    path('enseignant/cours/<int:cours_id>/lecon/<int:lecon_id>/modifier/', views_enseignant.modifier_lecon, name='modifier_lecon'),
    path('enseignant/cours/<int:cours_id>/lecon/<int:lecon_id>/supprimer/', views_enseignant.supprimer_lecon, name='supprimer_lecon'),
    path('enseignant/cours/<int:cours_id>/session/creer/', views.creer_session_cours, name='creer_session_cours'),
    path('enseignant/session-cours/<int:session_id>/', views.session_cours_detail, name='session_cours_detail'),
    path('enseignant/session-cours/<int:session_id>/demarrer/', views.demarrer_session_cours, name='demarrer_session_cours'),
    
    # Évaluations
    path('enseignant/evaluations/', views.mes_evaluations_enseignant, name='mes_evaluations_enseignant'),
    path('enseignant/evaluation/<int:evaluation_id>/session/creer/', views.creer_session_evaluation, name='creer_session_evaluation'),
    path('enseignant/session-evaluation/<int:session_id>/', views.session_evaluation_detail, name='session_evaluation_detail'),
    path('enseignant/session-evaluation/<int:session_id>/demarrer/', views.demarrer_session_evaluation, name='demarrer_session_evaluation'),
    
    # Upload cours/leçons
    path('enseignant/upload-cours-lecons/', views_enseignant.upload_cours_lecons_enseignant, name='upload_cours_lecons_enseignant'),
    path('enseignant/upload-cours/', views_enseignant.upload_cours_enseignant, name='upload_cours_enseignant'),
    path('enseignant/upload-lecon/', views_enseignant.upload_lecon_enseignant, name='upload_lecon_enseignant'),
    
    # Documents
    path('enseignant/stages/download/', views_administration.enseignant_download_stages, name='enseignant_download_stages'),
    path('enseignant/stages/<int:annee>/download/', views_administration.enseignant_download_stages, name='enseignant_download_stages_annee'),
    path('enseignant/lettre/<int:lettre_id>/download/', views_administration.enseignant_download_lettre, name='enseignant_download_lettre'),
    path('enseignant/modeles-pedagogiques/', views_administration.enseignant_liste_modeles_pedagogiques, name='enseignant_liste_modeles_pedagogiques'),
    path('enseignant/modele-pedagogique/<int:modele_id>/download/', views_administration.enseignant_download_modele_pedagogique, name='enseignant_download_modele_pedagogique'),
]

