# apps/evaluations/admin_grilles.py
"""
Interface d'administration pour les grilles d'évaluation
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from .models_grilles import (
    TypeGrilleEvaluation,
    GrilleEvaluation,
    CritereEvaluation,
    ElementEvaluation,
    EvaluationAvecGrille,
    ReponseCritere,
    ReponseElement
)
import tempfile
import os

# Import conditionnel pour éviter les erreurs si python-docx n'est pas installé
try:
    from .importers.import_word_grille import create_word_template
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False


@admin.register(TypeGrilleEvaluation)
class TypeGrilleEvaluationAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'type_grille', 'actif')
    list_filter = ('type_grille', 'actif')
    search_fields = ('code', 'nom', 'description')
    ordering = ('type_grille', 'nom')


class ElementEvaluationInline(admin.TabularInline):
    model = ElementEvaluation
    extra = 1
    fields = ('ordre', 'libelle', 'poids', 'actif')
    ordering = ('ordre',)


class CritereEvaluationInline(admin.TabularInline):
    model = CritereEvaluation
    extra = 1
    fields = ('ordre', 'libelle', 'poids', 'note_maximale', 'competence', 'actif')
    ordering = ('ordre',)
    show_change_link = True


@admin.register(GrilleEvaluation)
class GrilleEvaluationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_grille', 'cours', 'classe', 'note_maximale', 'date_creation', 'actif')
    list_filter = ('type_grille', 'actif', 'date_creation', 'classe')
    search_fields = ('titre', 'description', 'cours__titre', 'classe__nom')
    filter_horizontal = ('competences_evaluees', 'jalons_evalues')
    readonly_fields = ('date_creation', 'date_modification')
    
    def get_readonly_fields(self, request, obj=None):
        """Ajouter createur aux champs en lecture seule seulement lors de l'édition"""
        readonly = list(self.readonly_fields)
        if obj:  # Si l'objet existe déjà (édition)
            readonly.append('createur')
        return readonly
    inlines = [CritereEvaluationInline]
    
    def get_fieldsets(self, request, obj=None):
        """Définir les fieldsets avec createur seulement en édition"""
        fieldsets = (
            ('Informations générales', {
                'fields': ('type_grille', 'titre', 'description', 'actif')
            }),
            ('Contexte', {
                'fields': ('cours', 'classe', 'competences_evaluees', 'jalons_evaluees')
            }),
            ('Paramètres d\'évaluation', {
                'fields': ('note_maximale', 'echelle_evaluation')
            }),
        )
        
        # Ajouter les métadonnées seulement si l'objet existe
        if obj:
            fieldsets += (
                ('Métadonnées', {
                    'fields': ('createur', 'date_creation', 'date_modification'),
                    'classes': ('collapse',)
                }),
            )
        else:
            # Lors de la création, afficher seulement date_creation et date_modification (qui seront auto-remplis)
            fieldsets += (
                ('Métadonnées', {
                    'fields': ('date_creation', 'date_modification'),
                    'classes': ('collapse',)
                }),
            )
        
        return fieldsets
    
    actions = ['download_template']
    
    def save_model(self, request, obj, form, change):
        if not change:  # Nouvelle grille
            obj.createur = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('type_grille', 'cours', 'classe', 'createur')
    
    def get_form(self, request, obj=None, **kwargs):
        """Surcharge pour éviter les erreurs lors de la création"""
        form = super().get_form(request, obj, **kwargs)
        return form
    
    def download_template(self, request, queryset):
        """Action pour télécharger un modèle Word"""
        if not HAS_DOCX:
            from django.contrib import messages
            messages.error(request, "Le module python-docx n'est pas installé. Installez-le avec: pip install python-docx")
            return None
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            create_word_template(tmp_file.name)
            
            with open(tmp_file.name, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                response['Content-Disposition'] = 'attachment; filename="template_grille_evaluation.docx"'
            
            os.unlink(tmp_file.name)
            return response
    
    download_template.short_description = "Télécharger le modèle Word"


@admin.register(CritereEvaluation)
class CritereEvaluationAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'grille', 'ordre', 'poids', 'note_maximale', 'actif')
    list_filter = ('grille', 'actif', 'competence')
    search_fields = ('libelle', 'description', 'grille__titre')
    ordering = ('grille', 'ordre')
    inlines = [ElementEvaluationInline]
    
    fieldsets = (
        ('Informations', {
            'fields': ('grille', 'ordre', 'libelle', 'description', 'actif')
        }),
        ('Pondération', {
            'fields': ('poids', 'note_maximale')
        }),
        ('Associations', {
            'fields': ('competence', 'jalon')
        }),
    )


@admin.register(ElementEvaluation)
class ElementEvaluationAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'critere', 'ordre', 'poids', 'actif')
    list_filter = ('critere__grille', 'actif')
    search_fields = ('libelle', 'description', 'critere__libelle')
    ordering = ('critere', 'ordre')


class ReponseElementInline(admin.TabularInline):
    model = ReponseElement
    extra = 0
    fields = ('element', 'note', 'niveau', 'commentaire')
    readonly_fields = ('element',)
    can_delete = False


class ReponseCritereInline(admin.TabularInline):
    model = ReponseCritere
    extra = 0
    fields = ('critere', 'note', 'niveau', 'commentaire')
    readonly_fields = ('critere',)
    can_delete = False


@admin.register(EvaluationAvecGrille)
class EvaluationAvecGrilleAdmin(admin.ModelAdmin):
    list_display = ('grille', 'etudiant', 'evaluateur', 'note_obtenue', 'note_sur', 'pourcentage_display', 'date_evaluation')
    list_filter = ('grille', 'date_evaluation', 'evaluateur')
    search_fields = ('etudiant__username', 'etudiant__first_name', 'etudiant__last_name', 'grille__titre')
    readonly_fields = ('date_creation', 'date_modification', 'pourcentage_display')
    inlines = [ReponseCritereInline]
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('grille', 'etudiant', 'evaluateur', 'date_evaluation')
        }),
        ('Résultats', {
            'fields': ('note_obtenue', 'note_sur', 'pourcentage_display')
        }),
        ('Commentaires', {
            'fields': ('commentaires_generaux', 'points_forts', 'axes_amelioration')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def pourcentage_display(self, obj):
        if obj.pourcentage:
            return format_html('<strong>{:.1f}%</strong>', obj.pourcentage)
        return '-'
    pourcentage_display.short_description = 'Pourcentage'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('grille', 'etudiant', 'evaluateur')


@admin.register(ReponseCritere)
class ReponseCritereAdmin(admin.ModelAdmin):
    list_display = ('evaluation', 'critere', 'note', 'niveau', 'commentaire')
    list_filter = ('evaluation__grille', 'niveau')
    search_fields = ('evaluation__etudiant__username', 'critere__libelle')


@admin.register(ReponseElement)
class ReponseElementAdmin(admin.ModelAdmin):
    list_display = ('reponse_critere', 'element', 'note', 'niveau', 'commentaire')
    list_filter = ('reponse_critere__evaluation__grille', 'niveau')
    search_fields = ('element__libelle', 'reponse_critere__evaluation__etudiant__username')

