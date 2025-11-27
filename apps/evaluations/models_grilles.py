# apps/evaluations/models_grilles.py
"""
Modèles pour les grilles d'évaluation structurées
Grilles pour : formative, sommative, finale, supervision, simulation, scénario, présentation, habiletés cliniques
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Cours, Classe, Competence, CompetenceJalon


class TypeGrilleEvaluation(models.Model):
    """Types de grilles d'évaluation"""
    TYPE_CHOICES = [
        ('formative', 'Évaluation Formative'),
        ('sommative', 'Évaluation Sommative'),
        ('finale', 'Évaluation Finale'),
        ('supervision', 'Supervision'),
        ('simulation', 'Activité de Simulation'),
        ('scenario', 'Activité de Scénario'),
        ('presentation', 'Présentation'),
        ('habiletes_cliniques', 'Habiletés Cliniques'),
    ]
    
    code = models.CharField(max_length=50, unique=True, verbose_name="Code")
    nom = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(verbose_name="Description")
    type_grille = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES,
        verbose_name="Type de grille"
    )
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Type de grille d'évaluation"
        verbose_name_plural = "Types de grilles d'évaluation"
        ordering = ['type_grille', 'nom']
    
    def __str__(self):
        return f"{self.get_type_grille_display()} - {self.nom}"


class GrilleEvaluation(models.Model):
    """Modèle principal pour les grilles d'évaluation"""
    type_grille = models.ForeignKey(
        TypeGrilleEvaluation,
        on_delete=models.CASCADE,
        related_name='grilles',
        verbose_name="Type de grille"
    )
    titre = models.CharField(max_length=300, verbose_name="Titre de la grille")
    description = models.TextField(verbose_name="Description")
    
    # Contexte
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='grilles_evaluation',
        null=True,
        blank=True,
        verbose_name="Cours associé"
    )
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='grilles_evaluation',
        null=True,
        blank=True,
        verbose_name="Classe associée"
    )
    
    # Compétences et jalons évalués
    competences_evaluees = models.ManyToManyField(
        Competence,
        related_name='grilles_evaluation',
        blank=True,
        verbose_name="Compétences évaluées"
    )
    jalons_evalues = models.ManyToManyField(
        CompetenceJalon,
        related_name='grilles_evaluation',
        blank=True,
        verbose_name="Jalons évalués"
    )
    
    # Paramètres d'évaluation
    note_maximale = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20.0,
        validators=[MinValueValidator(0)],
        verbose_name="Note maximale"
    )
    echelle_evaluation = models.CharField(
        max_length=20,
        choices=[
            ('1-5', '1 : Insuffisante · 2 : Inconstante/Inférieure aux attentes · 3 : Conforme aux attentes · 4 : Dépasse nettement les attentes · 5 : NA (Non Applicable)'),
            ('0-20', 'Note sur 20'),
            ('0-100', 'Pourcentage (0-100)'),
        ],
        default='1-5',
        verbose_name="Échelle d'évaluation"
    )
    
    # Métadonnées
    createur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='grilles_creees',
        verbose_name="Créateur"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Grille d'évaluation"
        verbose_name_plural = "Grilles d'évaluation"
        ordering = ['-date_creation', 'titre']
    
    def __str__(self):
        return f"{self.type_grille.nom} - {self.titre}"


class CritereEvaluation(models.Model):
    """Critères d'évaluation dans une grille"""
    grille = models.ForeignKey(
        GrilleEvaluation,
        on_delete=models.CASCADE,
        related_name='criteres',
        verbose_name="Grille d'évaluation"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    libelle = models.CharField(max_length=500, verbose_name="Libellé du critère")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description détaillée"
    )
    
    # Pondération
    poids = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0)],
        verbose_name="Poids/Pondération"
    )
    note_maximale = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Note maximale (si différente de la grille)"
    )
    
    # Compétence/jalon associé
    competence = models.ForeignKey(
        Competence,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='criteres_evaluation',
        verbose_name="Compétence associée"
    )
    jalon = models.ForeignKey(
        CompetenceJalon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='criteres_evaluation',
        verbose_name="Jalon associé"
    )
    
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Critère d'évaluation"
        verbose_name_plural = "Critères d'évaluation"
        ordering = ['grille', 'ordre', 'libelle']
        unique_together = [['grille', 'ordre']]
    
    def __str__(self):
        return f"{self.grille.titre[:50]}... - {self.libelle[:50]}..."


class ElementEvaluation(models.Model):
    """Éléments de détail pour un critère (sous-critères)"""
    critere = models.ForeignKey(
        CritereEvaluation,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name="Critère parent"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    libelle = models.CharField(max_length=500, verbose_name="Libellé de l'élément")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    
    # Pondération
    poids = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0)],
        verbose_name="Poids/Pondération"
    )
    
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Élément d'évaluation"
        verbose_name_plural = "Éléments d'évaluation"
        ordering = ['critere', 'ordre', 'libelle']
    
    def __str__(self):
        return f"{self.critere.libelle[:30]}... - {self.libelle[:50]}..."


class EvaluationAvecGrille(models.Model):
    """Instance d'évaluation utilisant une grille"""
    grille = models.ForeignKey(
        GrilleEvaluation,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name="Grille utilisée"
    )
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='evaluations_grilles',
        verbose_name="Étudiant évalué"
    )
    evaluateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='evaluations_realisees',
        verbose_name="Évaluateur"
    )
    
    # Résultats
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
    
    # Commentaires
    commentaires_generaux = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaires généraux"
    )
    points_forts = models.TextField(
        blank=True,
        null=True,
        verbose_name="Points forts"
    )
    axes_amelioration = models.TextField(
        blank=True,
        null=True,
        verbose_name="Axes d'amélioration"
    )
    
    # Métadonnées
    date_evaluation = models.DateTimeField(
        default=timezone.now,
        verbose_name="Date d'évaluation"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Évaluation avec grille"
        verbose_name_plural = "Évaluations avec grilles"
        ordering = ['-date_evaluation', 'etudiant']
        unique_together = [['grille', 'etudiant', 'date_evaluation']]
    
    def __str__(self):
        return f"{self.grille.titre} - {self.etudiant.get_full_name() or self.etudiant.username} - {self.date_evaluation.date()}"
    
    @property
    def pourcentage(self):
        """Calcule le pourcentage obtenu"""
        if self.note_sur and self.note_sur > 0:
            return (self.note_obtenue / self.note_sur) * 100
        return 0


class ReponseCritere(models.Model):
    """Réponse/évaluation pour un critère spécifique"""
    evaluation = models.ForeignKey(
        EvaluationAvecGrille,
        on_delete=models.CASCADE,
        related_name='reponses_criteres',
        verbose_name="Évaluation"
    )
    critere = models.ForeignKey(
        CritereEvaluation,
        on_delete=models.CASCADE,
        related_name='reponses',
        verbose_name="Critère"
    )
    
    # Évaluation
    note = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Note obtenue"
    )
    niveau = models.CharField(
        max_length=20,
        choices=[
            ('1', '1 : Insuffisante'),
            ('2', '2 : Inconstante/Inférieure aux attentes'),
            ('3', '3 : Conforme aux attentes'),
            ('4', '4 : Dépasse nettement les attentes'),
            ('5', '5 : NA (Non Applicable)'),
        ],
        null=True,
        blank=True,
        verbose_name="Niveau atteint"
    )
    
    # Commentaires
    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire"
    )
    
    class Meta:
        verbose_name = "Réponse critère"
        verbose_name_plural = "Réponses critères"
        unique_together = [['evaluation', 'critere']]
    
    def __str__(self):
        return f"{self.evaluation} - {self.critere.libelle[:50]}..."


class ReponseElement(models.Model):
    """Réponse/évaluation pour un élément spécifique"""
    reponse_critere = models.ForeignKey(
        ReponseCritere,
        on_delete=models.CASCADE,
        related_name='reponses_elements',
        verbose_name="Réponse critère"
    )
    element = models.ForeignKey(
        ElementEvaluation,
        on_delete=models.CASCADE,
        related_name='reponses',
        verbose_name="Élément"
    )
    
    # Évaluation
    note = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Note obtenue"
    )
    niveau = models.CharField(
        max_length=20,
        choices=[
            ('1', '1 : Insuffisante'),
            ('2', '2 : Inconstante/Inférieure aux attentes'),
            ('3', '3 : Conforme aux attentes'),
            ('4', '4 : Dépasse nettement les attentes'),
            ('5', '5 : NA (Non Applicable)'),
        ],
        null=True,
        blank=True,
        verbose_name="Niveau atteint"
    )
    
    # Commentaires
    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire"
    )
    
    class Meta:
        verbose_name = "Réponse élément"
        verbose_name_plural = "Réponses éléments"
        unique_together = [['reponse_critere', 'element']]
    
    def __str__(self):
        return f"{self.reponse_critere} - {self.element.libelle[:50]}..."

