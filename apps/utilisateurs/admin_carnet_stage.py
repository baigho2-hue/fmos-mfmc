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
    """
    Admin pour les évaluations de compétences dans les tableaux d'évaluation par classe.
    
    Ce modèle lie une compétence à un tableau d'évaluation (TableauEvaluationClasse)
    et stocke le niveau d'acquisition de cette compétence pour un étudiant donné.
    
    Utilisé dans le système de carnet de stage pour suivre l'acquisition des compétences
    par classe et par année du DESMFMC.
    """
    list_display = (
        'get_tableau_info', 
        'get_etudiant_info',
        'competence', 
        'get_niveau_display', 
        'date_evaluation',
        'get_classe_info'
    )
    list_filter = (
        'niveau_acquisition', 
        'date_evaluation', 
        'tableau__annee', 
        'tableau__classe',
        'tableau__carnet__etudiant'
    )
    search_fields = (
        'competence__libelle', 
        'competence__description',
        'tableau__carnet__etudiant__username',
        'tableau__carnet__etudiant__first_name',
        'tableau__carnet__etudiant__last_name',
        'tableau__classe__nom',
        'commentaire'
    )
    readonly_fields = ('date_evaluation',)
    date_hierarchy = 'date_evaluation'
    list_per_page = 50
    
    fieldsets = (
        ('📋 Contexte d\'évaluation', {
            'fields': ('tableau', 'competence'),
            'description': 'Le tableau d\'évaluation et la compétence évaluée. '
                          'Le tableau est lié à un carnet de stage, une classe et une année du DES.'
        }),
        ('📊 Résultat d\'évaluation', {
            'fields': ('niveau_acquisition', 'commentaire', 'date_evaluation'),
            'description': 'Niveau d\'acquisition de la compétence (1=Non acquis, 2=En cours, 3=Acquis, 4=Maîtrisé)'
        }),
    )
    
    def get_tableau_info(self, obj):
        """Affiche les informations du tableau d'évaluation"""
        if obj.tableau:
            return f"{obj.tableau.classe.nom} - Année {obj.tableau.annee}"
        return "-"
    get_tableau_info.short_description = "Tableau d'évaluation"
    get_tableau_info.admin_order_field = 'tableau__classe__nom'
    
    def get_etudiant_info(self, obj):
        """Affiche les informations de l'étudiant"""
        if obj.tableau and obj.tableau.carnet and obj.tableau.carnet.etudiant:
            etudiant = obj.tableau.carnet.etudiant
            nom_complet = f"{etudiant.first_name} {etudiant.last_name}".strip()
            return nom_complet or etudiant.username
        return "-"
    get_etudiant_info.short_description = "Étudiant"
    get_etudiant_info.admin_order_field = 'tableau__carnet__etudiant__last_name'
    
    def get_niveau_display(self, obj):
        """Affiche le niveau avec une icône"""
        if obj.niveau_acquisition:
            niveaux_icones = {
                1: "❌ Non acquis",
                2: "🟡 En cours d'acquisition",
                3: "✅ Acquis",
                4: "⭐ Maîtrisé"
            }
            return niveaux_icones.get(obj.niveau_acquisition, "Non évalué")
        return "⏳ Non évalué"
    get_niveau_display.short_description = "Niveau"
    get_niveau_display.admin_order_field = 'niveau_acquisition'
    
    def get_classe_info(self, obj):
        """Affiche la classe"""
        if obj.tableau and obj.tableau.classe:
            return obj.tableau.classe.nom
        return "-"
    get_classe_info.short_description = "Classe"
    get_classe_info.admin_order_field = 'tableau__classe__nom'


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

