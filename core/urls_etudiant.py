# core/urls_etudiant.py
"""
URLs pour l'espace étudiant
"""
from django.urls import path
from core import views, views_paiements, views_administration

urlpatterns = [
    # Dashboard
    path('dashboard/etudiant/', views.dashboard_etudiant, name='dashboard_etudiant'),
    
    # Cours
    path('etudiant/cours/', views.mes_cours, name='mes_cours'),
    path('etudiant/cours/<int:cours_id>/', views.detail_cours, name='detail_cours'),
    
    # Progression
    path('etudiant/progression/', views.ma_progression, name='ma_progression'),
    path('etudiant/progression-programme/', views.ma_progression_programme, name='ma_progression_programme'),
    path('etudiant/planification/', views.ma_planification, name='ma_planification'),
    
    # Paiements
    path('etudiant/paiements/', views_paiements.mes_paiements, name='mes_paiements'),
    path('etudiant/paiements/creer/', views_paiements.creer_paiement, name='creer_paiement'),
    path('etudiant/paiements/<int:paiement_id>/', views_paiements.detail_paiement, name='detail_paiement'),
    path('etudiant/paiements/<int:paiement_id>/valider/', views_paiements.valider_paiement, name='valider_paiement'),
    path('etudiant/paiements/<int:paiement_id>/refuser/', views_paiements.refuser_paiement, name='refuser_paiement'),
    
    # Formations
    path('formations/inscrire/', views.inscription_formations, name='inscription_formations'),
    path('formations/inscrire/<str:formation_slug>/', views.inscription_formations, name='inscrire_formation'),
    path('formations/mes-formations/', views.mes_formations, name='mes_formations'),
    
    # Documents
    path('etudiant/bulletin/download/', views_administration.etudiant_download_bulletin, name='etudiant_download_bulletin'),
    path('etudiant/lettre/<int:lettre_id>/download/', views_administration.etudiant_download_lettre, name='etudiant_download_lettre'),
]

