# core/urls_modules.py
"""
URLs pour les modules (apps) et fonctionnalités spécialisées
"""
from django.urls import path, include
from core import views, views_lecons, views_carnet_stage, views_superviseur_stage

urlpatterns = [
    # Messagerie interne
    path('messagerie/', include('apps.communications.urls')),
    
    # Admissions
    path('admissions/', include('apps.admissions.urls')),
    
    # Évaluations
    path('evaluations/stage/', include('apps.evaluations.urls_stage')),
    path('evaluations/grilles/', include('apps.evaluations.urls_grilles')),
    
    # Leçons et quiz
    path('lecon/<int:lecon_id>/marquer-vue/', views_lecons.marquer_lecon_vue, name='marquer_lecon_vue'),
    path('lecon/<int:lecon_id>/commenter/', views_lecons.ajouter_commentaire_lecon, name='ajouter_commentaire_lecon'),
    path('quiz/<int:quiz_id>/passer/', views_lecons.passer_quiz, name='passer_quiz'),
    path('quiz/<int:quiz_id>/resultat/', views_lecons.resultat_quiz, name='resultat_quiz'),
    
    # Sessions d'évaluation
    path('etudiant/session-evaluation/<int:session_id>/rejoindre/', views.rejoindre_session_evaluation, name='rejoindre_session_evaluation'),
    
    # Carnet de stage
    path('etudiant/carnet-stage/', views_carnet_stage.mon_carnet_stage, name='mon_carnet_stage'),
    path('etudiant/carnet-stage/evaluation/<int:evaluation_id>/', views_carnet_stage.detail_evaluation_stage, name='detail_evaluation_stage'),
    path('etudiant/carnet-stage/<int:carnet_id>/ajouter-evaluation/', views_carnet_stage.ajouter_evaluation_stage, name='ajouter_evaluation_stage'),
    path('etudiant/carnet-stage/evaluation/<int:evaluation_id>/modifier/', views_carnet_stage.modifier_evaluation_stage, name='modifier_evaluation_stage'),
    path('etudiant/carnet-stage/evaluation/<int:evaluation_id>/ajouter-competence/', views_carnet_stage.ajouter_evaluation_competence, name='ajouter_evaluation_competence'),
    path('etudiant/carnet-stage/tableau/<int:tableau_id>/', views_carnet_stage.tableau_evaluation_classe, name='tableau_evaluation_classe'),
    path('etudiant/carnet-stage/tableau/<int:tableau_id>/imprimer/', views_carnet_stage.imprimer_tableau_evaluation, name='imprimer_tableau_evaluation'),
    path('etudiant/carnet-stage/<int:carnet_id>/ajouter-tableau/', views_carnet_stage.ajouter_tableau_evaluation, name='ajouter_tableau_evaluation'),
    
    # Superviseur/CEC
    path('superviseur/evaluations-stages/', views_superviseur_stage.liste_evaluations_superviseur, name='liste_evaluations_superviseur'),
    path('superviseur/evaluations-stages/<int:evaluation_id>/remplir/', views_superviseur_stage.remplir_evaluation_stage, name='remplir_evaluation_stage'),
    path('superviseur/evaluations-stages/<int:evaluation_id>/ajouter-competence/', views_superviseur_stage.ajouter_evaluation_competence_superviseur, name='ajouter_evaluation_competence_superviseur'),
]

