# apps/utilisateurs/models_med6.py
"""
Modèle pour les étudiants de Médecine 6ème année
"""
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta


class ListeMed6(models.Model):
    """
    Modèle pour gérer les différentes listes d'étudiants Med 6 par année universitaire
    """
    annee_universitaire = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Année universitaire",
        help_text="Ex: 2024-2025"
    )
    date_cloture = models.DateField(
        verbose_name="Date de clôture de l'année universitaire",
        help_text="Date de fin de l'année universitaire"
    )
    date_import = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'import"
    )
    fichier_source = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Fichier source",
        help_text="Nom du fichier Excel importé"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Liste active",
        help_text="Une seule liste peut être active à la fois"
    )
    nombre_etudiants = models.IntegerField(
        default=0,
        verbose_name="Nombre d'étudiants"
    )
    
    class Meta:
        verbose_name = "Liste Med 6"
        verbose_name_plural = "Listes Med 6"
        ordering = ['-annee_universitaire']
    
    def __str__(self):
        return f"Liste Med 6 - {self.annee_universitaire}"
    
    def est_expiree(self):
        """
        Vérifie si la liste est expirée (3 mois après la clôture)
        """
        if not self.date_cloture:
            return False
        date_expiration = self.date_cloture + timedelta(days=90)  # 3 mois
        return timezone.now().date() > date_expiration
    
    def jours_avant_expiration(self):
        """
        Retourne le nombre de jours avant expiration (négatif si expirée)
        """
        if not self.date_cloture:
            return None
        date_expiration = self.date_cloture + timedelta(days=90)
        jours = (date_expiration - timezone.now().date()).days
        return jours


class EtudiantMed6(models.Model):
    """
    Modèle pour stocker les informations des étudiants de 6ème année de médecine
    qui ont droit à l'accès gratuit aux cours Médecine 6
    
    IMPORTANT: Ce cours est réservé UNIQUEMENT aux étudiants en 6ème année de médecine.
    L'accès est validé via la liste Excel officielle (matricule, nom, prénom).
    """
    liste = models.ForeignKey(
        ListeMed6,
        on_delete=models.CASCADE,
        related_name='etudiants',
        verbose_name="Liste d'appartenance",
        help_text="Liste Med 6 à laquelle appartient cet étudiant",
        blank=True,
        null=True  # Temporairement nullable pour la migration
    )
    matricule = models.CharField(
        max_length=50,
        verbose_name="Matricule",
        help_text="Numéro de matricule de l'étudiant (2ème colonne du fichier Excel)"
    )
    prenom = models.CharField(
        max_length=100,
        verbose_name="Prénom",
        help_text="Prénom de l'étudiant (3ème colonne du fichier Excel)"
    )
    nom = models.CharField(
        max_length=100,
        verbose_name="Nom",
        help_text="Nom de l'étudiant (4ème colonne du fichier Excel)"
    )
    numero_carte_scolaire = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Numéro de Carte Scolaire",
        help_text="Numéro de la Carte Scolaire (si disponible)"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Désactiver pour retirer l'accès gratuit"
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    # Lien vers l'utilisateur si un compte a été créé
    utilisateur = models.OneToOneField(
        'utilisateurs.Utilisateur',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='etudiant_med6',
        verbose_name="Compte utilisateur associé"
    )
    
    class Meta:
        verbose_name = "Étudiant Médecine 6"
        verbose_name_plural = "Étudiants Médecine 6"
        ordering = ['nom', 'prenom']
        unique_together = [['liste', 'matricule']]  # Matricule unique par liste
        indexes = [
            models.Index(fields=['matricule']),
            models.Index(fields=['nom', 'prenom']),
            models.Index(fields=['liste', 'actif']),
        ]
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.matricule})"
    
    def nom_complet(self):
        """Retourne le nom complet de l'étudiant"""
        return f"{self.prenom} {self.nom}".strip()
    
    def verifier_identite(self, matricule, prenom, nom):
        """
        Vérifie si les informations fournies correspondent à cet étudiant
        Comparaison insensible à la casse et aux accents
        """
        import unicodedata
        
        def normalize_text(text):
            """Normalise le texte pour la comparaison"""
            if not text:
                return ""
            # Convertir en minuscules et supprimer les accents
            text = unicodedata.normalize('NFD', str(text).lower().strip())
            text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
            return text
        
        matricule_match = normalize_text(self.matricule) == normalize_text(matricule)
        prenom_match = normalize_text(self.prenom) == normalize_text(prenom)
        nom_match = normalize_text(self.nom) == normalize_text(nom)
        
        return matricule_match and prenom_match and nom_match
    
    @classmethod
    def get_etudiant_actif(cls, matricule, prenom, nom):
        """
        Récupère un étudiant actif avec une liste non expirée
        VALIDATION STRICTE: Le matricule, le nom ET le prénom doivent tous correspondre
        
        Args:
            matricule: Numéro de matricule de l'étudiant
            prenom: Prénom de l'étudiant
            nom: Nom de l'étudiant
        
        Returns:
            EtudiantMed6 si trouvé et validé, None sinon
        """
        # Normaliser les entrées
        matricule = str(matricule).strip() if matricule else ""
        prenom = str(prenom).strip() if prenom else ""
        nom = str(nom).strip() if nom else ""
        
        # Vérifier que tous les champs sont remplis
        if not matricule or not prenom or not nom:
            return None
        
        # Chercher dans les listes actives et non expirées
        listes_actives = ListeMed6.objects.filter(active=True)
        listes_valides = [l for l in listes_actives if not l.est_expiree()]
        
        if not listes_valides:
            return None
        
        # Chercher l'étudiant dans les listes valides
        # IMPORTANT: On cherche d'abord par matricule, puis on valide nom ET prénom
        for liste in listes_valides:
            try:
                etudiant = cls.objects.get(
                    liste=liste,
                    matricule__iexact=matricule,  # Recherche insensible à la casse
                    actif=True
                )
                # VALIDATION STRICTE: Vérifier que le matricule, nom ET prénom correspondent
                if etudiant.verifier_identite(matricule, prenom, nom):
                    return etudiant
            except cls.DoesNotExist:
                continue
            except cls.MultipleObjectsReturned:
                # Si plusieurs étudiants avec le même matricule, chercher celui qui correspond
                etudiants = cls.objects.filter(
                    liste=liste,
                    matricule__iexact=matricule,
                    actif=True
                )
                for etudiant in etudiants:
                    if etudiant.verifier_identite(matricule, prenom, nom):
                        return etudiant
        
        return None

