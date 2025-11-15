# apps/utilisateurs/models_documents.py
"""
Modèles pour les documents partagés : lettres d'informations, modèles pédagogiques
"""
from django.db import models
from django.utils import timezone
from django.conf import settings
from .models import Utilisateur


class LettreInformation(models.Model):
    """Modèle représentant une lettre d'information envoyée aux étudiants"""
    TYPE_LETTRE_CHOICES = [
        ('information', 'Information générale'),
        ('annonce', 'Annonce importante'),
        ('rappel', 'Rappel'),
        ('convocation', 'Convocation'),
        ('resultat', 'Résultats'),
        ('autre', 'Autre'),
    ]
    
    titre = models.CharField(max_length=200, verbose_name='Titre de la lettre')
    type_lettre = models.CharField(
        max_length=20,
        choices=TYPE_LETTRE_CHOICES,
        default='information',
        verbose_name='Type de lettre'
    )
    contenu = models.TextField(verbose_name='Contenu de la lettre')
    destinataires = models.ManyToManyField(
        Utilisateur,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='lettres_recues',
        verbose_name='Destinataires',
        help_text='Sélectionner les étudiants destinataires. Laisser vide pour tous les étudiants.'
    )
    classe_cible = models.ForeignKey(
        'utilisateurs.Classe',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='lettres_information',
        verbose_name='Classe cible',
        help_text='Si spécifiée, la lettre sera envoyée à tous les étudiants de cette classe'
    )
    auteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'type_utilisateur__in': ['enseignant', 'coordination']},
        related_name='lettres_envoyees',
        verbose_name='Auteur'
    )
    date_envoi = models.DateTimeField(default=timezone.now, verbose_name='Date d\'envoi')
    envoye_par_email = models.BooleanField(default=False, verbose_name='Envoyé par email')
    piece_jointe = models.FileField(
        blank=True,
        null=True,
        upload_to='lettres_information/',
        verbose_name='Pièce jointe'
    )
    actif = models.BooleanField(default=True, verbose_name='Actif')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Lettre d\'information'
        verbose_name_plural = 'Lettres d\'information'
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.titre} - {self.get_type_lettre_display()} ({self.date_envoi.strftime('%d/%m/%Y')})"
    
    def get_destinataires_list(self):
        """Retourne la liste des destinataires"""
        if self.destinataires.exists():
            return self.destinataires.all()
        elif self.classe_cible:
            return Utilisateur.objects.filter(
                type_utilisateur='etudiant',
                is_active=True,
                classe__icontains=self.classe_cible.nom
            )
        else:
            return Utilisateur.objects.filter(
                type_utilisateur='etudiant',
                is_active=True
            )


class ModelePedagogique(models.Model):
    """Modèle représentant un modèle pédagogique téléversé par la coordination"""
    TYPE_MODELE_CHOICES = [
        ('plan_cours', 'Plan de cours'),
        ('fiche_pedagogique', 'Fiche pédagogique'),
        ('grille_evaluation', 'Grille d\'évaluation'),
        ('template_presentation', 'Template de présentation'),
        ('guide_enseignant', 'Guide enseignant'),
        ('autre', 'Autre'),
    ]
    
    titre = models.CharField(max_length=200, verbose_name='Titre du modèle')
    type_modele = models.CharField(
        max_length=30,
        choices=TYPE_MODELE_CHOICES,
        default='plan_cours',
        verbose_name='Type de modèle'
    )
    description = models.TextField(verbose_name='Description')
    fichier = models.FileField(
        upload_to='modeles_pedagogiques/',
        verbose_name='Fichier'
    )
    auteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'type_utilisateur': 'coordination'},
        related_name='modeles_pedagogiques_crees',
        verbose_name='Auteur'
    )
    visible_enseignants = models.BooleanField(
        default=True,
        verbose_name='Visible par les enseignants'
    )
    actif = models.BooleanField(default=True, verbose_name='Actif')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Modèle pédagogique'
        verbose_name_plural = 'Modèles pédagogiques'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.titre} ({self.get_type_modele_display()})"
    
    def get_file_extension(self):
        """Retourne l'extension du fichier"""
        if self.fichier:
            return self.fichier.name.split('.')[-1].lower()
        return None


class SignatureCoordination(models.Model):
    """Modèle pour stocker les informations de signature de la coordination pour les documents administratifs"""
    nom_signataire = models.CharField(
        max_length=200,
        verbose_name='Nom du signataire',
        help_text='Nom complet de la personne autorisée à signer les documents'
    )
    prenom_signataire = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Prénom du signataire',
        help_text='Prénom du signataire (optionnel, sera combiné avec le nom)'
    )
    titre_signataire = models.CharField(
        max_length=200,
        verbose_name='Titre/Fonction',
        help_text='Titre ou fonction du signataire (ex: Directeur du Programme DESMFMC)',
        default='Coordonnateur DESMFMC'
    )
    cachet = models.ImageField(
        upload_to='signatures/',
        blank=True,
        null=True,
        verbose_name='Cachet de la coordination',
        help_text='Image du cachet officiel de la coordination'
    )
    est_directeur = models.BooleanField(
        default=False,
        verbose_name='Directeur du Programme',
        help_text='Cocher si cette personne est le Directeur du Programme'
    )
    actif = models.BooleanField(
        default=True,
        verbose_name='Actif',
        help_text='Utiliser cette signature pour les nouveaux documents'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Signature de la coordination'
        verbose_name_plural = 'Signatures de la coordination'
        ordering = ['-est_directeur', '-actif', '-date_creation']
    
    def __str__(self):
        nom_complet = f"{self.nom_signataire}"
        if self.prenom_signataire:
            nom_complet = f"{self.nom_signataire}, {self.prenom_signataire}"
        return f"{nom_complet} - {self.titre_signataire}"
    
    def get_nom_complet(self):
        """Retourne le nom complet du signataire"""
        if self.prenom_signataire:
            return f"{self.nom_signataire}, {self.prenom_signataire}"
        return self.nom_signataire
    
    @classmethod
    def get_signature_active(cls):
        """Retourne la signature active (priorité au directeur, sinon la première active)"""
        directeur = cls.objects.filter(actif=True, est_directeur=True).first()
        if directeur:
            return directeur
        return cls.objects.filter(actif=True).first()