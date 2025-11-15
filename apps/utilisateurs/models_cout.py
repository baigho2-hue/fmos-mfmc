# apps/utilisateurs/models_cout.py
"""
Modèle pour gérer les coûts des formations
"""
from django.db import models
from django.core.validators import MinValueValidator


class CoutFormation(models.Model):
    """Modèle pour gérer les coûts des formations"""
    
    NIVEAU_CHOICES = [
        ('diu', 'DIU (Diplôme Inter-Universitaire)'),
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('annuel', 'Par année'),
        ('unique', 'Paiement unique'),
    ]
    
    MODALITE_PAIEMENT_CHOICES = [
        ('unique', 'Paiement en une seule tranche'),
        ('tranches', 'Paiement en plusieurs tranches'),
        ('annuel', 'Paiement annuel'),
    ]
    
    # Identifiant de la formation (slug)
    formation_slug = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Identifiant de la formation",
        help_text="Slug de la formation (ex: 'desmfmc', 'sante-communautaire')"
    )
    
    nom_formation = models.CharField(
        max_length=200,
        verbose_name="Nom de la formation",
        help_text="Nom complet de la formation"
    )
    
    # Coûts selon les niveaux
    niveau = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        default='unique',
        verbose_name="Niveau de formation"
    )
    
    # Coût principal
    cout_principal = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Coût principal (FCFA)",
        help_text="Coût principal de la formation"
    )
    
    # Coûts additionnels pour les formations avec plusieurs niveaux
    cout_diu = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Coût DIU (FCFA)",
        help_text="Coût pour le DIU (si applicable)"
    )
    
    cout_licence = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Coût Licence (FCFA)",
        help_text="Coût pour la Licence (si applicable)"
    )
    
    cout_master = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        default=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Coût Master (FCFA)",
        help_text="Coût pour le Master (si applicable)"
    )
    
    # Modalité de paiement
    modalite_paiement = models.CharField(
        max_length=20,
        choices=MODALITE_PAIEMENT_CHOICES,
        default='unique',
        verbose_name="Modalité de paiement"
    )
    
    # Informations supplémentaires
    conditions_paiement = models.TextField(
        blank=True,
        null=True,
        verbose_name="Conditions de paiement",
        help_text="Conditions spécifiques de paiement (ex: avant le début de l'évaluation finale)"
    )
    
    informations_supplementaires = models.TextField(
        blank=True,
        null=True,
        verbose_name="Informations supplémentaires",
        help_text="Informations complémentaires sur le coût et les modalités"
    )
    
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Désactiver pour masquer cette formation"
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    class Meta:
        verbose_name = "Coût de formation"
        verbose_name_plural = "Coûts des formations"
        ordering = ['nom_formation']
    
    def __str__(self):
        return f"{self.nom_formation} - {self.get_niveau_display()}"
    
    @property
    def a_plusieurs_niveaux(self):
        """Vérifie si la formation a plusieurs niveaux de coût"""
        return bool(self.cout_diu or self.cout_licence or self.cout_master)
    
    def a_plusieurs_niveaux_method(self):
        """Méthode pour l'admin"""
        return self.a_plusieurs_niveaux
    
    def get_cout_affichage(self):
        """Retourne le coût formaté pour l'affichage"""
        if self.a_plusieurs_niveaux:
            niveaux = []
            if self.cout_diu:
                niveaux.append(f"DIU: {self.cout_diu:,.0f} FCFA")
            if self.cout_licence:
                niveaux.append(f"Licence: {self.cout_licence:,.0f} FCFA")
            if self.cout_master:
                niveaux.append(f"Master: {self.cout_master:,.0f} FCFA")
            return " / ".join(niveaux)
        else:
            return f"{self.cout_principal:,.0f} FCFA"

