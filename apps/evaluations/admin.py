# apps/evaluations/admin.py
from django.contrib import admin
from .models import (
    TypeEvaluation, Evaluation, ResultatEvaluation,
    EvaluationFormation, EvaluationEnseignant,
    Accompagnement, SuiviIndividuel,
    Stage, EvaluationTheorique, EvaluationPratique, Memoire
)
from .models_qualite import (
    IndicateurQualite, MesureQualite, RapportQualite, PlanAmelioration
)
from .models_questionnaire import (
    Question, ReponsePossible, ReponseEtudiant, ParticipationSession
)


@admin.register(TypeEvaluation)
class TypeEvaluationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'nature', 'description')
    list_filter = ('nature',)
    search_fields = ('nom', 'description')


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'cours', 'type_evaluation', 'date_evaluation', 'coefficient', 'actif')
    list_filter = ('type_evaluation', 'actif', 'date_evaluation')
    search_fields = ('titre', 'cours__titre', 'description')
    date_hierarchy = 'date_evaluation'
    filter_horizontal = ('objectifs_evalues', 'competences_evaluees')


@admin.register(ResultatEvaluation)
class ResultatEvaluationAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'evaluation', 'note_obtenue', 'note_sur', 'date_evaluation')
    list_filter = ('evaluation__cours', 'date_evaluation')
    search_fields = ('etudiant__username', 'etudiant__email', 'evaluation__titre')
    date_hierarchy = 'date_evaluation'
    filter_horizontal = ('objectifs_atteints', 'competences_demontrees')


@admin.register(EvaluationFormation)
class EvaluationFormationAdmin(admin.ModelAdmin):
    list_display = ('formation', 'classe', 'taux_reussite', 'satisfaction_etudiants', 'date_evaluation')
    list_filter = ('formation', 'date_evaluation')
    search_fields = ('formation__nom', 'points_forts', 'recommandations')
    date_hierarchy = 'date_evaluation'


@admin.register(EvaluationEnseignant)
class EvaluationEnseignantAdmin(admin.ModelAdmin):
    list_display = ('enseignant', 'cours', 'qualite_pedagogique', 'moyenne_generale', 'date_evaluation')
    list_filter = ('date_evaluation',)
    search_fields = ('enseignant__username', 'cours__titre', 'commentaires')
    date_hierarchy = 'date_evaluation'


@admin.register(Accompagnement)
class AccompagnementAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'accompagnateur', 'type_accompagnement', 'statut', 'date_debut')
    list_filter = ('type_accompagnement', 'statut', 'date_debut')
    search_fields = ('etudiant__username', 'accompagnateur__username', 'objectif')
    date_hierarchy = 'date_debut'


@admin.register(SuiviIndividuel)
class SuiviIndividuelAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'cours', 'responsable', 'date_entretien')
    list_filter = ('cours', 'date_entretien')
    search_fields = ('etudiant__username', 'observations', 'difficultes_identifiees')
    date_hierarchy = 'date_entretien'


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'titre', 'lieu', 'date_debut', 'date_fin', 'valide', 'note')
    list_filter = ('valide', 'date_debut')
    search_fields = ('etudiant__username', 'titre', 'lieu')
    date_hierarchy = 'date_debut'


@admin.register(EvaluationTheorique)
class EvaluationTheoriqueAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'cours', 'titre', 'note', 'date')
    list_filter = ('cours', 'date')
    search_fields = ('etudiant__username', 'titre')
    date_hierarchy = 'date'


@admin.register(EvaluationPratique)
class EvaluationPratiqueAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'cours', 'titre', 'note', 'date')
    list_filter = ('cours', 'date')
    search_fields = ('etudiant__username', 'titre')
    date_hierarchy = 'date'


@admin.register(Memoire)
class MemoireAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'titre', 'note', 'date_soumission', 'date_soutenance')
    list_filter = ('date_soumission',)
    search_fields = ('etudiant__username', 'titre')
    date_hierarchy = 'date_soumission'


# Admin pour les modèles de qualité
@admin.register(IndicateurQualite)
class IndicateurQualiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'categorie', 'cible', 'seuil_alerte', 'unite', 'actif')
    list_filter = ('categorie', 'actif')
    search_fields = ('nom', 'description')


@admin.register(MesureQualite)
class MesureQualiteAdmin(admin.ModelAdmin):
    list_display = ('indicateur', 'formation', 'classe', 'valeur', 'date_mesure', 'statut')
    list_filter = ('indicateur__categorie', 'date_mesure')
    search_fields = ('indicateur__nom', 'formation__nom', 'analyse')
    date_hierarchy = 'date_mesure'
    
    def statut(self, obj):
        return obj.statut
    statut.short_description = 'Statut'


@admin.register(RapportQualite)
class RapportQualiteAdmin(admin.ModelAdmin):
    list_display = ('formation', 'classe', 'periode_debut', 'periode_fin', 'taux_reussite', 'valide', 'date_creation')
    list_filter = ('formation', 'valide', 'date_creation')
    search_fields = ('formation__nom', 'synthese', 'recommandations')
    date_hierarchy = 'date_creation'


@admin.register(PlanAmelioration)
class PlanAmeliorationAdmin(admin.ModelAdmin):
    list_display = ('formation', 'objectif', 'statut', 'date_debut', 'date_fin_prevue')
    list_filter = ('statut', 'date_debut')
    search_fields = ('formation__nom', 'objectif', 'actions_prevues')
    date_hierarchy = 'date_debut'
    filter_horizontal = ('responsables', 'indicateurs_suivi')


# Admin pour les questionnaires
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('enonce', 'evaluation', 'type_question', 'points', 'ordre', 'actif')
    list_filter = ('type_question', 'actif', 'evaluation')
    search_fields = ('enonce', 'evaluation__titre')
    ordering = ('evaluation', 'ordre')


@admin.register(ReponsePossible)
class ReponsePossibleAdmin(admin.ModelAdmin):
    list_display = ('texte', 'question', 'est_correcte', 'ordre')
    list_filter = ('est_correcte', 'question__evaluation')
    search_fields = ('texte', 'question__enonce')
    ordering = ('question', 'ordre')


@admin.register(ReponseEtudiant)
class ReponseEtudiantAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'question', 'points_obtenus', 'est_correcte', 'date_reponse')
    list_filter = ('est_correcte', 'date_reponse')
    search_fields = ('etudiant__username', 'question__enonce')
    date_hierarchy = 'date_reponse'
    filter_horizontal = ('reponses_choisies',)


@admin.register(ParticipationSession)
class ParticipationSessionAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'session_evaluation', 'soumise', 'note_obtenue', 'date_connexion')
    list_filter = ('soumise', 'en_cours', 'date_connexion')
    search_fields = ('etudiant__username', 'session_evaluation__titre')
    date_hierarchy = 'date_connexion'
