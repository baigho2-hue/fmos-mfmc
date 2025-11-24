from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
    path('mes-dossiers/', views.mes_dossiers, name='mes_dossiers'),
    path('creer-dossier/', views.creer_dossier, name='creer_dossier'),
    path('dossier/<int:dossier_id>/', views.voir_dossier, name='voir_dossier'),
    path('dossier/<int:dossier_id>/upload-document/', views.uploader_document, name='uploader_document'),
    path('dossier/<int:dossier_id>/inscription/', views.inscription, name='inscription'),
    path('ajax/documents-requis/', views.ajax_documents_requis, name='ajax_documents_requis'),
]
