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
        ('du', 'DU (Diplôme Universitaire)'),
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
    
    # Bourse
    bourse_offerte = models.BooleanField(
        default=False,
        verbose_name="Bourse offerte",
        help_text="Si une bourse est offerte, le coût sera doublé"
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
    
    def get_cout_principal_calcule(self):
        """Retourne le coût principal calculé (doublé si bourse offerte)"""
        from decimal import Decimal
        cout = Decimal(str(self.cout_principal))
        if self.bourse_offerte:
            cout = cout * Decimal('2')
        return cout
    
    def get_cout_diu_calcule(self):
        """Retourne le coût DIU calculé (doublé si bourse offerte)"""
        from decimal import Decimal
        if not self.cout_diu:
            return None
        cout = Decimal(str(self.cout_diu))
        if self.bourse_offerte:
            cout = cout * Decimal('2')
        return cout
    
    def get_cout_licence_calcule(self):
        """Retourne le coût Licence calculé (doublé si bourse offerte)"""
        from decimal import Decimal
        if not self.cout_licence:
            return None
        cout = Decimal(str(self.cout_licence))
        if self.bourse_offerte:
            cout = cout * Decimal('2')
        return cout
    
    def get_cout_master_calcule(self):
        """Retourne le coût Master calculé (doublé si bourse offerte)"""
        from decimal import Decimal
        if not self.cout_master:
            return None
        cout = Decimal(str(self.cout_master))
        if self.bourse_offerte:
            cout = cout * Decimal('2')
        return cout
    
    def get_cout_affichage(self):
        """Retourne le coût formaté pour l'affichage (avec bourse si applicable)"""
        if self.a_plusieurs_niveaux:
            niveaux = []
            cout_diu = self.get_cout_diu_calcule()
            cout_licence = self.get_cout_licence_calcule()
            cout_master = self.get_cout_master_calcule()
            
            if cout_diu:
                niveaux.append(f"DIU: {cout_diu:,.0f} FCFA")
            if cout_licence:
                niveaux.append(f"Licence: {cout_licence:,.0f} FCFA")
            if cout_master:
                niveaux.append(f"Master: {cout_master:,.0f} FCFA")
            
            affichage = " / ".join(niveaux)
            if self.bourse_offerte:
                affichage += " (avec bourse)"
            return affichage
        else:
            cout = self.get_cout_principal_calcule()
            affichage = f"{cout:,.0f} FCFA"
            if self.bourse_offerte:
                affichage += " (avec bourse)"
            return affichage

