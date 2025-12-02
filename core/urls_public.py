# core/urls_public.py
"""
URLs pour les pages publiques
"""
from django.urls import path
from core import views

urlpatterns = [
    # Pages principales
    path('', views.index, name='index'),
    path('accueil/', views.accueil, name='accueil'),
    path('activites/', views.activites, name='activites'),
    path('formations/', views.formations, name='formations'),
    path('cours/', views.cours, name='cours'),
    path('enseignants/', views.enseignants, name='enseignants'),
    path('etudiants/', views.etudiants, name='etudiants'),
    path('contact/', views.contact, name='contact'),
    path('inscription/', views.inscription, name='inscription'),
    
    # Programmes (routes spécifiques AVANT la route générale)
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
    
    # Programme DESMFMC structuré
    path('programme/desmfmc/complet/', views.programme_desmfmc_complet, name='programme_desmfmc_complet'),
    path('programme/jalon/<int:jalon_id>/', views.detail_jalon, name='detail_jalon'),
]

