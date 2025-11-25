from django.contrib import admin

from .models import (
    DossierCandidature,
    ExamenProbatoire,
    EntretienIndividuel,
    DecisionAdmission,
    Inscription,
    DocumentRequis,
    DocumentDossier,
    PaiementAnneeDES,
)


@admin.register(DossierCandidature)
class DossierCandidatureAdmin(admin.ModelAdmin):
    list_display = ('reference', 'candidat', 'formation', 'statut', 'date_depot', 'prise_en_charge_bourse')
    list_filter = ('formation', 'statut', 'date_depot', 'prise_en_charge_bourse')
    search_fields = ('reference', 'candidat__username', 'candidat__first_name', 'candidat__last_name')
    ordering = ('-date_depot',)
    autocomplete_fields = ('candidat', 'formation')
    readonly_fields = ('est_desmfmc',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('candidat', 'formation', 'reference', 'date_depot', 'statut', 'est_desmfmc')
        }),
        ('Informations spécifiques DESMFMC', {
            'fields': ('prise_en_charge_bourse', 'details_bourse'),
            'classes': ('collapse',)
        }),
        ('Observations', {
            'fields': ('observations', 'pieces_manquantes')
        }),
    )
    
    def est_desmfmc(self, obj):
        return obj.est_desmfmc() if obj.pk else False
    est_desmfmc.boolean = True
    est_desmfmc.short_description = "Formation DESMFMC"


@admin.register(ExamenProbatoire)
class ExamenProbatoireAdmin(admin.ModelAdmin):
    list_display = ('dossier', 'date_examen', 'note', 'seuil_reussite', 'reussi')
    list_filter = ('date_examen',)
    search_fields = ('dossier__reference', 'dossier__candidat__username')
    ordering = ('-date_examen',)
    readonly_fields = ('reussi',)

    def reussi(self, obj):
        return obj.reussi
    reussi.boolean = True
    reussi.short_description = "Réussi"


@admin.register(EntretienIndividuel)
class EntretienIndividuelAdmin(admin.ModelAdmin):
    list_display = ('dossier', 'date_entretien', 'score', 'seuil_reussite', 'reussi', 'evaluateur')
    list_filter = ('date_entretien',)
    search_fields = ('dossier__reference', 'dossier__candidat__username')
    ordering = ('-date_entretien',)
    autocomplete_fields = ('dossier', 'evaluateur')
    readonly_fields = ('reussi',)

    def reussi(self, obj):
        return obj.reussi
    reussi.boolean = True
    reussi.short_description = "Réussi"


@admin.register(DecisionAdmission)
class DecisionAdmissionAdmin(admin.ModelAdmin):
    list_display = ('dossier', 'date_decision', 'decision', 'note_finale', 'email_confirmation_envoye', 'date_envoi_email')
    list_filter = ('decision', 'date_decision', 'email_confirmation_envoye')
    search_fields = ('dossier__reference', 'dossier__candidat__username')
    ordering = ('-date_decision',)
    autocomplete_fields = ('dossier',)
    readonly_fields = ('note_finale',)


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'dossier', 'formation', 'statut', 
        'validee_par_coordination', 'validee_par_decanat', 
        'paiement_valide', 'montant_inscription', 'mode_paiement',
        'date_inscription'
    )
    list_filter = (
        'statut', 'formation', 
        'validee_par_coordination', 'validee_par_decanat', 
        'paiement_valide', 'mode_paiement',
        'date_inscription'
    )
    search_fields = (
        'dossier__reference', 'dossier__candidat__username',
        'dossier__candidat__first_name', 'dossier__candidat__last_name',
        'reference_paiement'
    )
    ordering = ('-date_inscription',)
    autocomplete_fields = ('dossier', 'decision_admission', 'formation', 'validateur_coordination', 'validateur_decanat', 'valideur_paiement')
    readonly_fields = ('statut', 'date_inscription', 'date_modification', 'est_certifiante', 'peut_payer', 'est_complete')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('dossier', 'decision_admission', 'formation', 'statut', 'est_certifiante', 'date_inscription', 'date_modification')
        }),
        ('Validation Coordination MFMC', {
            'fields': (
                'validee_par_coordination', 
                'date_validation_coordination', 
                'validateur_coordination'
            )
        }),
        ('Validation Décanat', {
            'fields': (
                'validee_par_decanat', 
                'date_validation_decanat', 
                'validateur_decanat'
            )
        }),
        ('Commentaires de validation', {
            'fields': ('commentaires_validation',)
        }),
        ('Paiement (uniquement pour formations certifiantes)', {
            'fields': (
                'montant_inscription', 
                'mode_paiement', 
                'paiement_valide',
                'date_paiement',
                'reference_paiement',
                'preuve_paiement',
                'valideur_paiement',
                'date_validation_paiement',
                'commentaires_paiement',
            ),
            'description': 'Les champs de paiement ne sont utilisés que pour les formations certifiantes. Pour les autres formations, seule la validation administrative est requise.'
        }),
        ('Informations complémentaires', {
            'fields': ('notes', 'peut_payer', 'est_complete'),
            'classes': ('collapse',)
        }),
    )
    
    def peut_payer(self, obj):
        return obj.peut_payer
    peut_payer.boolean = True
    peut_payer.short_description = "Peut payer"
    
    def est_certifiante(self, obj):
        return obj.est_certifiante
    est_certifiante.boolean = True
    est_certifiante.short_description = "Formation certifiante"
    
    def est_complete(self, obj):
        return obj.est_complete
    est_complete.boolean = True
    est_complete.short_description = "Inscription complète"


@admin.register(DocumentRequis)
class DocumentRequisAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_formation', 'obligatoire', 'ordre', 'actif')
    list_filter = ('type_formation', 'obligatoire', 'actif')
    search_fields = ('nom', 'description')
    ordering = ('type_formation', 'ordre', 'nom')
    list_editable = ('ordre', 'actif', 'obligatoire')


@admin.register(DocumentDossier)
class DocumentDossierAdmin(admin.ModelAdmin):
    list_display = ('dossier', 'document_requis', 'date_upload', 'valide', 'valide_par')
    list_filter = ('valide', 'date_upload', 'document_requis__type_formation')
    search_fields = ('dossier__reference', 'document_requis__nom')
    ordering = ('-date_upload',)
    autocomplete_fields = ('dossier', 'document_requis', 'valide_par')
    readonly_fields = ('date_upload',)


@admin.register(PaiementAnneeDES)
class PaiementAnneeDESAdmin(admin.ModelAdmin):
    list_display = (
        'etudiant', 'formation', 'annee', 'montant', 'statut', 
        'mode_paiement', 'date_paiement', 'valide_par', 'date_validation'
    )
    list_filter = ('formation', 'annee', 'statut', 'mode_paiement', 'date_creation')
    search_fields = (
        'etudiant__username', 'etudiant__first_name', 'etudiant__last_name',
        'reference_paiement'
    )
    ordering = ('-date_creation',)
    autocomplete_fields = ('etudiant', 'formation', 'valide_par')
    readonly_fields = ('date_creation', 'date_modification', 'paiement_valide', 'peut_valider_passage')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('etudiant', 'formation', 'annee', 'resultat_annee', 'statut')
        }),
        ('Paiement', {
            'fields': (
                'montant', 'mode_paiement', 'reference_paiement',
                'preuve_paiement', 'date_paiement'
            )
        }),
        ('Validation', {
            'fields': (
                'valide_par', 'date_validation', 'commentaires',
                'paiement_valide', 'peut_valider_passage'
            )
        }),
        ('Informations complémentaires', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def paiement_valide(self, obj):
        return obj.paiement_valide
    paiement_valide.boolean = True
    paiement_valide.short_description = "Paiement validé"
    
    def peut_valider_passage(self, obj):
        return obj.peut_valider_passage() if obj.pk else False
    peut_valider_passage.boolean = True
    peut_valider_passage.short_description = "Peut valider passage"
