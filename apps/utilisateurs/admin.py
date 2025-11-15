from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from .models import Utilisateur, CodeVerification, Code2FA
from .admin_filters import ClasseWithCoursFilter
from .models_formation import (
    Formation, Classe, Cours, Lecon, ProgressionEtudiant, Planification,
    ObjectifApprentissage, MethodePedagogique, Competence,
    SessionCoursEnLigne, SessionEvaluationEnLigne,
    ProgressionLecon, CommentaireLecon, QuizLecon, QuestionQuiz,
    ReponseQuestion, ReponseEtudiantQuiz, ResultatQuiz, AlerteLecon
)
from .models_programme_desmfmc import (
    JalonProgramme, ModuleProgramme, CoursProgramme, SuiviProgressionProgramme,
    CSComUCentre
)
from .models_cout import CoutFormation
from .models_med6 import EtudiantMed6, ListeMed6
from .models_documents import LettreInformation, ModelePedagogique, SignatureCoordination
from .models_carnet_stage import (
    CarnetStage, EvaluationStage, EvaluationCompetence,
    TableauEvaluationClasse, EvaluationCompetenceTableau
)
# Import de l'admin pour le carnet de stage (défini dans admin_carnet_stage.py)
from .admin_carnet_stage import (
    CarnetStageAdmin, EvaluationStageAdmin, EvaluationCompetenceAdmin,
    TableauEvaluationClasseAdmin, EvaluationCompetenceTableauAdmin
)

@admin.register(ListeMed6)
class ListeMed6Admin(admin.ModelAdmin):
    list_display = ('annee_universitaire', 'fichier_source', 'date_import', 'nombre_etudiants', 'active', 'est_expiree_display')
    list_filter = ('active', 'date_import', 'annee_universitaire')
    search_fields = ('annee_universitaire', 'fichier_source')
    readonly_fields = ('date_import', 'nombre_etudiants')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('annee_universitaire', 'fichier_source', 'date_cloture', 'active', 'date_import', 'nombre_etudiants')
        }),
    )
    
    def nombre_etudiants(self, obj):
        """Affiche le nombre d'étudiants dans la liste"""
        return obj.etudiants.count()
    nombre_etudiants.short_description = 'Nombre d\'étudiants'
    
    def est_expiree_display(self, obj):
        """Affiche si la liste est expirée"""
        return "Oui" if obj.est_expiree() else "Non"
    est_expiree_display.boolean = True
    est_expiree_display.short_description = 'Expirée'


@admin.register(EtudiantMed6)
class EtudiantMed6Admin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'liste', 'actif', 'date_creation')
    list_filter = ('liste', 'actif', 'date_creation')
    search_fields = ('matricule', 'nom', 'prenom')
    readonly_fields = ('date_creation', 'date_modification')
    
    fieldsets = (
        ('Informations étudiant', {
            'fields': ('liste', 'matricule', 'nom', 'prenom', 'numero_carte_scolaire', 'actif')
        }),
        ('Informations système', {
            'fields': ('utilisateur', 'date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('username', 'email', 'type_utilisateur', 'classe', 'niveau_acces', 'email_verifie', 'superviseur_cec', 'centre_supervision', 'membre_coordination', 'is_staff', 'is_active')
    list_filter = ('type_utilisateur', 'niveau_acces', 'email_verifie', 'superviseur_cec', 'centre_supervision', 'membre_coordination', 'is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'telephone', 'first_name', 'last_name', 'classe', 'matieres')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'telephone', 'date_naissance', 'adresse')
        }),
        ('Type et accès', {
            'fields': ('type_utilisateur', 'classe', 'matieres', 'niveau_acces', 'email_verifie', 'superviseur_cec', 'centre_supervision', 'membre_coordination')
        }),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Informations personnelles', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'telephone', 'date_naissance', 'adresse'),
        }),
        ('Type et accès', {
            'classes': ('wide',),
            'fields': ('type_utilisateur', 'classe', 'matieres', 'niveau_acces', 'email_verifie', 'superviseur_cec', 'centre_supervision', 'membre_coordination'),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_staff', 'is_active', 'is_superuser'),
        }),
    )


@admin.register(CodeVerification)
class CodeVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'cree_le', 'expire_le', 'utilise', 'est_valide_display')
    list_filter = ('utilise', 'cree_le', 'expire_le')
    search_fields = ('user__username', 'user__email', 'code')
    readonly_fields = ('cree_le', 'expire_le', 'utilise')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'code', 'cree_le', 'expire_le', 'utilise')
        }),
    )
    
    def est_valide_display(self, obj):
        """Affiche si le code est encore valide"""
        from django.utils import timezone
        if obj.utilise:
            return "Utilisé"
        if obj.expire_le < timezone.now():
            return "Expiré"
        return "Valide"
    est_valide_display.short_description = 'Statut'


@admin.register(Code2FA)
class Code2FAAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'cree_le', 'expire_le', 'utilise', 'ip_address', 'est_valide_display')
    list_filter = ('utilise', 'cree_le', 'expire_le')
    search_fields = ('user__username', 'user__email', 'code', 'ip_address')
    readonly_fields = ('cree_le', 'expire_le', 'utilise', 'ip_address', 'user_agent')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'code', 'cree_le', 'expire_le', 'utilise')
        }),
        ('Informations techniques', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
    )
    
    def est_valide_display(self, obj):
        """Affiche si le code est encore valide"""
        from django.utils import timezone
        if obj.utilise:
            return "Utilisé"
        if obj.expire_le < timezone.now():
            return "Expiré"
        return "Valide"
    est_valide_display.short_description = 'Statut'


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'type_formation', 'nature', 'duree_annees', 'actif')
    list_filter = ('type_formation', 'nature', 'actif')
    search_fields = ('nom', 'code', 'description')
    prepopulated_fields = {'code': ('nom',)}


@admin.register(CSComUCentre)
class CSComUCentreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'type_centre', 'localisation', 'cec_superviseur_principal', 'actif', 'nombre_superviseurs', 'nombre_stages')
    list_filter = ('type_centre', 'actif')
    search_fields = ('nom', 'code', 'localisation', 'cec_superviseur_principal')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'code', 'type_centre', 'localisation', 'actif')
        }),
        ('Supervision', {
            'fields': ('cec_superviseur_principal',)
        }),
    )
    
    def nombre_superviseurs(self, obj):
        """Affiche le nombre de superviseurs assignés à ce centre"""
        return obj.superviseurs.count()
    nombre_superviseurs.short_description = 'Superviseurs'
    
    def nombre_stages(self, obj):
        """Affiche le nombre de stages attribués à ce centre"""
        return obj.stages_attribues.count()
    nombre_stages.short_description = 'Stages'


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'formation', 'annee', 'date_debut', 'date_fin', 'actif', 'nombre_etudiants', 'nombre_cours')
    list_filter = ('formation', 'annee', 'actif', 'date_debut')
    search_fields = ('nom', 'code', 'formation__nom')
    date_hierarchy = 'date_debut'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('formation', 'nom', 'code', 'annee', 'actif')
        }),
        ('Dates', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Effectif', {
            'fields': ('effectif_max', 'responsable')
        }),
    )
    
    def nombre_etudiants(self, obj):
        """Affiche le nombre d'étudiants dans cette classe"""
        return Utilisateur.objects.filter(classe=obj.nom, type_utilisateur='etudiant', is_active=True).count()
    nombre_etudiants.short_description = 'Étudiants'
    
    def nombre_cours(self, obj):
        """Affiche le nombre de cours dans cette classe"""
        return obj.cours.filter(actif=True).count()
    nombre_cours.short_description = 'Cours'


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'code', 'classe', 'enseignant', 'date_debut', 'date_fin', 'volume_horaire', 'ordre', 'actif', 'nombre_lecons')
    list_filter = ('classe', 'actif', 'date_debut', 'classe__formation')
    search_fields = ('titre', 'code', 'description', 'classe__nom')
    date_hierarchy = 'date_debut'
    filter_horizontal = ('co_enseignants', 'objectifs_apprentissage', 'competences', 'methodes_pedagogiques')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('classe', 'titre', 'code', 'ordre', 'actif')
        }),
        ('Contenu', {
            'fields': ('description', 'contenu', 'fichier_contenu', 'ressources_pedagogiques')
        }),
        ('Dates et volume', {
            'fields': ('date_debut', 'date_fin', 'volume_horaire')
        }),
        ('Enseignants', {
            'fields': ('enseignant', 'co_enseignants')
        }),
        ('Pédagogie', {
            'fields': ('description_methodes', 'objectifs_apprentissage', 'competences', 'methodes_pedagogiques'),
            'classes': ('collapse',)
        }),
    )
    
    def nombre_lecons(self, obj):
        """Affiche le nombre de leçons dans ce cours"""
        return obj.lecons.filter(actif=True).count()
    nombre_lecons.short_description = 'Leçons'


@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'numero', 'type_lecon', 'duree_estimee', 'ordre', 'date_dispensation', 'actif')
    list_filter = ('cours', 'type_lecon', 'actif', 'cours__classe')
    search_fields = ('titre', 'cours__titre', 'contenu')
    date_hierarchy = 'date_dispensation'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('cours', 'titre', 'numero', 'type_lecon', 'ordre', 'actif')
        }),
        ('Contenu', {
            'fields': ('contenu', 'fichier_contenu', 'ressources')
        }),
        ('Planification', {
            'fields': ('date_dispensation', 'duree_estimee')
        }),
    )
    
    def get_queryset(self, request):
        """Optimise les requêtes en préchargeant les relations"""
        qs = super().get_queryset(request)
        return qs.select_related('cours', 'cours__classe')


# Les autres modèles sont enregistrés dans leurs fichiers admin respectifs
# (admin_carnet_stage.py pour les modèles du carnet de stage)
