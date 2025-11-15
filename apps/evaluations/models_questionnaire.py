# apps/evaluations/models_questionnaire.py
"""
Modèles pour les questionnaires interactifs d'évaluation en ligne
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.utilisateurs.models import Utilisateur
from .models import Evaluation


class Question(models.Model):
    """Modèle pour les questions d'une évaluation"""
    TYPE_QUESTION_CHOICES = [
        ('qcm', 'Question à choix multiples (QCM)'),
        ('qcu', 'Question à choix unique (QCU)'),
        ('texte', 'Réponse libre (texte)'),
        ('numerique', 'Réponse numérique'),
        ('vrai_faux', 'Vrai/Faux'),
        ('ordre', 'Mise en ordre'),
    ]
    
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Évaluation"
    )
    enonce = models.TextField(verbose_name="Énoncé de la question")
    type_question = models.CharField(
        max_length=20,
        choices=TYPE_QUESTION_CHOICES,
        default='qcm',
        verbose_name="Type de question"
    )
    points = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0)],
        verbose_name="Points"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    explication = models.TextField(
        blank=True,
        null=True,
        verbose_name="Explication",
        help_text="Explication de la réponse correcte (affichée après correction)"
    )
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['evaluation', 'ordre']
    
    def __str__(self):
        return f"{self.evaluation.titre} - Question {self.ordre}"


class ReponsePossible(models.Model):
    """Modèle pour les réponses possibles d'une question"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='reponses_possibles',
        verbose_name="Question"
    )
    texte = models.TextField(verbose_name="Texte de la réponse")
    est_correcte = models.BooleanField(
        default=False,
        verbose_name="Est correcte",
        help_text="Cocher si cette réponse est correcte"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    
    class Meta:
        verbose_name = "Réponse possible"
        verbose_name_plural = "Réponses possibles"
        ordering = ['question', 'ordre']
    
    def __str__(self):
        return f"{self.question} - {self.texte[:50]}"


class ReponseEtudiant(models.Model):
    """Modèle pour les réponses d'un étudiant à une question"""
    session_evaluation = models.ForeignKey(
        'utilisateurs.SessionEvaluationEnLigne',
        on_delete=models.CASCADE,
        related_name='reponses_etudiants',
        verbose_name="Session d'évaluation"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='reponses_etudiants',
        verbose_name="Question"
    )
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='reponses_questions',
        verbose_name="Étudiant"
    )
    
    # Réponse (peut être multiple pour QCM)
    reponses_choisies = models.ManyToManyField(
        ReponsePossible,
        related_name='reponses_etudiants',
        blank=True,
        verbose_name="Réponses choisies"
    )
    reponse_texte = models.TextField(
        blank=True,
        null=True,
        verbose_name="Réponse texte",
        help_text="Pour les questions à réponse libre"
    )
    reponse_numerique = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Réponse numérique"
    )
    
    # Correction
    points_obtenus = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Points obtenus"
    )
    est_correcte = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Est correcte"
    )
    commentaire_correction = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire de correction"
    )
    
    # Métadonnées
    date_reponse = models.DateTimeField(auto_now_add=True, verbose_name="Date de réponse")
    date_correction = models.DateTimeField(null=True, blank=True, verbose_name="Date de correction")
    
    class Meta:
        verbose_name = "Réponse étudiant"
        verbose_name_plural = "Réponses étudiants"
        unique_together = ['session_evaluation', 'question', 'etudiant']
        ordering = ['date_reponse']
    
    def __str__(self):
        return f"{self.etudiant.username} - {self.question}"


class ParticipationSession(models.Model):
    """Modèle pour suivre la participation aux sessions"""
    session_evaluation = models.ForeignKey(
        'utilisateurs.SessionEvaluationEnLigne',
        on_delete=models.CASCADE,
        related_name='participations',
        verbose_name="Session d'évaluation"
    )
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='participations_sessions',
        verbose_name="Étudiant"
    )
    
    # Suivi
    date_connexion = models.DateTimeField(auto_now_add=True, verbose_name="Date de connexion")
    date_debut_evaluation = models.DateTimeField(null=True, blank=True, verbose_name="Date de début")
    date_fin_evaluation = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")
    date_soumission = models.DateTimeField(null=True, blank=True, verbose_name="Date de soumission")
    
    # Statut
    en_cours = models.BooleanField(default=True, verbose_name="En cours")
    soumise = models.BooleanField(default=False, verbose_name="Soumise")
    
    # Résultat
    note_obtenue = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Note obtenue"
    )
    note_sur = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Note sur"
    )
    
    class Meta:
        verbose_name = "Participation à une session"
        verbose_name_plural = "Participations aux sessions"
        unique_together = ['session_evaluation', 'etudiant']
        ordering = ['-date_connexion']
    
    def __str__(self):
        return f"{self.etudiant.username} - {self.session_evaluation.titre}"

