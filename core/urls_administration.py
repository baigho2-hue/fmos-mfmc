# core/urls_administration.py
"""
URLs pour l'administration (coordination DESMFMC)
"""
from django.urls import path
from core import views_administration

urlpatterns = [
    # Dashboard
    path('administration/', views_administration.dashboard_administration, name='dashboard_administration'),
    
    # Planning & Agenda
    path('administration/agenda/', views_administration.agenda_administration, name='agenda_administration'),
    path('administration/alertes/', views_administration.alertes_agenda, name='alertes_agenda'),
    
    # Gestion des personnes
    path('administration/enseignants/', views_administration.gestion_enseignants, name='gestion_enseignants'),
    path('administration/enseignants/ajouter/', views_administration.ajouter_enseignant, name='ajouter_enseignant'),
    path('administration/enseignants/<int:enseignant_id>/', views_administration.detail_enseignant, name='detail_enseignant'),
    path('administration/enseignants/<int:enseignant_id>/modifier/', views_administration.modifier_enseignant, name='modifier_enseignant'),
    path('administration/enseignants/<int:enseignant_id>/assigner-cours/', views_administration.assigner_cours_enseignant, name='assigner_cours_enseignant'),
    path('administration/inscriptions/', views_administration.gestion_inscriptions, name='gestion_inscriptions'),
    path('administration/inscriptions/formation/<int:formation_id>/', views_administration.detail_inscriptions_formation, name='detail_inscriptions_formation'),
    path('administration/etudiants/', views_administration.liste_etudiants_par_formation, name='liste_etudiants_par_formation'),
    
    # Pédagogie & Évaluations
    path('administration/notes/', views_administration.notes_classes, name='notes_classes'),
    path('administration/notes/classe/<int:classe_id>/', views_administration.detail_notes_classe, name='detail_notes_classe'),
    path('administration/resultats/', views_administration.resultats_evaluations, name='resultats_evaluations'),
    path('administration/competences/', views_administration.competences_par_jalon_classe, name='competences_par_jalon_classe'),
    path('administration/upload-cours-lecons/', views_administration.upload_cours_lecons, name='upload_cours_lecons'),
    path('administration/upload-cours/', views_administration.upload_cours, name='upload_cours'),
    path('administration/upload-lecon/', views_administration.upload_lecon, name='upload_lecon'),
    
    # Stages & Évaluations
    path('administration/stages-cscom/', views_administration.gestion_stages_cscom, name='gestion_stages_cscom'),
    path('administration/stages-cscom/tirage/', views_administration.tirage_au_sort_stages, name='tirage_au_sort_stages'),
    path('administration/evaluations-stages/', views_administration.evaluations_stages_coordination, name='evaluations_stages_coordination'),
    
    # Configuration
    path('administration/signature-coordination/', views_administration.gestion_signature_coordination, name='gestion_signature_coordination'),
    
    # PDF et Email
    path('administration/pdf/liste-etudiants/', views_administration.pdf_liste_etudiants, name='pdf_liste_etudiants'),
    path('administration/pdf/liste-etudiants/classe/<int:classe_id>/', views_administration.pdf_liste_etudiants, name='pdf_liste_etudiants_classe'),
    path('administration/pdf/stages/', views_administration.pdf_stages, name='pdf_stages'),
    path('administration/pdf/stages/annee/<int:annee>/', views_administration.pdf_stages, name='pdf_stages_annee'),
    path('administration/pdf/bulletins/classe/<int:classe_id>/', views_administration.pdf_bulletins, name='pdf_bulletins'),
    path('administration/pdf/lettre-information/<int:lettre_id>/', views_administration.pdf_lettre_information, name='pdf_lettre_information'),
    path('administration/pdf/lettres-informations/', views_administration.pdf_lettres_informations, name='pdf_lettres_informations'),
    path('administration/envoyer-pdf/', views_administration.envoyer_pdf_par_email, name='envoyer_pdf_par_email'),
    
    # API pour l'admin Django
    path('admin/utilisateurs/cours/get-cours-by-classe/', views_administration.get_cours_by_classe_json, name='get_cours_by_classe_json'),
]

