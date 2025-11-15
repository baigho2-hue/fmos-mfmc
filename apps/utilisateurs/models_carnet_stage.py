# apps/utilisateurs/models_carnet_stage.py
"""
Modèles pour le carnet de stage du DESMFMC
Suivi et évaluation des stages sur 4 ans avec compétences et jalons
"""
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Utilisateur
from .models_programme_desmfmc import JalonProgramme, StagePremiereAnnee, StageRotationDES
from .models_formation import Competence, Classe


class CarnetStage(models.Model):
    """Carnet de stage principal pour un étudiant du DESMFMC"""
    
    etudiant = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='carnet_stage',
        limit_choices_to={'type_utilisateur': 'etudiant'},
        verbose_name="Étudiant"
    )
    annee_scolaire = models.CharField(
        max_length=20,
        verbose_name="Année scolaire",
        help_text="Ex: 2024-2025"
    )
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Dernière modification")
    actif = models.BooleanField(default=True, verbose_name="Carnet actif")
    
    class Meta:
        verbose_name = "Carnet de stage"
        verbose_name_plural = "Carnets de stage"
        ordering = ['-annee_scolaire', 'etudiant__username']
    
    def __str__(self):
        return f"Carnet de stage - {self.etudiant.username} ({self.annee_scolaire})"
    
    def get_stages_annee_1(self):
        """Retourne tous les stages de 1ère année"""
        return self.evaluations_stages.filter(annee=1).order_by('date_debut')
    
    def get_stages_annee_2(self):
        """Retourne tous les stages de 2ème année"""
        return self.evaluations_stages.filter(annee=2).order_by('date_debut')
    
    def get_stages_annee_3(self):
        """Retourne tous les stages de 3ème année"""
        return self.evaluations_stages.filter(annee=3).order_by('date_debut')
    
    def get_stages_annee_4(self):
        """Retourne tous les stages de 4ème année"""
        return self.evaluations_stages.filter(annee=4).order_by('date_debut')


class EvaluationStage(models.Model):
    """Évaluation d'un stage dans le carnet"""
    
    TYPE_STAGE_CHOICES = [
        ('hospitalier_annee1', 'Stage hospitalier (Année 1)'),
        ('cscom_urbain', 'Stage CSCom-U urbain'),
        ('cscom_rural', 'Stage CSCom-U rural'),
        ('autre', 'Autre stage'),
    ]
    
    carnet = models.ForeignKey(
        CarnetStage,
        on_delete=models.CASCADE,
        related_name='evaluations_stages',
        verbose_name="Carnet de stage"
    )
    annee = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name="Année du DES (1-4)"
    )
    type_stage = models.CharField(
        max_length=30,
        choices=TYPE_STAGE_CHOICES,
        verbose_name="Type de stage"
    )
    
    # Lien avec les stages existants (optionnel)
    stage_annee1 = models.ForeignKey(
        StagePremiereAnnee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluations_carnet',
        verbose_name="Stage 1ère année (si applicable)"
    )
    stage_rotation = models.ForeignKey(
        StageRotationDES,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluations_carnet',
        verbose_name="Stage rotation DES (si applicable)"
    )
    
    # Informations du stage
    lieu_stage = models.CharField(
        max_length=300,
        verbose_name="Lieu du stage"
    )
    service_stage = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Service / Département"
    )
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    duree_semaines = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
        verbose_name="Durée (en semaines)"
    )
    
    # Responsables
    maitre_stage = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stages_maitre',
        limit_choices_to={'type_utilisateur': 'enseignant'},
        verbose_name="Maître de stage"
    )
    maitre_stage_nom = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Nom du maître de stage (si non-enseignant)"
    )
    maitre_stage_titre = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Titre du maître de stage"
    )
    
    # Évaluation globale
    note_globale = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Note globale (sur 20)"
    )
    appreciation_globale = models.TextField(
        blank=True,
        verbose_name="Appréciation globale"
    )
    points_forts = models.TextField(
        blank=True,
        verbose_name="Points forts"
    )
    points_amelioration = models.TextField(
        blank=True,
        verbose_name="Points à améliorer"
    )
    
    # Validation
    valide = models.BooleanField(
        default=False,
        verbose_name="Stage validé"
    )
    date_validation = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de validation"
    )
    valide_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stages_valides',
        limit_choices_to={'type_utilisateur__in': ['enseignant', 'coordination']},
        verbose_name="Validé par"
    )
    
    # Évaluation par superviseur/CEC
    evalue_par_superviseur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluations_stages_superviseur',
        limit_choices_to={'type_utilisateur': 'enseignant'},
        verbose_name="Évalué par (Superviseur/CEC)"
    )
    date_evaluation_superviseur = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'évaluation par le superviseur"
    )
    
    # Dates
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Évaluation de stage"
        verbose_name_plural = "Évaluations de stages"
        ordering = ['annee', 'date_debut']
    
    def __str__(self):
        return f"Évaluation {self.annee}ème année - {self.get_type_stage_display()} ({self.lieu_stage})"
    
    def clean(self):
        if self.date_fin and self.date_debut and self.date_fin < self.date_debut:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")
        
        if self.duree_semaines is None and self.date_debut and self.date_fin:
            from datetime import timedelta
            delta = self.date_fin - self.date_debut
            self.duree_semaines = max(1, delta.days // 7)
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class EvaluationCompetence(models.Model):
    """Évaluation d'une compétence spécifique lors d'un stage"""
    
    NIVEAU_CHOICES = [
        (1, '1 - Non acquis'),
        (2, '2 - En cours d\'acquisition'),
        (3, '3 - Acquis'),
        (4, '4 - Maîtrisé'),
    ]
    
    evaluation_stage = models.ForeignKey(
        EvaluationStage,
        on_delete=models.CASCADE,
        related_name='evaluations_competences',
        verbose_name="Évaluation de stage"
    )
    competence = models.ForeignKey(
        Competence,
        on_delete=models.CASCADE,
        related_name='evaluations_stages',
        verbose_name="Compétence"
    )
    jalon = models.ForeignKey(
        JalonProgramme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluations_competences',
        verbose_name="Jalon associé"
    )
    
    niveau_acquisition = models.IntegerField(
        choices=NIVEAU_CHOICES,
        null=True,
        blank=True,
        verbose_name="Niveau d'acquisition"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Commentaire sur la compétence"
    )
    observations = models.TextField(
        blank=True,
        verbose_name="Observations spécifiques"
    )
    
    # Évaluation par le maître de stage
    evalue_par_maitre = models.BooleanField(
        default=False,
        verbose_name="Évalué par le maître de stage"
    )
    date_evaluation = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'évaluation"
    )
    
    class Meta:
        verbose_name = "Évaluation de compétence"
        verbose_name_plural = "Évaluations de compétences"
        unique_together = ['evaluation_stage', 'competence']
        ordering = ['competence__libelle']
    
    def __str__(self):
        niveau = self.get_niveau_acquisition_display() if self.niveau_acquisition else "Non évalué"
        return f"{self.competence.libelle} - {niveau}"


class TableauEvaluationClasse(models.Model):
    """Tableau d'évaluation par classe et compétence (utilisé comme jalon)"""
    
    carnet = models.ForeignKey(
        CarnetStage,
        on_delete=models.CASCADE,
        related_name='tableaux_evaluation',
        verbose_name="Carnet de stage"
    )
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='tableaux_evaluation',
        verbose_name="Classe"
    )
    jalon = models.ForeignKey(
        JalonProgramme,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tableaux_evaluation',
        verbose_name="Jalon associé"
    )
    annee = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name="Année du DES"
    )
    
    # Compétences évaluées dans ce tableau
    competences = models.ManyToManyField(
        Competence,
        through='EvaluationCompetenceTableau',
        related_name='tableaux_evaluation',
        verbose_name="Compétences évaluées"
    )
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Tableau d'évaluation par classe"
        verbose_name_plural = "Tableaux d'évaluation par classe"
        unique_together = ['carnet', 'classe', 'annee']
        ordering = ['annee', 'classe__nom']
    
    def __str__(self):
        return f"Tableau {self.classe.nom} - Année {self.annee}"


class EvaluationCompetenceTableau(models.Model):
    """Évaluation d'une compétence dans un tableau d'évaluation"""
    
    NIVEAU_CHOICES = [
        (1, '1 - Non acquis'),
        (2, '2 - En cours d\'acquisition'),
        (3, '3 - Acquis'),
        (4, '4 - Maîtrisé'),
    ]
    
    tableau = models.ForeignKey(
        TableauEvaluationClasse,
        on_delete=models.CASCADE,
        related_name='evaluations_competences_tableau'
    )
    competence = models.ForeignKey(
        Competence,
        on_delete=models.CASCADE,
        related_name='evaluations_tableaux'
    )
    
    niveau_acquisition = models.IntegerField(
        choices=NIVEAU_CHOICES,
        null=True,
        blank=True,
        verbose_name="Niveau d'acquisition"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Commentaire"
    )
    date_evaluation = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'évaluation"
    )
    
    class Meta:
        verbose_name = "Évaluation compétence dans tableau"
        verbose_name_plural = "Évaluations compétences dans tableaux"
        unique_together = ['tableau', 'competence']
    
    def __str__(self):
        niveau = self.get_niveau_acquisition_display() if self.niveau_acquisition else "Non évalué"
        return f"{self.competence.libelle} - {niveau}"


class ProclamationResultats(models.Model):
    """Modèle pour gérer la proclamation des résultats par classe"""
    
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='proclamations_resultats',
        verbose_name="Classe"
    )
    annee_scolaire = models.CharField(
        max_length=20,
        verbose_name="Année scolaire",
        help_text="Ex: 2024-2025"
    )
    date_proclamation = models.DateField(
        verbose_name="Date de proclamation des résultats"
    )
    proclame_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proclamations_effectuees',
        limit_choices_to={'membre_coordination': True},
        verbose_name="Proclamé par"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Proclamation active"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Proclamation des résultats"
        verbose_name_plural = "Proclamations des résultats"
        unique_together = ['classe', 'annee_scolaire']
        ordering = ['-date_proclamation', 'classe__nom']
    
    def __str__(self):
        return f"Proclamation {self.classe.nom} - {self.annee_scolaire}"
