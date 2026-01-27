# apps/utilisateurs/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# Import des modèles de formation (éviter les imports circulaires)
def get_formation_models():
    """Fonction pour importer les modèles de formation de manière différée"""
    try:
        from .models_formation import Formation, Classe, Cours, ProgressionEtudiant, Planification
        return Formation, Classe, Cours, ProgressionEtudiant, Planification
    except ImportError:
        return None, None, None, None, None

class Utilisateur(AbstractUser):
    TYPE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('enseignant', 'Enseignant'),
    ]
    
    VERIFICATION_CHOICES = [
        ('email', 'E-mail'),
        ('sms', 'SMS'),
    ]
    
    NIVEAU_ACCES_CHOICES = [
        ('limite', 'Accès limité'),
        ('standard', 'Accès standard'),
        ('complet', 'Accès complet'),
    ]
    
    # Champs de base
    email = models.EmailField(unique=True, verbose_name="Adresse e-mail")
    email_verifie = models.BooleanField(default=False, verbose_name="Email vérifié")
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    
    # Type d'utilisateur
    type_utilisateur = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='etudiant',
        verbose_name="Type d'utilisateur"
    )
    
    # Champs pour étudiants
    classe = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Classe",
        help_text="Ex: Médecine 6, DESMFMC 1ère année, etc."
    )
    
    # Champs pour enseignants
    matieres = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Matières enseignées",
        help_text="Liste des matières séparées par des virgules"
    )
    classes_enseignees = models.ManyToManyField(
        'utilisateurs.Classe',
        blank=True,
        related_name='enseignants',
        verbose_name="Classes enseignées",
        help_text="Classes où cet enseignant dispense des cours"
    )
    niveau_acces = models.CharField(
        max_length=20,
        choices=NIVEAU_ACCES_CHOICES,
        default='standard',
        verbose_name="Niveau d'accès",
        help_text="Accès complet = accès à tout le contenu"
    )

    def __str__(self):
        return f"{self.username} ({self.email}) - {self.get_type_utilisateur_display()}"
    
    def est_etudiant(self):
        return self.type_utilisateur == 'etudiant'
    
    def est_enseignant(self):
        return self.type_utilisateur == 'enseignant'
    
    def a_acces_complet(self):
        return self.est_enseignant() and self.niveau_acces == 'complet'
    
    # Champ pour la coordination DESMFMC
    membre_coordination = models.BooleanField(
        default=False,
        verbose_name="Membre de la coordination DESMFMC",
        help_text="Accès au menu Administration pour gérer les formations, agenda, notes, etc."
    )
    
    def est_membre_coordination(self):
        """Vérifie si l'utilisateur est membre de la coordination DESMFMC"""
        return self.membre_coordination or self.is_superuser
    
    # Superviseur/CEC (Chargé d'Encadrement Clinique)
    superviseur_cec = models.BooleanField(
        default=False,
        verbose_name="Superviseur clinique / CEC",
        help_text="Accès aux évaluations de stages pour les superviseurs cliniques et CEC. Une personne peut être à la fois enseignant et superviseur/CEC."
    )
    centre_supervision = models.ForeignKey(
        'utilisateurs.CSComUCentre',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='superviseurs',
        verbose_name="Centre de supervision principal",
        help_text="Centre CSCom-U où ce superviseur/CEC est principalement assigné. Les évaluations seront automatiquement filtrées par ce centre."
    )
    
    # Double authentification (2FA)
    deux_facteurs_actives = models.BooleanField(
        default=False,
        verbose_name="Double authentification activée",
        help_text="Active la vérification par code email ou SMS pour les accès sensibles"
    )
    pref_verification = models.CharField(
        max_length=10,
        choices=VERIFICATION_CHOICES,
        default='email',
        verbose_name="Méthode de vérification préférée"
    )
    
    def est_superviseur_cec(self):
        """Vérifie si l'utilisateur est superviseur clinique ou CEC"""
        return self.superviseur_cec and self.est_enseignant()
    
    def get_classe_obj(self):
        """Retourne l'objet Classe associé à la classe de l'étudiant"""
        if not self.est_etudiant() or not self.classe:
            return None
        try:
            from .models_formation import Classe
            # Chercher la classe par nom (ex: "DESMFMC 1ère année")
            return Classe.objects.filter(nom__icontains=self.classe).first()
        except:
            return None
    
    def get_formation_obj(self):
        """Retourne l'objet Formation associé à l'étudiant"""
        classe_obj = self.get_classe_obj()
        if classe_obj:
            return classe_obj.formation
        return None
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateur"
        # Les champs groups et user_permissions sont hérités de AbstractUser
        # Le related_name est géré via les migrations


class CodeVerification(models.Model):
    """Modèle pour stocker les codes de vérification pour la connexion"""
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='codes_verification')
    code = models.CharField(max_length=6, verbose_name="Code de vérification")
    cree_le = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    expire_le = models.DateTimeField(verbose_name="Expire le")
    utilise = models.BooleanField(default=False, verbose_name="Utilisé")
    
    class Meta:
        verbose_name = "Code de vérification"
        verbose_name_plural = "Codes de vérification"
        ordering = ['-cree_le']
    
    def __str__(self):
        return f"Code {self.code} pour {self.user.username} - {'Utilisé' if self.utilise else 'Actif'}"
    
    def est_valide(self):
        from django.utils import timezone
        return not self.utilise and timezone.now() < self.expire_le


class Code2FA(models.Model):
    """Modèle pour stocker les codes de double authentification (2FA)"""
    user = models.ForeignKey(
        Utilisateur, 
        on_delete=models.CASCADE, 
        related_name='codes_2fa',
        verbose_name="Utilisateur"
    )
    code = models.CharField(
        max_length=6, 
        verbose_name="Code de vérification 2FA"
    )
    cree_le = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Créé le"
    )
    expire_le = models.DateTimeField(
        verbose_name="Expire le"
    )
    utilise = models.BooleanField(
        default=False, 
        verbose_name="Utilisé"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="Adresse IP"
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="User Agent"
    )
    
    class Meta:
        verbose_name = "Code 2FA"
        verbose_name_plural = "Codes 2FA"
        ordering = ['-cree_le']
    
    def __str__(self):
        return f"Code 2FA {self.code} pour {self.user.username} - {'Utilisé' if self.utilise else 'Actif'}"
    
    def est_valide(self):
        from django.utils import timezone
        return not self.utilise and timezone.now() < self.expire_le
