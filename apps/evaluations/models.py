# apps/evaluations/models.py
"""
Modèles pour le système d'évaluation complet
Évaluation des étudiants, des formations, des enseignants
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Cours, Formation, Classe, ObjectifApprentissage, Competence


class TypeEvaluation(models.Model):
    """Types d'évaluation (formative, sommative, diagnostique, etc.)"""
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    description = models.TextField(verbose_name="Description")
    nature = models.CharField(
        max_length=20,
        choices=[
            ('formative', 'Formative'),
            ('sommative', 'Sommative'),
            ('diagnostique', 'Diagnostique'),
            ('certificative', 'Certificative'),
        ],
        default='formative',
        verbose_name="Nature"
    )
    
    class Meta:
        verbose_name = "Type d'évaluation"
        verbose_name_plural = "Types d'évaluation"
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Evaluation(models.Model):
    """Modèle pour les évaluations des étudiants"""
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name="Cours"
    )
    titre = models.CharField(max_length=200, verbose_name="Titre de l'évaluation")
    type_evaluation = models.ForeignKey(
        TypeEvaluation,
        on_delete=models.SET_NULL,
        null=True,
        related_name='evaluations',
        verbose_name="Type d'évaluation"
    )
    description = models.TextField(verbose_name="Description")
    
    # Objectifs évalués
    objectifs_evalues = models.ManyToManyField(
        ObjectifApprentissage,
        related_name='evaluations',
        blank=True,
        verbose_name="Objectifs évalués"
    )
    
    # Compétences évaluées
    competences_evaluees = models.ManyToManyField(
        Competence,
        related_name='evaluations',
        blank=True,
        verbose_name="Compétences évaluées"
    )
    
    # Organisation
    date_evaluation = models.DateTimeField(verbose_name="Date et heure de l'évaluation")
    duree_minutes = models.IntegerField(
        default=60,
        validators=[MinValueValidator(1)],
        verbose_name="Durée en minutes"
    )
    coefficient = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0)],
        verbose_name="Coefficient"
    )
    note_maximale = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20.0,
        validators=[MinValueValidator(0)],
        verbose_name="Note maximale"
    )
    
    # Critères d'évaluation
    criteres_evaluation = models.TextField(
        verbose_name="Critères d'évaluation",
        help_text="Critères détaillés pour l'évaluation"
    )
    
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Évaluation"
        verbose_name_plural = "Évaluations"
        ordering = ['-date_evaluation']
    
    def __str__(self):
        return f"{self.cours.titre} - {self.titre}"


class ResultatEvaluation(models.Model):
    """Résultats d'évaluation d'un étudiant"""
    evaluation = models.ForeignKey(
        Evaluation,
        on_delete=models.CASCADE,
        related_name='resultats',
        verbose_name="Évaluation"
    )
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='resultats_evaluations',
        verbose_name="Étudiant"
    )
    
    # Notes
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
        default=20.0,
        verbose_name="Note sur"
    )
    
    # Objectifs atteints
    objectifs_atteints = models.ManyToManyField(
        ObjectifApprentissage,
        related_name='resultats_objectifs',
        blank=True,
        verbose_name="Objectifs atteints"
    )
    
    # Compétences démontrées
    competences_demontrees = models.ManyToManyField(
        Competence,
        related_name='resultats_competences',
        blank=True,
        verbose_name="Compétences démontrées"
    )
    
    # Commentaires
    commentaires = models.TextField(blank=True, null=True, verbose_name="Commentaires")
    commentaires_enseignant = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaires de l'enseignant"
    )
    
    # Dates
    date_evaluation = models.DateTimeField(null=True, blank=True, verbose_name="Date de l'évaluation")
    date_correction = models.DateTimeField(null=True, blank=True, verbose_name="Date de correction")
    
    class Meta:
        verbose_name = "Résultat d'évaluation"
        verbose_name_plural = "Résultats d'évaluation"
        unique_together = ['evaluation', 'etudiant']
        ordering = ['-date_evaluation']
    
    def __str__(self):
        return f"{self.etudiant.username} - {self.evaluation.titre}"
    
    @property
    def pourcentage(self):
        if self.note_obtenue and self.note_sur:
            return (self.note_obtenue / self.note_sur) * 100
        return 0


class EvaluationFormation(models.Model):
    """Évaluation de l'efficacité d'une formation"""
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='evaluations_formation',
        verbose_name="Formation"
    )
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='evaluations_classe',
        null=True,
        blank=True,
        verbose_name="Classe (optionnel)"
    )
    
    # Indicateurs de qualité
    taux_reussite = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Taux de réussite (%)"
    )
    taux_assiduite = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Taux d'assiduité (%)"
    )
    satisfaction_etudiants = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Satisfaction étudiants (0-5)"
    )
    satisfaction_enseignants = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Satisfaction enseignants (0-5)"
    )
    
    # Analyse
    points_forts = models.TextField(blank=True, null=True, verbose_name="Points forts")
    points_amelioration = models.TextField(blank=True, null=True, verbose_name="Points à améliorer")
    recommandations = models.TextField(blank=True, null=True, verbose_name="Recommandations")
    
    # Métadonnées
    periode_debut = models.DateField(verbose_name="Période début")
    periode_fin = models.DateField(verbose_name="Période fin")
    date_evaluation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'évaluation")
    evaluateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='evaluations_formation_effectuees',
        verbose_name="Évaluateur"
    )
    
    class Meta:
        verbose_name = "Évaluation de formation"
        verbose_name_plural = "Évaluations de formation"
        ordering = ['-date_evaluation']
    
    def __str__(self):
        return f"Évaluation {self.formation.nom} - {self.periode_debut}"


class EvaluationEnseignant(models.Model):
    """Évaluation des enseignants"""
    enseignant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='evaluations_enseignant',
        verbose_name="Enseignant"
    )
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='evaluations_enseignants',
        null=True,
        blank=True,
        verbose_name="Cours (optionnel)"
    )
    
    # Critères d'évaluation
    qualite_pedagogique = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Qualité pédagogique (0-5)"
    )
    disponibilite = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Disponibilité (0-5)"
    )
    clarte_explications = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Clarté des explications (0-5)"
    )
    gestion_classe = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Gestion de classe (0-5)"
    )
    
    # Commentaires
    commentaires = models.TextField(blank=True, null=True, verbose_name="Commentaires")
    points_forts = models.TextField(blank=True, null=True, verbose_name="Points forts")
    axes_amelioration = models.TextField(blank=True, null=True, verbose_name="Axes d'amélioration")
    
    # Métadonnées
    date_evaluation = models.DateTimeField(auto_now_add=True, verbose_name="Date d'évaluation")
    evaluateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='evaluations_enseignants_effectuees',
        verbose_name="Évaluateur"
    )
    
    class Meta:
        verbose_name = "Évaluation enseignant"
        verbose_name_plural = "Évaluations enseignants"
        ordering = ['-date_evaluation']
    
    def __str__(self):
        return f"Évaluation {self.enseignant.username} - {self.date_evaluation.strftime('%Y-%m-%d')}"
    
    @property
    def moyenne_generale(self):
        scores = [
            self.qualite_pedagogique,
            self.disponibilite,
            self.clarte_explications,
            self.gestion_classe
        ]
        scores_valides = [s for s in scores if s is not None]
        if scores_valides:
            return sum(scores_valides) / len(scores_valides)
        return None


class Accompagnement(models.Model):
    """Système d'accompagnement personnalisé des étudiants"""
    TYPE_ACCOMPAGNEMENT_CHOICES = [
        ('pedagogique', 'Accompagnement pédagogique'),
        ('methodologique', 'Accompagnement méthodologique'),
        ('psychologique', 'Accompagnement psychologique'),
        ('orientation', 'Orientation professionnelle'),
        ('autre', 'Autre'),
    ]
    
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='accompagnements',
        verbose_name="Étudiant"
    )
    accompagnateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='accompagnements_effectues',
        verbose_name="Accompagnateur"
    )
    type_accompagnement = models.CharField(
        max_length=20,
        choices=TYPE_ACCOMPAGNEMENT_CHOICES,
        default='pedagogique',
        verbose_name="Type d'accompagnement"
    )
    
    # Suivi
    objectif = models.TextField(verbose_name="Objectif de l'accompagnement")
    actions_prevues = models.TextField(verbose_name="Actions prévues")
    actions_realisees = models.TextField(blank=True, null=True, verbose_name="Actions réalisées")
    resultats = models.TextField(blank=True, null=True, verbose_name="Résultats obtenus")
    
    # Dates
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin_prevue = models.DateField(null=True, blank=True, verbose_name="Date de fin prévue")
    date_fin_reelle = models.DateField(null=True, blank=True, verbose_name="Date de fin réelle")
    
    # Statut
    statut = models.CharField(
        max_length=20,
        choices=[
            ('en_cours', 'En cours'),
            ('termine', 'Terminé'),
            ('suspendu', 'Suspendu'),
        ],
        default='en_cours',
        verbose_name="Statut"
    )
    
    # Notes
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Accompagnement"
        verbose_name_plural = "Accompagnements"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Accompagnement {self.etudiant.username} - {self.get_type_accompagnement_display()}"


class SuiviIndividuel(models.Model):
    """Suivi individuel détaillé d'un étudiant"""
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='suivis_individuels',
        verbose_name="Étudiant"
    )
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='suivis_individuels',
        null=True,
        blank=True,
        verbose_name="Cours (optionnel)"
    )
    
    # Observations
    observations = models.TextField(verbose_name="Observations")
    difficultes_identifiees = models.TextField(
        blank=True,
        null=True,
        verbose_name="Difficultés identifiées"
    )
    forces_identifiees = models.TextField(
        blank=True,
        null=True,
        verbose_name="Forces identifiées"
    )
    
    # Plan d'action
    plan_action = models.TextField(
        blank=True,
        null=True,
        verbose_name="Plan d'action"
    )
    
    # Suivi
    prochaines_etapes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Prochaines étapes"
    )
    
    # Métadonnées
    date_entretien = models.DateTimeField(verbose_name="Date de l'entretien")
    responsable = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='suivis_individuels_effectues',
        verbose_name="Responsable"
    )
    
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Suivi individuel"
        verbose_name_plural = "Suivis individuels"
        ordering = ['-date_entretien']
    
    def __str__(self):
        return f"Suivi {self.etudiant.username} - {self.date_entretien.strftime('%Y-%m-%d')}"


# Modèles hérités pour compatibilité
class Stage(models.Model):
    """Stage d'un étudiant"""
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='stages')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    lieu = models.CharField(max_length=200, blank=True, null=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    valide = models.BooleanField(default=False)
    note = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    
    class Meta:
        verbose_name = "Stage"
        verbose_name_plural = "Stages"
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"{self.etudiant.username} - {self.titre}"


class EvaluationTheorique(models.Model):
    """Évaluation théorique (héritée pour compatibilité)"""
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='evaluations_theoriques')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True, blank=True, related_name='evaluations_theoriques')
    titre = models.CharField(max_length=200, default='Évaluation théorique')
    note = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(20)])
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Évaluation théorique"
        verbose_name_plural = "Évaluations théoriques"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.etudiant.username} - {self.titre}"


class EvaluationPratique(models.Model):
    """Évaluation pratique (héritée pour compatibilité)"""
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='evaluations_pratiques')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, null=True, blank=True, related_name='evaluations_pratiques')
    titre = models.CharField(max_length=200, default='Évaluation pratique')
    note = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(20)])
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Évaluation pratique"
        verbose_name_plural = "Évaluations pratiques"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.etudiant.username} - {self.titre}"


class Memoire(models.Model):
    """Mémoire d'un étudiant"""
    etudiant = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='memoires')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    note = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)]
    )
    date_soumission = models.DateField(null=True, blank=True)
    date_soutenance = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Mémoire"
        verbose_name_plural = "Mémoires"
        ordering = ['-date_soumission']
    
    def __str__(self):
        return f"{self.etudiant.username} - {self.titre}"
