from django.contrib import admin

from .models import (
    DossierCandidature,
    ExamenProbatoire,
    EntretienIndividuel,
    DecisionAdmission,
    Inscription,
)


@admin.register(DossierCandidature)
class DossierCandidatureAdmin(admin.ModelAdmin):
    list_display = ('reference', 'candidat', 'formation', 'statut', 'date_depot')
    list_filter = ('formation', 'statut', 'date_depot')
    search_fields = ('reference', 'candidat__username', 'candidat__nom', 'candidat__prenom')
    ordering = ('-date_depot',)
    autocomplete_fields = ('candidat', 'formation')


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
    list_display = ('dossier', 'date_decision', 'decision', 'note_finale', 'confirmations_envoyees')
    list_filter = ('decision', 'date_decision')
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
