from django.contrib import admin, messages
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
    ReponseQuestion, ReponseEtudiantQuiz, ResultatQuiz, AlerteLecon,
    PaiementCours
)
from .models_programme_desmfmc import (
    JalonProgramme, ModuleProgramme, CoursProgramme, SuiviProgressionProgramme,
    CSComUCentre
)
from .models_cout import CoutFormation
from .models_med6 import EtudiantMed6, ListeMed6
from .services.med6_import import sync_etudiants_from_excel
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
    actions = ['generer_etudiants_depuis_fichier']
    
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

    def save_model(self, request, obj, form, change):
        """Enregistre la liste et synchronise automatiquement les étudiants si nécessaire."""
        super().save_model(request, obj, form, change)

        if not obj.fichier_source:
            return

        should_sync = not change

        if form is not None and 'fichier_source' in getattr(form, 'changed_data', []):
            should_sync = True

        if not should_sync:
            return

        try:
            result = sync_etudiants_from_excel(obj, obj.fichier_source)
        except FileNotFoundError:
            messages.error(
                request,
                f"Fichier introuvable pour la liste {obj.annee_universitaire}: {obj.fichier_source}"
            )
        except ImportError as exc:
            messages.error(request, str(exc))
        except Exception as exc:  # pylint: disable=broad-except
            messages.error(
                request,
                f"Erreur lors de la synchronisation automatique pour {obj.annee_universitaire}: {exc}"
            )
        else:
            messages.success(
                request,
                (
                    f"Synchronisation automatique terminée pour {obj.annee_universitaire}: "
                    f"{result['imported']} importés, {result['updated']} mis à jour, "
                    f"{result['errors']} erreurs. Total: {result['total']}."
                )
            )

    @admin.action(description="Générer les étudiants à partir du fichier associé")
    def generer_etudiants_depuis_fichier(self, request, queryset):
        """Action d'admin pour créer/mettre à jour les EtudiantMed6 depuis le fichier Excel."""
        for liste in queryset:
            if not liste.fichier_source:
                messages.error(
                    request,
                    f"La liste {liste.annee_universitaire} n'a pas de fichier source défini."
                )
                continue

            try:
                result = sync_etudiants_from_excel(liste, liste.fichier_source)
            except FileNotFoundError:
                messages.error(
                    request,
                    f"Fichier introuvable pour la liste {liste.annee_universitaire}: {liste.fichier_source}"
                )
                continue
            except ImportError as exc:
                messages.error(request, str(exc))
                return
            except Exception as exc:  # pylint: disable=broad-except
                messages.error(
                    request,
                    f"Erreur lors de la génération pour {liste.annee_universitaire}: {exc}"
                )
                continue

            messages.success(
                request,
                (
                    f"Liste {liste.annee_universitaire}: "
                    f"{result['imported']} importés, {result['updated']} mis à jour, "
                    f"{result['errors']} erreurs. Total: {result['total']}."
                )
            )


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


@admin.register(PaiementCours)
class PaiementCoursAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'cours', 'montant', 'mode_paiement', 'statut', 'date_paiement', 'date_validation', 'est_cours_med6_gratuit')
    list_filter = ('statut', 'mode_paiement', 'date_paiement', 'cours__classe')
    search_fields = ('etudiant__username', 'etudiant__email', 'cours__titre', 'reference_paiement')
    date_hierarchy = 'date_paiement'
    readonly_fields = ('date_paiement', 'date_creation', 'date_modification', 'est_cours_med6_gratuit')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('cours', 'etudiant', 'montant', 'mode_paiement', 'statut')
        }),
        ('Paiement', {
            'fields': ('reference_paiement', 'preuve_paiement', 'date_paiement')
        }),
        ('Validation', {
            'fields': ('valideur', 'date_validation', 'commentaires')
        }),
        ('Informations', {
            'fields': ('est_cours_med6_gratuit',),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimise les requêtes en préchargeant les relations"""
        qs = super().get_queryset(request)
        return qs.select_related('cours', 'cours__classe', 'etudiant', 'valideur')
    
    def est_cours_med6_gratuit(self, obj):
        """Vérifie si le cours est un cours Med6 gratuit pour cet étudiant"""
        if not obj.cours or not obj.cours.classe:
            return "N/A"
        if 'Médecine 6' in obj.cours.classe.nom:
            from core.views_med6 import a_acces_gratuit_med6
            if a_acces_gratuit_med6(obj.etudiant):
                return "⚠️ Oui (cours gratuit - étudiant dans liste active)"
        return "Non"
    est_cours_med6_gratuit.short_description = "Cours Med6 gratuit"
    
    def save_model(self, request, obj, form, change):
        """Valide avant de sauvegarder"""
        # Vérifier si c'est un cours Med6 et si l'étudiant a accès gratuit
        if obj.cours and obj.cours.classe and 'Médecine 6' in obj.cours.classe.nom:
            from core.views_med6 import a_acces_gratuit_med6
            if a_acces_gratuit_med6(obj.etudiant):
                from django.contrib import messages
                messages.warning(
                    request,
                    f"⚠️ Attention : Le cours '{obj.cours.titre}' est gratuit pour {obj.etudiant.get_full_name()} "
                    "car il/elle est dans la liste active des étudiants de Médecine 6. "
                    "Le paiement a été enregistré mais n'est normalement pas nécessaire."
                )
        super().save_model(request, obj, form, change)
    
    actions = ['valider_paiements', 'refuser_paiements']
    
    @admin.action(description="Valider les paiements sélectionnés")
    def valider_paiements(self, request, queryset):
        """Action pour valider plusieurs paiements"""
        from django.utils import timezone
        count = 0
        for paiement in queryset.filter(statut='en_attente'):
            paiement.statut = 'valide'
            paiement.valideur = request.user
            paiement.date_validation = timezone.now()
            paiement.save()
            count += 1
        self.message_user(request, f"{count} paiement(s) validé(s).")
    valider_paiements.short_description = "Valider les paiements sélectionnés"
    
    @admin.action(description="Refuser les paiements sélectionnés")
    def refuser_paiements(self, request, queryset):
        """Action pour refuser plusieurs paiements"""
        count = queryset.filter(statut='en_attente').update(statut='refuse')
        self.message_user(request, f"{count} paiement(s) refusé(s).")
    refuser_paiements.short_description = "Refuser les paiements sélectionnés"


@admin.register(CoutFormation)
class CoutFormationAdmin(admin.ModelAdmin):
    list_display = ('nom_formation', 'formation_slug', 'niveau', 'cout_principal', 'bourse_offerte', 'get_cout_principal_calcule_display', 'actif')
    list_filter = ('niveau', 'modalite_paiement', 'bourse_offerte', 'actif')
    search_fields = ('nom_formation', 'formation_slug')
    readonly_fields = ('date_creation', 'date_modification', 'get_cout_principal_calcule_display', 'get_cout_diu_calcule_display', 'get_cout_licence_calcule_display', 'get_cout_master_calcule_display')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('formation_slug', 'nom_formation', 'niveau', 'actif')
        }),
        ('Coûts de base', {
            'fields': ('cout_principal', 'cout_diu', 'cout_licence', 'cout_master')
        }),
        ('Bourse', {
            'fields': ('bourse_offerte',),
            'description': 'Si une bourse est offerte, tous les coûts seront automatiquement doublés.'
        }),
        ('Coûts calculés (avec bourse si applicable)', {
            'fields': ('get_cout_principal_calcule_display', 'get_cout_diu_calcule_display', 'get_cout_licence_calcule_display', 'get_cout_master_calcule_display'),
            'classes': ('collapse',)
        }),
        ('Modalités de paiement', {
            'fields': ('modalite_paiement', 'conditions_paiement', 'informations_supplementaires')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def get_cout_principal_calcule_display(self, obj):
        """Affiche le coût principal calculé"""
        if obj:
            cout = obj.get_cout_principal_calcule()
            return f"{cout:,.0f} FCFA"
        return "-"
    get_cout_principal_calcule_display.short_description = "Coût principal (calculé)"
    
    def get_cout_diu_calcule_display(self, obj):
        """Affiche le coût DIU calculé"""
        if obj and obj.cout_diu:
            cout = obj.get_cout_diu_calcule()
            return f"{cout:,.0f} FCFA"
        return "-"
    get_cout_diu_calcule_display.short_description = "Coût DIU (calculé)"
    
    def get_cout_licence_calcule_display(self, obj):
        """Affiche le coût Licence calculé"""
        if obj and obj.cout_licence:
            cout = obj.get_cout_licence_calcule()
            return f"{cout:,.0f} FCFA"
        return "-"
    get_cout_licence_calcule_display.short_description = "Coût Licence (calculé)"
    
    def get_cout_master_calcule_display(self, obj):
        """Affiche le coût Master calculé"""
        if obj and obj.cout_master:
            cout = obj.get_cout_master_calcule()
            return f"{cout:,.0f} FCFA"
        return "-"
    get_cout_master_calcule_display.short_description = "Coût Master (calculé)"


# Les autres modèles sont enregistrés dans leurs fichiers admin respectifs
# (admin_carnet_stage.py pour les modèles du carnet de stage)
