# apps/evaluations/urls_stage.py
"""
URLs pour les évaluations de stage basées sur les jalons
"""
from django.urls import path
from . import views_stage

app_name = 'evaluations_stage'

urlpatterns = [
    # Vues enseignants
    path('enseignant/liste/', views_stage.liste_evaluations_stage, name='liste_evaluations_stage'),
    path('enseignant/creer/', views_stage.creer_evaluation_stage, name='creer_evaluation_stage'),
    path('enseignant/modifier/<int:evaluation_id>/', views_stage.modifier_evaluation_stage, name='modifier_evaluation_stage'),
    path('enseignant/supprimer/<int:evaluation_id>/', views_stage.supprimer_evaluation_stage, name='supprimer_evaluation_stage'),
    path('enseignant/grille-vierge/<int:classe_id>/pdf/', views_stage.telecharger_grille_vierge_pdf, name='telecharger_grille_vierge_pdf'),
    
    # Vues coordination
    path('coordination/liste/', views_stage.liste_evaluations_a_verifier, name='liste_evaluations_a_verifier'),
    path('coordination/verifier/<int:evaluation_id>/', views_stage.verifier_evaluation_stage, name='verifier_evaluation_stage'),
    
    # Vues étudiants
    path('etudiant/mes-evaluations/', views_stage.mes_evaluations_stage_etudiant, name='mes_evaluations_stage_etudiant'),
    path('etudiant/detail/<int:evaluation_id>/', views_stage.detail_evaluation_stage_etudiant, name='detail_evaluation_stage_etudiant'),
    
    # Téléchargement PDF
    path('pdf/<int:evaluation_id>/', views_stage.telecharger_evaluation_stage_pdf, name='telecharger_evaluation_stage_pdf'),
    
    # APIs AJAX
    path('api/etudiants-classe/', views_stage.get_etudiants_classe, name='get_etudiants_classe'),
    path('api/stages-etudiant/', views_stage.get_stages_etudiant, name='get_stages_etudiant'),
]

