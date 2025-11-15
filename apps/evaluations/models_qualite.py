# apps/evaluations/models_qualite.py
"""
Modèles pour les indicateurs de qualité et d'efficacité des formations
Système d'assurance qualité adapté aux standards internationaux
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Formation, Classe, Cours


class IndicateurQualite(models.Model):
    """Indicateurs de qualité pour évaluer l'efficacité des formations"""
    CATEGORIE_CHOICES = [
        ('pedagogique', 'Pédagogique'),
        ('organisationnel', 'Organisationnel'),
        ('satisfaction', 'Satisfaction'),
        ('resultats', 'Résultats'),
        ('ressources', 'Ressources'),
        ('accompagnement', 'Accompagnement'),
    ]
    
    nom = models.CharField(max_length=200, unique=True, verbose_name="Nom de l'indicateur")
    description = models.TextField(verbose_name="Description")
    categorie = models.CharField(
        max_length=20,
        choices=CATEGORIE_CHOICES,
        default='pedagogique',
        verbose_name="Catégorie"
    )
    formule_calcul = models.TextField(
        blank=True,
        null=True,
        verbose_name="Formule de calcul",
        help_text="Description de la méthode de calcul"
    )
    cible = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valeur cible",
        help_text="Valeur cible à atteindre"
    )
    seuil_alerte = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Seuil d'alerte",
        help_text="Valeur en dessous de laquelle une alerte est déclenchée"
    )
    unite = models.CharField(
        max_length=50,
        default='%',
        verbose_name="Unité de mesure"
    )
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Indicateur de qualité"
        verbose_name_plural = "Indicateurs de qualité"
        ordering = ['categorie', 'nom']
    
    def __str__(self):
        return f"{self.get_categorie_display()}: {self.nom}"


class MesureQualite(models.Model):
    """Mesures effectives des indicateurs de qualité"""
    indicateur = models.ForeignKey(
        IndicateurQualite,
        on_delete=models.CASCADE,
        related_name='mesures',
        verbose_name="Indicateur"
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='mesures_qualite',
        null=True,
        blank=True,
        verbose_name="Formation"
    )
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='mesures_qualite',
        null=True,
        blank=True,
        verbose_name="Classe"
    )
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='mesures_qualite',
        null=True,
        blank=True,
        verbose_name="Cours"
    )
    
    valeur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valeur mesurée"
    )
    periode_debut = models.DateField(verbose_name="Période début")
    periode_fin = models.DateField(verbose_name="Période fin")
    
    # Analyse
    analyse = models.TextField(
        blank=True,
        null=True,
        verbose_name="Analyse",
        help_text="Analyse de la mesure"
    )
    actions_correctives = models.TextField(
        blank=True,
        null=True,
        verbose_name="Actions correctives",
        help_text="Actions à entreprendre si nécessaire"
    )
    
    # Métadonnées
    date_mesure = models.DateTimeField(auto_now_add=True, verbose_name="Date de mesure")
    mesure_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='mesures_qualite_effectuees',
        verbose_name="Mesuré par"
    )
    
    class Meta:
        verbose_name = "Mesure de qualité"
        verbose_name_plural = "Mesures de qualité"
        ordering = ['-date_mesure']
    
    def __str__(self):
        return f"{self.indicateur.nom}: {self.valeur} {self.indicateur.unite}"
    
    @property
    def statut(self):
        """Détermine le statut par rapport à la cible et au seuil d'alerte"""
        if self.indicateur.cible and self.valeur >= self.indicateur.cible:
            return 'atteint'
        elif self.indicateur.seuil_alerte and self.valeur < self.indicateur.seuil_alerte:
            return 'alerte'
        else:
            return 'en_cours'


class RapportQualite(models.Model):
    """Rapports périodiques de qualité des formations"""
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='rapports_qualite',
        verbose_name="Formation"
    )
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='rapports_qualite',
        null=True,
        blank=True,
        verbose_name="Classe (optionnel)"
    )
    
    # Période
    periode_debut = models.DateField(verbose_name="Période début")
    periode_fin = models.DateField(verbose_name="Période fin")
    
    # Synthèse
    synthese = models.TextField(verbose_name="Synthèse")
    points_forts = models.TextField(verbose_name="Points forts")
    points_amelioration = models.TextField(verbose_name="Points à améliorer")
    recommandations = models.TextField(verbose_name="Recommandations")
    
    # Indicateurs clés
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
    satisfaction_moyenne = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Satisfaction moyenne (0-5)"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    auteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='rapports_qualite_crees',
        verbose_name="Auteur"
    )
    valide = models.BooleanField(default=False, verbose_name="Validé")
    valide_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rapports_qualite_valides',
        verbose_name="Validé par"
    )
    date_validation = models.DateTimeField(null=True, blank=True, verbose_name="Date de validation")
    
    class Meta:
        verbose_name = "Rapport de qualité"
        verbose_name_plural = "Rapports de qualité"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Rapport {self.formation.nom} - {self.periode_debut}"


class PlanAmelioration(models.Model):
    """Plans d'amélioration continue basés sur les évaluations"""
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='plans_amelioration',
        verbose_name="Formation"
    )
    rapport_qualite = models.ForeignKey(
        RapportQualite,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='plans_amelioration',
        verbose_name="Rapport de qualité source"
    )
    
    # Objectifs
    objectif = models.TextField(verbose_name="Objectif d'amélioration")
    actions_prevues = models.TextField(verbose_name="Actions prévues")
    responsables = models.ManyToManyField(
        Utilisateur,
        related_name='plans_amelioration_responsables',
        limit_choices_to={'type_utilisateur': 'enseignant'},
        verbose_name="Responsables"
    )
    
    # Planning
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin_prevue = models.DateField(verbose_name="Date de fin prévue")
    date_fin_reelle = models.DateField(null=True, blank=True, verbose_name="Date de fin réelle")
    
    # Suivi
    statut = models.CharField(
        max_length=20,
        choices=[
            ('planifie', 'Planifié'),
            ('en_cours', 'En cours'),
            ('termine', 'Terminé'),
            ('suspendu', 'Suspendu'),
        ],
        default='planifie',
        verbose_name="Statut"
    )
    resultats = models.TextField(blank=True, null=True, verbose_name="Résultats obtenus")
    indicateurs_suivi = models.ManyToManyField(
        IndicateurQualite,
        related_name='plans_amelioration',
        blank=True,
        verbose_name="Indicateurs de suivi"
    )
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        related_name='plans_amelioration_crees',
        verbose_name="Créé par"
    )
    
    class Meta:
        verbose_name = "Plan d'amélioration"
        verbose_name_plural = "Plans d'amélioration"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Plan d'amélioration {self.formation.nom} - {self.date_debut}"

