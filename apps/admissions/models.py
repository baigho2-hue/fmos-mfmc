from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from decimal import Decimal

from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Formation, Classe
from apps.utilisateurs.models_programme_desmfmc import ResultatAnneeDES


SANTE_COMMUNAUTAIRE_CODE = 'SANTE_COMMUNAUTAIRE'


class DocumentRequis(models.Model):
    """Modèle définissant les documents requis pour un type de formation."""
    
    TYPE_FORMATION_CHOICES = [
        ('DESMFMC', 'DESMFMC'),
        (SANTE_COMMUNAUTAIRE_CODE, 'Santé communautaire'),
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
    """Dossier de candidature déposé au décana de la FMOS pour intégrer les formations."""

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
        verbose_name="Candidat",
        null=True,
        blank=True,
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
    nom_candidat = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Nom du candidat (si non connecté)"
    )
    prenom_candidat = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Prénom du candidat (si non connecté)"
    )
    email_contact = models.EmailField(
        blank=True,
        verbose_name="Email de contact"
    )
    telephone_contact = models.CharField(
        max_length=30,
        blank=True,
        verbose_name="Téléphone de contact"
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
        return f"{self.reference} - {self.nom_affichage}"

    @property
    def nom_affichage(self):
        if self.candidat:
            return self.candidat.get_full_name() or self.candidat.username
        pieces = [p for p in [self.prenom_candidat, self.nom_candidat] if p]
        return " ".join(pieces) or "Candidat"

    @property
    def email_affichage(self):
        if self.candidat:
            return self.candidat.email
        return self.email_contact
    
    def est_desmfmc(self):
        """Vérifie si le dossier est pour DESMFMC"""
        return self.formation.code == 'DESMFMC'
    
    def est_sante_communautaire(self):
        """Vérifie si le dossier est pour la formation Santé communautaire"""
        return self.formation.code == SANTE_COMMUNAUTAIRE_CODE
    
    def verifier_completude(self):
        """Vérifie si tous les documents requis sont présents et validés"""
        type_code = None
        if self.est_desmfmc():
            type_code = 'DESMFMC'
        elif self.est_sante_communautaire():
            type_code = SANTE_COMMUNAUTAIRE_CODE
        else:
            # Pour les autres formations, on vérifie juste qu'il y a des documents
            return self.documents.exists()
        
        documents_requis = DocumentRequis.objects.filter(
            type_formation=type_code,
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
        if self.est_desmfmc():
            type_code = 'DESMFMC'
        elif self.est_sante_communautaire():
            type_code = SANTE_COMMUNAUTAIRE_CODE
        else:
            return []
        
        documents_requis = DocumentRequis.objects.filter(
            type_formation=type_code,
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
        if self.pk:
            previous_decision = DecisionAdmission.objects.filter(pk=self.pk).values_list('decision', flat=True).first()
        else:
            previous_decision = None
        super().save(*args, **kwargs)
        if self.decision == 'admis' and previous_decision != 'admis':
            self._assurer_creation_compte_et_notifier()

    def _assurer_creation_compte_et_notifier(self):
        dossier = self.dossier
        user = dossier.candidat
        password = None
        UserModel = get_user_model()

        if not user:
            email = dossier.email_affichage
            if not email:
                return
            existing_user = UserModel.objects.filter(email__iexact=email).first()
            if existing_user:
                user = existing_user
            else:
                base_username = (email.split('@')[0] or 'candidat').lower()
                username = base_username
                counter = 1
                while UserModel.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                password = get_random_string(10)
                user = UserModel.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=dossier.prenom_candidat or '',
                    last_name=dossier.nom_candidat or '',
                    type_utilisateur='etudiant',
                )
                if dossier.telephone_contact:
                    user.telephone = dossier.telephone_contact
                    user.save(update_fields=['telephone'])

            dossier.candidat = user
            dossier.save(update_fields=['candidat'])

        if user and not self.email_confirmation_envoye:
            self._envoyer_email_admission(user, password)

    def _envoyer_email_admission(self, user, password=None):
        sujet = "Votre admission à la FMOS MFMC"
        message = (
            f"Bonjour {user.get_full_name() or user.username},\n\n"
            f"Votre demande de candidature (réf : {self.dossier.reference}) a été acceptée.\n"
        )
        if password:
            message += (
                "Un compte a été créé pour vous afin d'accéder à la plateforme :\n"
                f"Identifiant : {user.email}\n"
                f"Mot de passe temporaire : {password}\n\n"
                "Veuillez vous connecter et modifier votre mot de passe dès que possible.\n"
            )
        else:
            message += "Vous pouvez utiliser vos identifiants existants pour vous connecter à la plateforme.\n"

        message += "\nCordialement,\nFMOS MFMC"

        try:
            send_mail(
                sujet,
                message,
                getattr(settings, 'DEFAULT_FROM_EMAIL', None),
                [user.email],
                fail_silently=False,
            )
            DecisionAdmission.objects.filter(pk=self.pk).update(
                email_confirmation_envoye=True,
                date_envoi_email=timezone.now(),
            )
            self.email_confirmation_envoye = True
            self.date_envoi_email = timezone.now()
        except Exception:  # pylint: disable=broad-except
            # En cas d'échec d'envoi, on laisse les champs à False pour retenter manuellement
            pass


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


class PaiementAnneeDES(models.Model):
    """Paiement des frais d'inscription annuels pour les années 2, 3 et 4 du DESMFMC."""
    
    STATUTS_PAIEMENT = [
        ('en_attente', 'En attente'),
        ('paiement_effectue', 'Paiement effectué'),
        ('paiement_valide', 'Paiement validé'),
        ('refuse', 'Refusé'),
    ]
    
    MODES_PAIEMENT = [
        ('liquide', 'Espèces (Secrétariat FMOS)'),
        ('carte_bancaire', 'Carte bancaire'),
        ('orange_money', 'Orange Money'),
    ]
    
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='paiements_annee_des',
        limit_choices_to={'type_utilisateur': 'etudiant'},
        verbose_name="Étudiant"
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='paiements_annee_des',
        verbose_name="Formation"
    )
    annee = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(4)],
        verbose_name="Année du DES (2, 3 ou 4)",
        help_text="Paiement pour l'accès à cette année"
    )
    resultat_annee = models.ForeignKey(
        ResultatAnneeDES,
        on_delete=models.CASCADE,
        related_name='paiements',
        null=True,
        blank=True,
        verbose_name="Résultat de l'année précédente",
        help_text="Résultat de l'année précédente (année-1) qui doit être validé"
    )
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Montant des frais d'inscription annuels"
    )
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODES_PAIEMENT,
        null=True,
        blank=True,
        verbose_name="Mode de paiement"
    )
    compte_bancaire = models.ForeignKey(
        'utilisateurs.CompteBancaire',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='paiements_annee_des',
        verbose_name='Compte bancaire',
        help_text="Compte bancaire sur lequel le paiement a été effectué (si mode bancaire)"
    )
    statut = models.CharField(
        max_length=30,
        choices=STATUTS_PAIEMENT,
        default='en_attente',
        verbose_name="Statut du paiement"
    )
    reference_paiement = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Référence de paiement",
        help_text="Numéro de transaction, référence Orange Money, etc."
    )
    preuve_paiement = models.FileField(
        upload_to='paiements_annee_des/preuves/',
        blank=True,
        null=True,
        verbose_name="Preuve de paiement",
        help_text="Capture d'écran, reçu, etc."
    )
    date_paiement = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de paiement"
    )
    valide_par = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paiements_annee_des_valides',
        verbose_name="Validé par"
    )
    date_validation = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date de validation"
    )
    commentaires = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaires"
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
        verbose_name = "Paiement annuel DES"
        verbose_name_plural = "Paiements annuels DES"
        ordering = ['-date_creation']
        unique_together = [['etudiant', 'formation', 'annee']]
    
    def __str__(self):
        return f"Paiement {self.etudiant.username} - Année {self.annee} - {self.get_statut_display()}"
    
    def peut_valider_passage(self):
        """
        Vérifie si l'étudiant peut passer à l'année suivante après validation du paiement.
        Conditions :
        1. Paiement validé
        2. Résultat de l'année précédente validé (admis)
        3. Épreuves écrites et pratiques validées (déjà dans ResultatAnneeDES)
        """
        if self.statut != 'paiement_valide':
            return False
        
        # Vérifier le résultat de l'année précédente
        annee_precedente = self.annee - 1
        resultat_precedent = self.resultat_annee
        if not resultat_precedent:
            resultat_precedent = ResultatAnneeDES.objects.filter(
                etudiant=self.etudiant,
                formation=self.formation,
                annee=annee_precedente
            ).first()
        
        if not resultat_precedent:
            return False
        
        # L'année précédente doit être admise
        if resultat_precedent.decision != 'admis':
            return False
        
        # Vérifier que les exigences pédagogiques ont bien été validées
        if not (
            resultat_precedent.cours_theoriques_valides
            and resultat_precedent.stages_valides
            and resultat_precedent.presence_validee
        ):
            return False
        
        return True
    
    def acceder_annee_suivante(self):
        """
        Donne accès à l'année suivante si toutes les conditions sont remplies.
        Met à jour la classe de l'étudiant et prépare le ResultatAnneeDES de l'année cible.
        """
        if not self.peut_valider_passage():
            return False
        
        # Préparer/obtenir le résultat pour l'année cible
        resultat_cible, _ = ResultatAnneeDES.objects.get_or_create(
            etudiant=self.etudiant,
            formation=self.formation,
            annee=self.annee,
            defaults={
                'decision': 'en_cours',
            }
        )
        
        # Mettre à jour la classe de l'étudiant
        classe = Classe.objects.filter(
            formation=self.formation,
            annee=self.annee,
            actif=True
        ).first()
        
        if classe and self.etudiant.classe != classe.nom:
            update_fields = []
            if self.etudiant.classe != classe.nom:
                self.etudiant.classe = classe.nom
                update_fields.append('classe')
            if not self.etudiant.date_joined:
                self.etudiant.date_joined = timezone.now()
                update_fields.append('date_joined')
            if update_fields:
                self.etudiant.save(update_fields=update_fields)
        
        return True
    
    @property
    def paiement_valide(self):
        """Vérifie si le paiement est validé"""
        return self.statut == 'paiement_valide'
    
    @property
    def est_desmfmc(self):
        """Vérifie si l'inscription est pour DESMFMC"""
        return self.formation.code == 'DESMFMC'
    
    @property
    def est_premiere_annee_desmfmc(self):
        """Pour DESMFMC, l'inscription n'est valable que pour la 1ère année"""
        if not self.est_desmfmc:
            return False
        # Pour DESMFMC, l'inscription est toujours pour la 1ère année
        return True

    def save(self, *args, **kwargs):
        """
        Enregistre le paiement et déclenche automatiquement l'accès à l'année cible
        lorsqu'il passe à l'état 'paiement_valide'.
        """
        previous_statut = None
        if self.pk:
            previous_statut = PaiementAnneeDES.objects.filter(pk=self.pk).values_list('statut', flat=True).first()

        # Toujours lier le paiement au résultat de l'année précédente si disponible
        if not self.resultat_annee and self.annee > 1:
            self.resultat_annee = ResultatAnneeDES.objects.filter(
                etudiant=self.etudiant,
                formation=self.formation,
                annee=self.annee - 1
            ).first()

        # Timestamp de validation par défaut si le statut passe à validé
        if self.statut == 'paiement_valide' and self.date_validation is None:
            self.date_validation = timezone.now()

        super().save(*args, **kwargs)

        if self.statut == 'paiement_valide' and previous_statut != 'paiement_valide':
            self.acceder_annee_suivante()