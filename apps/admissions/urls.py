from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('suivi/', views.suivi_dossiers_formation, name='suivi_dossiers'),
    path('mes-dossiers/', views.mes_dossiers, name='mes_dossiers'),
    path('creer-dossier/', views.creer_dossier, name='creer_dossier'),
    path('dossier/<int:dossier_id>/', views.voir_dossier, name='voir_dossier'),
    path('dossier/<int:dossier_id>/upload-document/', views.uploader_document, name='uploader_document'),
    path('dossier/<int:dossier_id>/inscription/', views.inscription, name='inscription'),
    path('ajax/documents-requis/', views.ajax_documents_requis, name='ajax_documents_requis'),
    
    # Paiements annuels DESMFMC (années 2, 3, 4)
    path('paiements-annee-des/', views.paiements_annee_des, name='paiements_annee_des'),
    path('paiements-annee-des/<int:annee>/creer/', views.creer_paiement_annee_des, name='creer_paiement_annee_des'),
    path('validation-passage/<int:annee>/', views.validation_passage_annee, name='validation_passage_annee'),
]
