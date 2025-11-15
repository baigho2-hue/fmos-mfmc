# apps/utilisateurs/admin_carnet_stage.py
"""
Configuration admin pour le carnet de stage
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models_carnet_stage import (
    CarnetStage, EvaluationStage, EvaluationCompetence,
    TableauEvaluationClasse, EvaluationCompetenceTableau,
    ProclamationResultats
)


class EvaluationCompetenceInline(admin.TabularInline):
    """Inline pour les évaluations de compétences dans une évaluation de stage"""
    model = EvaluationCompetence
    extra = 0
    fields = ('competence', 'jalon', 'niveau_acquisition', 'commentaire', 'date_evaluation')
    readonly_fields = ('date_evaluation',)


@admin.register(CarnetStage)
class CarnetStageAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'annee_scolaire', 'nombre_stages', 'stages_valides', 'actif', 'date_creation')
    list_filter = ('actif', 'annee_scolaire', 'date_creation')
    search_fields = ('etudiant__username', 'etudiant__email', 'etudiant__first_name', 'etudiant__last_name', 'annee_scolaire')
    readonly_fields = ('date_creation', 'date_modification')
    inlines = []
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('etudiant', 'annee_scolaire', 'actif')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification')
        }),
    )
    
    def nombre_stages(self, obj):
        return obj.evaluations_stages.count()
    nombre_stages.short_description = 'Nombre de stages'
    
    def stages_valides(self, obj):
        return obj.evaluations_stages.filter(valide=True).count()
    stages_valides.short_description = 'Stages validés'


@admin.register(EvaluationStage)
class EvaluationStageAdmin(admin.ModelAdmin):
    list_display = ('carnet', 'annee', 'type_stage', 'lieu_stage', 'date_debut', 'date_fin', 'note_globale', 'valide', 'date_creation')
    list_filter = ('annee', 'type_stage', 'valide', 'date_debut', 'date_creation')
    search_fields = ('carnet__etudiant__username', 'lieu_stage', 'service_stage', 'maitre_stage_nom')
    readonly_fields = ('date_creation', 'date_modification')
    inlines = [EvaluationCompetenceInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('carnet', 'annee', 'type_stage', 'stage_annee1', 'stage_rotation')
        }),
        ('Informations du stage', {
            'fields': ('lieu_stage', 'service_stage', 'date_debut', 'date_fin', 'duree_semaines')
        }),
        ('Maître de stage', {
            'fields': ('maitre_stage', 'maitre_stage_nom', 'maitre_stage_titre')
        }),
        ('Évaluation', {
            'fields': ('note_globale', 'appreciation_globale', 'points_forts', 'points_amelioration')
        }),
        ('Validation', {
            'fields': ('valide', 'date_validation', 'valide_par')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification')
        }),
    )


@admin.register(EvaluationCompetence)
class EvaluationCompetenceAdmin(admin.ModelAdmin):
    list_display = ('evaluation_stage', 'competence', 'jalon', 'niveau_acquisition', 'date_evaluation')
    list_filter = ('niveau_acquisition', 'jalon', 'evalue_par_maitre', 'date_evaluation')
    search_fields = ('competence__libelle', 'evaluation_stage__lieu_stage')
    readonly_fields = ('date_evaluation',)


class EvaluationCompetenceTableauInline(admin.TabularInline):
    """Inline pour les évaluations de compétences dans un tableau"""
    model = EvaluationCompetenceTableau
    extra = 0
    fields = ('competence', 'niveau_acquisition', 'commentaire', 'date_evaluation')
    readonly_fields = ('date_evaluation',)


@admin.register(TableauEvaluationClasse)
class TableauEvaluationClasseAdmin(admin.ModelAdmin):
    list_display = ('carnet', 'classe', 'jalon', 'annee', 'nombre_competences', 'date_creation')
    list_filter = ('annee', 'classe', 'jalon', 'date_creation')
    search_fields = ('carnet__etudiant__username', 'classe__nom')
    readonly_fields = ('date_creation', 'date_modification')
    inlines = [EvaluationCompetenceTableauInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('carnet', 'classe', 'jalon', 'annee')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification')
        }),
    )
    
    def nombre_competences(self, obj):
        return obj.evaluations_competences_tableau.count()
    nombre_competences.short_description = 'Nombre de compétences'


@admin.register(EvaluationCompetenceTableau)
class EvaluationCompetenceTableauAdmin(admin.ModelAdmin):
    list_display = ('tableau', 'competence', 'niveau_acquisition', 'date_evaluation')
    list_filter = ('niveau_acquisition', 'date_evaluation', 'tableau__annee', 'tableau__classe')
    search_fields = ('competence__libelle', 'tableau__carnet__etudiant__username')
    readonly_fields = ('date_evaluation',)


@admin.register(ProclamationResultats)
class ProclamationResultatsAdmin(admin.ModelAdmin):
    list_display = ('classe', 'annee_scolaire', 'date_proclamation', 'proclame_par', 'actif', 'date_creation')
    list_filter = ('actif', 'annee_scolaire', 'date_proclamation', 'classe')
    search_fields = ('classe__nom', 'annee_scolaire', 'proclame_par__username')
    readonly_fields = ('date_creation', 'date_modification')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('classe', 'annee_scolaire', 'date_proclamation', 'proclame_par', 'actif')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification')
        }),
    )

