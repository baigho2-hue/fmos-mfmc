from django.db import models
from django.conf import settings

# -------------------------
# Formation principale
# -------------------------
class FormationExtra(models.Model):
    TYPE_FORMATION = [
        ('certifiante','Certifiante'),
        ('non_certifiante','Non certifiante')
    ]
    TARIFICATION = [
        ('gratuite','Gratuite'),
        ('payante','Payante')
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    type_formation = models.CharField(max_length=20, choices=TYPE_FORMATION)
    tarification = models.CharField(max_length=20, choices=TARIFICATION)
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_debut = models.DateField()
    date_fin = models.DateField()
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

# -------------------------
# Inscription à une formation
# -------------------------
class InscriptionExtra(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    formation = models.ForeignKey('FormationExtra', on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.formation.titre}"

# -------------------------
# Module d’une formation
# -------------------------
class ModuleExtra(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    formation_extra = models.ForeignKey('FormationExtra', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.titre} ({self.formation_extra.titre})"

# -------------------------
# Paiement lié à une inscription
# -------------------------
class PaiementExtra(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('espece', 'Espèces'),
        ('bancaire', 'Virement bancaire'),
        ('orange_money', 'Orange Money'),
    ]
    
    inscription_extra = models.ForeignKey('InscriptionExtra', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES, default='bancaire')
    compte_bancaire = models.ForeignKey(
        'utilisateurs.CompteBancaire',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='paiements_extra',
        verbose_name='Compte bancaire',
        help_text="Compte bancaire sur lequel le paiement a été effectué (si mode bancaire)"
    )
    date_paiement = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False)
    reference_paiement = models.CharField(max_length=100, blank=True, null=True, help_text="Référence du paiement (numéro de transaction, etc.)")

    def __str__(self):
        return f"{self.inscription_extra} - {self.montant} FCFA ({self.get_mode_paiement_display()})"

# -------------------------
# Certificat délivré après réussite
# -------------------------
class CertificatExtra(models.Model):
    inscription = models.OneToOneField('InscriptionExtra', on_delete=models.CASCADE)
    date_emission = models.DateField(auto_now_add=True)
    code_certificat = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Certificat {self.code_certificat} - {self.inscription.utilisateur.username}"
