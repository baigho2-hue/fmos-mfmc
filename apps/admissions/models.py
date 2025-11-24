from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal

from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Formation


class DocumentRequis(models.Model):
    """Modèle définissant les documents requis pour un type de formation."""
    
    TYPE_FORMATION_CHOICES = [
        ('DESMFMC', 'DESMFMC'),
        ('autre', 'Autre formation'),
    ]
    
    type_formation = models.CharField(
        max_length=20,
        choices=TYPE_FORMATION_CHOICES,
        verbose_name="Type de formation"
    )
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom du document"
    )
    description = models.TextField(
        verbose_name="Description du document requis"
    )
    obligatoire = models.BooleanField(
        default=True,
        verbose_name="Obligatoire"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage"
    )
    actif = models.BooleanField(
        default=True,
        verbose_name="Actif"
    )
    
    class Meta:
        verbose_name = "Document requis"
        verbose_name_plural = "Documents requis"
        ordering = ['type_formation', 'ordre', 'nom']
    
    def __str__(self):
        return f"{self.get_type_formation_display()} - {self.nom}"


class DocumentDossier(models.Model):
    """Document uploadé par un candidat pour son dossier de candidature."""
    
    dossier = models.ForeignKey(
        'DossierCandidature',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name="Dossier de candidature"
    )
    document_requis = models.ForeignKey(
        DocumentRequis,
        on_delete=models.CASCADE,
        related_name='documents_uploades',
        verbose_name="Document requis"
    )
    fichier = models.FileField(
        upload_to='dossiers_candidature/documents/',
        verbose_name="Fichier"
    )
    date_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'upload"
    )
    valide = models.BooleanField(
        default=False,
        verbose_name="Document validé"
    )
    commentaire_validation = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaire de validation"
    )
    valide_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents_valides',
        verbose_name="Validé par"
    )
    date_validation = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de validation"
    )
    
    class Meta:
        verbose_name = "Document du dossier"
        verbose_name_plural = "Documents des dossiers"
        ordering = ['dossier', 'document_requis__ordre']
        unique_together = [['dossier', 'document_requis']]
    
    def __str__(self):
        return f"{self.dossier.reference} - {self.document_requis.nom}"


class DossierCandidature(models.Model):
    """Dossier de candidature déposé au décana de la FMOS pour intégrer le DESMFMC."""

    STATUTS_DOSSIER = [
        ('soumis', 'Soumis'),
        ('incomplet', 'Incomplet'),
        ('verifie', 'Vérifié'),
        ('rejete', 'Rejeté'),
    ]

    candidat = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='dossiers_candidature',
        verbose_name="Candidat"
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='dossiers_candidature',
        verbose_name="Formation demandée"
    )
    reference = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Référence dossier",
        help_text="Identifiant interne du dossier (ex: DES-2025-001)"
    )
    date_depot = models.DateField(
        default=timezone.now,
        verbose_name="Date de dépôt"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUTS_DOSSIER,
        default='soumis',
        verbose_name="Statut du dossier"
    )
    observations = models.TextField(
        blank=True,
        verbose_name="Observations sur le dossier"
    )
    pieces_manquantes = models.TextField(
        blank=True,
        verbose_name="Pièces manquantes"
    )
    
    # Informations spécifiques pour DESMFMC
    prise_en_charge_bourse = models.BooleanField(
        default=False,
        verbose_name="Études prises en charge par une bourse",
        help_text="Préciser si les études sont prises en charge par une bourse"
    )
    details_bourse = models.TextField(
        blank=True,
        null=True,
        verbose_name="Détails de la bourse",
        help_text="Préciser les détails de la bourse si applicable"
    )

    class Meta:
        verbose_name = "Dossier de candidature"
        verbose_name_plural = "Dossiers de candidature"
        ordering = ['-date_depot']

    def __str__(self):
        return f"{self.reference} - {self.candidat.get_full_name() or self.candidat.username}"
    
    def est_desmfmc(self):
        """Vérifie si le dossier est pour DESMFMC"""
        return self.formation.code == 'DESMFMC'
    
    def verifier_completude(self):
        """Vérifie si tous les documents requis sont présents et validés"""
        if not self.est_desmfmc():
            # Pour les autres formations, on vérifie juste qu'il y a des documents
            return self.documents.exists()
        
        # Pour DESMFMC, vérifier tous les documents obligatoires
        documents_requis = DocumentRequis.objects.filter(
            type_formation='DESMFMC',
            obligatoire=True,
            actif=True
        )
        
        for doc_requis in documents_requis:
            doc_upload = self.documents.filter(document_requis=doc_requis).first()
            if not doc_upload or not doc_upload.valide:
                return False
        
        return True
    
    def get_documents_manquants(self):
        """Retourne la liste des documents manquants"""
        if not self.est_desmfmc():
            return []
        
        documents_requis = DocumentRequis.objects.filter(
            type_formation='DESMFMC',
            obligatoire=True,
            actif=True
        )
        documents_manquants = []
        
        for doc_requis in documents_requis:
            doc_upload = self.documents.filter(document_requis=doc_requis).first()
            if not doc_upload or not doc_upload.valide:
                documents_manquants.append(doc_requis)
        
        return documents_manquants


class ExamenProbatoire(models.Model):
    """Épreuve écrite probatoire pour l'accès au DESMFMC."""

    dossier = models.OneToOneField(
        DossierCandidature,
        on_delete=models.CASCADE,
        related_name='examen_probatoire',
        verbose_name="Dossier de candidature"
    )
    date_examen = models.DateField(
        default=timezone.now,
        verbose_name="Date de l'examen probatoire"
    )
    note = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Note sur 20"
    )
    seuil_reussite = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('10.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Seuil de réussite"
    )
    observation = models.TextField(
        blank=True,
        verbose_name="Observation"
    )

    class Meta:
        verbose_name = "Épreuve probatoire écrite"
        verbose_name_plural = "Épreuves probatoires écrites"
        ordering = ['-date_examen']

    def __str__(self):
        return f"Probatoire {self.dossier.reference} - {self.note}/20"

    @property
    def reussi(self):
        return self.note >= self.seuil_reussite


class EntretienIndividuel(models.Model):
    """Entretien de motivation qui suit l'examen probatoire."""

    dossier = models.OneToOneField(
        DossierCandidature,
        on_delete=models.CASCADE,
        related_name='entretien_individuel',
        verbose_name="Dossier de candidature"
    )
    date_entretien = models.DateField(
        default=timezone.now,
        verbose_name="Date de l'entretien"
    )
    score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Score sur 20"
    )
    seuil_reussite = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('10.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Seuil de réussite"
    )
    motivation = models.TextField(
        blank=True,
        verbose_name="Appréciation de la motivation"
    )
    evaluateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='entretiens_realises',
        limit_choices_to={'type_utilisateur': 'enseignant'},
        verbose_name="Évaluateur"
    )

    class Meta:
        verbose_name = "Entretien individuel"
        verbose_name_plural = "Entretiens individuels"
        ordering = ['-date_entretien']

    def __str__(self):
        return f"Entretien {self.dossier.reference} - {self.score}/20"

    @property
    def reussi(self):
        return self.score >= self.seuil_reussite


class DecisionAdmission(models.Model):
    """Décision finale d'admission au DESMFMC."""

    DECISIONS = [
        ('en_attente', 'En attente'),
        ('admis', 'Admis'),
        ('liste_attente', 'Liste d\'attente'),
        ('refuse', 'Refusé'),
    ]

    dossier = models.OneToOneField(
        DossierCandidature,
        on_delete=models.CASCADE,
        related_name='decision_admission',
        verbose_name="Dossier de candidature"
    )
    date_decision = models.DateField(
        default=timezone.now,
        verbose_name="Date de décision"
    )
    decision = models.CharField(
        max_length=20,
        choices=DECISIONS,
        default='en_attente',
        verbose_name="Décision"
    )
    note_finale = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Note finale (moyenne)"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Commentaire"
    )
    confirmations_envoyees = models.BooleanField(
        default=False,
        verbose_name="Courriel de confirmation envoyé"
    )
    email_confirmation_envoye = models.BooleanField(
        default=False,
        verbose_name="Email de confirmation envoyé",
        help_text="Indique si l'email de confirmation d'admission a été envoyé au candidat"
    )
    date_envoi_email = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date d'envoi de l'email"
    )

    class Meta:
        verbose_name = "Décision d'admission"
        verbose_name_plural = "Décisions d'admission"
        ordering = ['-date_decision']

    def __str__(self):
        return f"Décision {self.dossier.reference} - {self.get_decision_display()}"

    def calculer_note_finale(self):
        """Calcule la note finale comme moyenne entre probatoire et entretien si disponibles."""
        note_examen = getattr(self.dossier, 'examen_probatoire', None)
        entretien = getattr(self.dossier, 'entretien_individuel', None)
        if note_examen and entretien:
            self.note_finale = (note_examen.note + entretien.score) / Decimal('2')
        elif note_examen:
            self.note_finale = note_examen.note
        elif entretien:
            self.note_finale = entretien.score
        else:
            self.note_finale = None

    def save(self, *args, **kwargs):
        self.calculer_note_finale()
        super().save(*args, **kwargs)


class Inscription(models.Model):
    """Inscription administrative validée et paiement pour une formation."""
    
    STATUTS_INSCRIPTION = [
        ('en_attente', 'En attente de validation'),
        ('validee_coordination', 'Validée par la Coordination MFMC'),
        ('validee_decanat', 'Validée par le Décanat'),
        ('validee_complete', 'Validation complète (Coordination + Décanat)'),
        ('paiement_en_attente', 'Paiement en attente'),
        ('paiement_valide', 'Paiement validé'),
        ('inscription_complete', 'Inscription complète'),
        ('annulee', 'Annulée'),
        ('refusee', 'Refusée'),
    ]
    
    MODES_PAIEMENT = [
        ('liquide', 'Espèces (Secrétariat FMOS)'),
        ('carte_bancaire', 'Carte bancaire'),
        ('orange_money', 'Orange Money'),
    ]
    
    dossier = models.ForeignKey(
        DossierCandidature,
        on_delete=models.CASCADE,
        related_name='inscriptions',
        verbose_name="Dossier de candidature"
    )
    decision_admission = models.ForeignKey(
        DecisionAdmission,
        on_delete=models.CASCADE,
        related_name='inscriptions',
        null=True,
        blank=True,
        verbose_name="Décision d'admission",
        help_text="Lien vers la décision d'admission si disponible"
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='inscriptions',
        verbose_name="Formation"
    )
    
    # Validation administrative
    statut = models.CharField(
        max_length=30,
        choices=STATUTS_INSCRIPTION,
        default='en_attente',
        verbose_name="Statut de l'inscription"
    )
    validee_par_coordination = models.BooleanField(
        default=False,
        verbose_name="Validée par la Coordination MFMC"
    )
    date_validation_coordination = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de validation Coordination MFMC"
    )
    validateur_coordination = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inscriptions_validees_coordination',
        limit_choices_to={'type_utilisateur__in': ['coordination', 'enseignant']},
        verbose_name="Validateur Coordination MFMC"
    )
    validee_par_decanat = models.BooleanField(
        default=False,
        verbose_name="Validée par le Décanat"
    )
    date_validation_decanat = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de validation Décanat"
    )
    validateur_decanat = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inscriptions_validees_decanat',
        limit_choices_to={'type_utilisateur__in': ['coordination', 'enseignant']},
        verbose_name="Validateur Décanat"
    )
    commentaires_validation = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaires de validation"
    )
    
    # Paiement (uniquement pour les formations certifiantes)
    montant_inscription = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        verbose_name="Montant de l'inscription",
        help_text="Montant à payer pour l'inscription (uniquement pour les formations certifiantes)"
    )
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODES_PAIEMENT,
        null=True,
        blank=True,
        verbose_name="Mode de paiement",
        help_text="Uniquement pour les formations certifiantes"
    )
    paiement_valide = models.BooleanField(
        default=False,
        verbose_name="Paiement validé"
    )
    date_paiement = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de paiement"
    )
    reference_paiement = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Référence de paiement",
        help_text="Numéro de transaction, référence Orange Money, etc."
    )
    preuve_paiement = models.FileField(
        upload_to='inscriptions/preuves_paiement/',
        blank=True,
        null=True,
        verbose_name="Preuve de paiement",
        help_text="Capture d'écran, reçu, etc."
    )
    valideur_paiement = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paiements_valides',
        verbose_name="Personne ayant validé le paiement"
    )
    date_validation_paiement = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de validation du paiement"
    )
    commentaires_paiement = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaires sur le paiement"
    )
    
    # Informations complémentaires
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notes internes"
    )
    
    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
        ordering = ['-date_inscription']
        unique_together = [['dossier', 'formation']]
    
    def __str__(self):
        return f"Inscription {self.dossier.reference} - {self.formation.nom}"
    
    def save(self, *args, **kwargs):
        # Mettre à jour le statut automatiquement selon les validations et le type de formation
        validation_complete = self.validee_par_coordination and self.validee_par_decanat
        
        if validation_complete:
            if self.est_certifiante:
                # Formation certifiante : nécessite paiement
                if self.paiement_valide:
                    self.statut = 'inscription_complete'
                else:
                    self.statut = 'paiement_en_attente'
            else:
                # Formation non certifiante : validation suffit
                self.statut = 'inscription_complete'
        elif self.validee_par_coordination:
            self.statut = 'validee_coordination'
        elif self.validee_par_decanat:
            self.statut = 'validee_decanat'
        elif self.paiement_valide and not validation_complete and self.est_certifiante:
            # Paiement effectué mais validation incomplète (ne devrait pas arriver normalement)
            self.statut = 'paiement_valide'
        
        super().save(*args, **kwargs)
    
    @property
    def est_certifiante(self):
        """Vérifie si la formation est certifiante"""
        return self.formation.nature == 'certifiante'
    
    @property
    def peut_payer(self):
        """Vérifie si l'inscription peut être payée (validation complète + formation certifiante)"""
        if not self.est_certifiante:
            return False  # Pas de paiement pour les formations non certifiantes
        return self.validee_par_coordination and self.validee_par_decanat
    
    @property
    def est_complete(self):
        """Vérifie si l'inscription est complète"""
        validation_complete = self.validee_par_coordination and self.validee_par_decanat
        
        if self.est_certifiante:
            # Pour les formations certifiantes : validation + paiement requis
            return validation_complete and self.paiement_valide
        else:
            # Pour les formations non certifiantes : seule la validation est requise
            return validation_complete