# apps/evaluations/models_stage.py
"""
Modèles pour les évaluations de stage basées sur les jalons
Tous les enseignants peuvent faire des évaluations en stage sur la base des jalons
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Classe, Competence, CompetenceJalon
from apps.utilisateurs.models_programme_desmfmc import StageRotationDES, CSComUCentre


class EvaluationStage(models.Model):
    """
    Évaluation de stage basée sur les jalons de compétences.
    La grille comprend les jalons de la classe selon le lieu de stage.
    """
    
    TYPE_EVALUATION_CHOICES = [
        ('formative', 'Évaluation Formative'),
        ('sommative', 'Évaluation Sommative'),
        ('intermediaire', 'Évaluation Intermédiaire'),
        ('finale', 'Évaluation Finale de Stage'),
    ]
    
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('soumis', 'Soumis pour vérification'),
        ('verifie', 'Vérifié par la coordination'),
        ('disponible', 'Disponible pour l\'étudiant'),
        ('rejete', 'Rejeté'),
    ]
    
    # Informations de base
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='evaluations_stage',
        verbose_name="Étudiant"
    )
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='evaluations_stage',
        verbose_name="Classe"
    )
    
    # Stage concerné
    stage_rotation = models.ForeignKey(
        StageRotationDES,
        on_delete=models.CASCADE,
        related_name='evaluations',
        null=True,
        blank=True,
        verbose_name="Stage DES (si applicable)",
        help_text="Stage de rotation DES si l'évaluation concerne un stage DES"
    )
    structure_stage = models.ForeignKey(
        CSComUCentre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluations_stage',
        verbose_name="Structure de stage",
        help_text="CSCom-U ou autre structure où se déroule le stage"
    )
    
    # Enseignant/Superviseur
    enseignant = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='evaluations_stage_enseignant',
        verbose_name="Enseignant / Superviseur"
    )
    nom_superviseur = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Nom du superviseur",
        help_text="Si différent de l'enseignant connecté"
    )
    
    # Type et date d'évaluation
    type_evaluation = models.CharField(
        max_length=20,
        choices=TYPE_EVALUATION_CHOICES,
        default='formative',
        verbose_name="Type d'évaluation"
    )
    date_evaluation = models.DateField(
        default=timezone.now,
        verbose_name="Date de l'évaluation"
    )
    
    # Workflow
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='brouillon',
        verbose_name="Statut"
    )
    
    # Commentaire général et signature
    commentaire_general = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire général",
        help_text="Commentaire général sur l'évaluation du stage"
    )
    signature_responsable = models.ImageField(
        upload_to='evaluations/signatures/',
        blank=True,
        null=True,
        verbose_name="Signature du responsable de stage",
        help_text="Image de la signature du responsable"
    )
    cachet_structure = models.ImageField(
        upload_to='evaluations/cachets/',
        blank=True,
        null=True,
        verbose_name="Cachet de la structure",
        help_text="Image du cachet de la structure de stage"
    )
    
    # Vérification par coordination
    verifie_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluations_stage_verifiees',
        verbose_name="Vérifié par",
        help_text="Membre de la coordination qui a vérifié l'évaluation"
    )
    date_verification = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de vérification"
    )
    commentaire_verification = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire de vérification"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
    class Meta:
        verbose_name = "Évaluation de stage"
        verbose_name_plural = "Évaluations de stage"
        ordering = ['-date_evaluation', 'etudiant']
        indexes = [
            models.Index(fields=['etudiant', 'classe', 'date_evaluation']),
            models.Index(fields=['statut', 'date_evaluation']),
        ]
    
    def __str__(self):
        return f"Évaluation {self.etudiant.get_full_name() or self.etudiant.username} - {self.classe.nom} - {self.date_evaluation}"
    
    def get_structure_display(self):
        """Retourne le nom de la structure de stage"""
        if self.structure_stage:
            return str(self.structure_stage)
        elif self.stage_rotation and self.stage_rotation.centre:
            return str(self.stage_rotation.centre)
        return "Non spécifié"
    
    def get_superviseur_display(self):
        """Retourne le nom du superviseur"""
        if self.nom_superviseur:
            return self.nom_superviseur
        elif self.enseignant:
            return self.enseignant.get_full_name() or self.enseignant.username
        return "Non spécifié"
    
    def peut_etre_modifiee(self, utilisateur):
        """Vérifie si l'utilisateur peut modifier cette évaluation"""
        if self.statut == 'disponible':
            return False
        if utilisateur == self.enseignant:
            return True
        if utilisateur.is_superuser:
            return True
        return False
    
    def peut_etre_verifiee(self, utilisateur):
        """Vérifie si l'utilisateur peut vérifier cette évaluation"""
        if self.statut not in ['soumis', 'rejete']:
            return False
        # Seuls les membres de la coordination peuvent vérifier
        # TODO: Ajouter une vérification spécifique pour les membres de la coordination
        if utilisateur.is_superuser:
            return True
        return False


class EvaluationJalonStage(models.Model):
    """
    Évaluation d'un jalon spécifique dans le cadre d'une évaluation de stage.
    Chaque compétence peut avoir un commentaire.
    """
    
    NIVEAU_CHOICES = [
        ('1', '1 : Insuffisante'),
        ('2', '2 : Inconstante/Inférieure aux attentes'),
        ('3', '3 : Conforme aux attentes'),
        ('4', '4 : Dépasse nettement les attentes'),
        ('5', '5 : NA (Non Applicable)'),
    ]
    
    evaluation_stage = models.ForeignKey(
        EvaluationStage,
        on_delete=models.CASCADE,
        related_name='evaluations_jalons',
        verbose_name="Évaluation de stage"
    )
    jalon = models.ForeignKey(
        CompetenceJalon,
        on_delete=models.CASCADE,
        related_name='evaluations_stage',
        verbose_name="Jalon de compétence"
    )
    
    # Évaluation du jalon
    niveau = models.CharField(
        max_length=1,
        choices=NIVEAU_CHOICES,
        null=True,
        blank=True,
        verbose_name="Niveau atteint"
    )
    
    # Commentaire pour cette compétence
    commentaire = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire",
        help_text="Commentaire spécifique pour cette compétence/jalon"
    )
    
    # Ordre d'affichage (pour respecter l'ordre des jalons)
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    
    class Meta:
        verbose_name = "Évaluation jalon de stage"
        verbose_name_plural = "Évaluations jalons de stage"
        ordering = ['evaluation_stage', 'ordre', 'jalon__competence__libelle', 'jalon__ordre']
        unique_together = [['evaluation_stage', 'jalon']]
    
    def __str__(self):
        return f"{self.evaluation_stage} - {self.jalon.titre} ({self.get_niveau_display() if self.niveau else 'Non évalué'})"

