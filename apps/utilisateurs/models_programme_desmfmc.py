# apps/utilisateurs/models_programme_desmfmc.py
"""
Modèles pour structurer le programme DESMFMC sur 4 ans
avec jalons, progression et suivi pédagogique
"""
from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Utilisateur
from .models_formation import Formation, Classe, Cours, ObjectifApprentissage, Competence, MethodePedagogique


class JalonProgramme(models.Model):
    """Jalons du programme (semestres, trimestres, modules)"""
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='jalons',
        verbose_name="Formation"
    )
    nom = models.CharField(max_length=200, verbose_name="Nom du jalon")
    code = models.CharField(max_length=50, verbose_name="Code du jalon")
    annee = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name="Année (1-4)"
    )
    semestre = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2)],
        null=True,
        blank=True,
        verbose_name="Semestre (1-2)"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre d'affichage",
        help_text="Ordre dans l'année"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    volume_horaire_total = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Volume horaire total (heures)"
    )
    
    class Meta:
        verbose_name = "Jalon du programme"
        verbose_name_plural = "Jalons du programme"
        ordering = ['formation', 'annee', 'ordre']
        unique_together = ['formation', 'code']
    
    def __str__(self):
        semestre_str = f" - S{self.semestre}" if self.semestre else ""
        return f"{self.formation.nom} - Année {self.annee}{semestre_str} - {self.nom}"


class ModuleProgramme(models.Model):
    """Modules de cours dans un jalon"""
    jalon = models.ForeignKey(
        JalonProgramme,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name="Jalon"
    )
    nom = models.CharField(max_length=200, verbose_name="Nom du module")
    code = models.CharField(max_length=50, verbose_name="Code du module")
    description = models.TextField(verbose_name="Description")
    volume_horaire = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Volume horaire (heures)"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre dans le jalon"
    )
    
    # Objectifs et compétences du module
    objectifs_module = models.ManyToManyField(
        ObjectifApprentissage,
        related_name='modules',
        blank=True,
        verbose_name="Objectifs d'apprentissage"
    )
    competences_module = models.ManyToManyField(
        Competence,
        related_name='modules',
        blank=True,
        verbose_name="Compétences visées"
    )
    
    # Prérequis
    prerequis_modules = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='modules_suivants',
        verbose_name="Modules prérequis"
    )
    
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Module du programme"
        verbose_name_plural = "Modules du programme"
        ordering = ['jalon', 'ordre']
        unique_together = ['jalon', 'code']
    
    def __str__(self):
        return f"{self.jalon} - {self.nom}"


class CoursProgramme(models.Model):
    """Cours spécifiques dans un module du programme"""
    module = models.ForeignKey(
        ModuleProgramme,
        on_delete=models.CASCADE,
        related_name='cours_programme',
        verbose_name="Module"
    )
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='cours_programmes',
        verbose_name="Cours"
    )
    ordre = models.IntegerField(
        default=0,
        verbose_name="Ordre dans le module"
    )
    obligatoire = models.BooleanField(
        default=True,
        verbose_name="Cours obligatoire"
    )
    
    class Meta:
        verbose_name = "Cours du programme"
        verbose_name_plural = "Cours du programme"
        ordering = ['module', 'ordre']
        unique_together = ['module', 'cours']
    
    def __str__(self):
        return f"{self.module} - {self.cours.titre}"


class SuiviProgressionProgramme(models.Model):
    """Suivi de la progression d'un étudiant dans le programme"""
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='progression_programme',
        verbose_name="Étudiant"
    )
    jalon = models.ForeignKey(
        JalonProgramme,
        on_delete=models.CASCADE,
        related_name='progressions',
        verbose_name="Jalon"
    )
    
    # Statut de progression
    statut = models.CharField(
        max_length=20,
        choices=[
            ('non_commence', 'Non commencé'),
            ('en_cours', 'En cours'),
            ('termine', 'Terminé'),
            ('valide', 'Validé'),
            ('non_valide', 'Non validé'),
        ],
        default='non_commence',
        verbose_name="Statut"
    )
    
    # Progression
    pourcentage_completion = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Pourcentage de complétion"
    )
    
    # Dates
    date_debut = models.DateTimeField(null=True, blank=True, verbose_name="Date de début")
    date_fin = models.DateTimeField(null=True, blank=True, verbose_name="Date de fin")
    derniere_activite = models.DateTimeField(auto_now=True, verbose_name="Dernière activité")
    
    # Notes et commentaires
    note_finale = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name="Note finale"
    )
    commentaires = models.TextField(blank=True, null=True, verbose_name="Commentaires")
    
    class Meta:
        verbose_name = "Suivi progression programme"
        verbose_name_plural = "Suivis progression programme"
        unique_together = ['etudiant', 'jalon']
        ordering = ['jalon__annee', 'jalon__ordre']
    
    def __str__(self):
        return f"{self.etudiant.username} - {self.jalon} ({self.get_statut_display()})"


class CSComUCentre(models.Model):
    """Centres de santé communautaires universitaires (CSCom-U) utilisés pour les stages DESMFMC."""

    TYPE_CHOICES = [
        ('urbain', 'Urbain'),
        ('rural', 'Rural'),
    ]

    nom = models.CharField(max_length=150, unique=True, verbose_name="Nom du CSCom-U")
    code = models.CharField(max_length=30, unique=True, verbose_name="Code du CSCom-U")
    type_centre = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='urbain',
        verbose_name="Type de CSCom-U"
    )
    localisation = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Localisation / Commune"
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Latitude GPS",
        help_text="Exemple : 12.639947"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        verbose_name="Longitude GPS",
        help_text="Exemple : -7.984300"
    )
    cec_superviseur_principal = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="CEC/Superviseur Principal"
    )
    actif = models.BooleanField(default=True, verbose_name="Actif pour les affectations")

    class Meta:
        verbose_name = "CSCom-U"
        verbose_name_plural = "CSCom-U"
        ordering = ['type_centre', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.get_type_centre_display()})"


class StageRotationDES(models.Model):
    """Affectations de stages (urbain/rural) pour les années 2 et 3 du DESMFMC."""

    PERIODES = [
        (1, "Période 1 (janvier-avril)"),
        (2, "Période 2 (mai-août)"),
    ]

    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='stages_rotation_des',
        limit_choices_to={'type_utilisateur': 'etudiant'},
        verbose_name="Étudiant"
    )
    annee = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(3)],
        verbose_name="Année du DES (2 ou 3)"
    )
    periode = models.IntegerField(
        choices=PERIODES,
        verbose_name="Période de stage"
    )
    centre = models.ForeignKey(
        CSComUCentre,
        on_delete=models.PROTECT,
        related_name='stages_attribues',
        verbose_name="CSCom-U attribué"
    )
    date_debut = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de début"
    )
    date_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin"
    )
    attribue_automatiquement = models.BooleanField(
        default=False,
        verbose_name="Tirage automatique"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Commentaire / ajustements"
    )

    class Meta:
        verbose_name = "Stage CSCom-U"
        verbose_name_plural = "Stages CSCom-U"
        unique_together = [
            ('etudiant', 'annee', 'periode'),
            ('etudiant', 'centre'),
        ]
        ordering = ['annee', 'periode', 'etudiant__username']

    def __str__(self):
        return f"{self.etudiant.username} - Année {self.annee} - {self.get_periode_display()} ({self.centre})"

    @property
    def type_centre(self):
        return self.centre.type_centre
    
    @classmethod
    def get_periode_actuelle(cls):
        """
        Détermine la période actuelle basée sur le calendrier de l'année scolaire.
        Période 1 : janvier-avril
        Période 2 : mai-août
        Retourne None si on est en dehors des périodes de stage (septembre-décembre)
        """
        mois_actuel = timezone.now().month
        if mois_actuel in [1, 2, 3, 4]:  # janvier-avril
            return 1
        elif mois_actuel in [5, 6, 7, 8]:  # mai-août
            return 2
        else:  # septembre-décembre
            return None
    
    @classmethod
    def get_annee_scolaire_actuelle(cls):
        """
        Détermine l'année scolaire actuelle au format "YYYY-YYYY".
        L'année scolaire commence en septembre et se termine en août.
        """
        maintenant = timezone.now()
        annee = maintenant.year
        mois = maintenant.month
        
        # Si on est entre septembre et décembre, on est dans l'année scolaire suivante
        if mois >= 9:
            return f"{annee}-{annee + 1}"
        else:
            return f"{annee - 1}-{annee}"


class ResultatAnneeDES(models.Model):
    """Suivi des validations annuelles du DESMFMC et décision de passage."""

    DECISIONS = [
        ('en_cours', 'Évaluation en cours'),
        ('admis', 'Admis en année suivante'),
        ('ajourne', 'Ajourné'),
        ('diplome', 'Diplômé'),
    ]

    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='resultats_des',
        limit_choices_to={'type_utilisateur': 'etudiant'},
        verbose_name="Étudiant"
    )
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='resultats_des',
        verbose_name="Formation"
    )
    annee = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name="Année du DES (1 à 4)"
    )
    cours_theoriques_valides = models.BooleanField(default=False, verbose_name="Cours théoriques validés")
    presence_validee = models.BooleanField(default=False, verbose_name="Présence aux enseignements validée")
    stages_valides = models.BooleanField(default=False, verbose_name="Stages hospitaliers validés")
    note_theorique = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Note théorique (sur 20)"
    )
    note_pratique = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Note pratique (sur 20)"
    )
    moyenne = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
        verbose_name="Moyenne générale (sur 20)"
    )
    epreuve_malade_validee = models.BooleanField(
        default=False,
        verbose_name="Épreuve du malade validée"
    )
    stage_urbain = models.ForeignKey(
        StageRotationDES,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resultats_urbains',
        limit_choices_to={'centre__type_centre': 'urbain'},
        verbose_name="Stage urbain"
    )
    stage_rural = models.ForeignKey(
        StageRotationDES,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resultats_ruraux',
        limit_choices_to={'centre__type_centre': 'rural'},
        verbose_name="Stage rural"
    )
    evaluations_finales_validees = models.BooleanField(
        default=False,
        verbose_name="Évaluations finales validées"
    )
    memoire_titre = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Titre du mémoire"
    )
    memoire_structure = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Structure d'accueil du mémoire"
    )
    memoire_valide = models.BooleanField(
        default=False,
        verbose_name="Mémoire soutenu et validé"
    )
    memoire_date_soutenance = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de soutenance"
    )
    decision = models.CharField(
        max_length=20,
        choices=DECISIONS,
        default='en_cours',
        verbose_name="Décision"
    )
    decision_forcee = models.BooleanField(
        default=False,
        verbose_name="Décision forcée manuellement"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Commentaire"
    )
    date_decision = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de décision"
    )
    mis_a_jour_le = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    class Meta:
        verbose_name = "Résultat annuel DES"
        verbose_name_plural = "Résultats annuels DES"
        unique_together = ['etudiant', 'formation', 'annee']
        ordering = ['etudiant__username', 'annee']

    def __str__(self):
        return f"{self.etudiant.username} - Année {self.annee} ({self.get_decision_display()})"

    def clean(self):
        if self.stage_urbain and self.stage_urbain.centre.type_centre != 'urbain':
            raise ValidationError("Le stage urbain sélectionné n'est pas identifié comme urbain.")
        if self.stage_rural and self.stage_rural.centre.type_centre != 'rural':
            raise ValidationError("Le stage rural sélectionné n'est pas identifié comme rural.")
        if self.stage_urbain and self.stage_rural and self.stage_urbain.centre_id == self.stage_rural.centre_id:
            raise ValidationError("Le stage urbain et le stage rural doivent être réalisés dans des CSCom-U différents.")

    def calculer_moyenne(self):
        if self.note_theorique is not None and self.note_pratique is not None:
            self.moyenne = (self.note_theorique + self.note_pratique) / Decimal('2')
        else:
            self.moyenne = None

    def calculer_decision(self):
        moyenne_valide = self.moyenne is not None and self.moyenne >= Decimal('10.00')

        if self.annee == 1:
            conditions = [
                self.cours_theoriques_valides,
                self.presence_validee,
                self.stages_valides,
                self.epreuve_malade_validee,
                moyenne_valide,
            ]
            return 'admis' if all(conditions) else 'ajourne'

        if self.annee in (2, 3):
            conditions = [
                self.cours_theoriques_valides,
                self.stages_valides,
                moyenne_valide,
                self.stage_urbain_id is not None,
                self.stage_rural_id is not None,
            ]
            return 'admis' if all(conditions) else 'ajourne'

        if self.annee == 4:
            conditions = [
                self.cours_theoriques_valides,
                self.stages_valides,
                self.evaluations_finales_validees,
                self.memoire_valide,
            ]
            return 'diplome' if all(conditions) else 'ajourne'

        return 'en_cours'

    def peut_acceder_annee_suivante(self):
        """
        Vérifie si l'étudiant peut accéder à l'année suivante.
        Pour les années 2, 3, 4 : nécessite :
        1. Résultat de l'année actuelle = 'admis'
        2. Paiement des frais d'inscription annuels validé pour l'année suivante
        3. Pour année 4 : mémoire validé
        """
        if self.decision != 'admis':
            return False
        
        # Pour l'année 1, l'inscription initiale suffit (gérée par le modèle Inscription)
        if self.annee == 1:
            return True
        
        # Pour les années 2, 3, 4 : vérifier le paiement annuel
        annee_suivante = self.annee + 1
        if annee_suivante > 4:
            # Année 4 : vérifier le mémoire pour obtenir le diplôme
            return self.memoire_valide if self.annee == 4 else False
        
        # Vérifier le paiement pour l'année suivante
        try:
            from apps.admissions.models import PaiementAnneeDES
            paiement = PaiementAnneeDES.objects.filter(
                etudiant=self.etudiant,
                formation=self.formation,
                annee=annee_suivante
            ).first()
            
            if not paiement or paiement.statut != 'paiement_valide':
                return False
            
            return paiement.peut_valider_passage()
        except ImportError:
            # Si le modèle n'existe pas encore, retourner False
            return False
    
    def save(self, *args, **kwargs):
        self.calculer_moyenne()
        if not self.decision_forcee:
            nouvelle_decision = self.calculer_decision()
            self.decision = nouvelle_decision
            if nouvelle_decision in ('admis', 'ajourne', 'diplome') and self.date_decision is None:
                self.date_decision = timezone.now().date()
        elif self.date_decision is None and self.decision != 'en_cours':
            self.date_decision = timezone.now().date()
        super().save(*args, **kwargs)


class StagePremiereAnnee(models.Model):
    """Stages hospitaliers de 1ère année dans les différents services."""
    
    SERVICE_CHOICES = [
        ('medecine_interne', 'Médecine interne'),
        ('chirurgie', 'Chirurgie générale'),
        ('pediatrie', 'Pédiatrie'),
        ('gynecologie', 'Gynécologie-obstétrique'),
        ('psychiatrie', 'Psychiatrie'),
        ('autre', 'Autre service'),
    ]
    
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='stages_premiere_annee',
        limit_choices_to={'type_utilisateur': 'etudiant'},
        verbose_name="Étudiant"
    )
    service = models.CharField(
        max_length=30,
        choices=SERVICE_CHOICES,
        verbose_name="Service hospitalier"
    )
    service_autre = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Autre service (si autre)"
    )
    hopital = models.CharField(
        max_length=200,
        verbose_name="Hôpital / Centre hospitalier"
    )
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")
    valide = models.BooleanField(
        default=False,
        verbose_name="Stage validé"
    )
    note = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Note du stage (sur 20)"
    )
    commentaire = models.TextField(
        blank=True,
        verbose_name="Commentaire / Appréciation"
    )
    responsable_stage = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stages_supervises',
        limit_choices_to={'type_utilisateur': 'enseignant'},
        verbose_name="Responsable du stage"
    )
    
    class Meta:
        verbose_name = "Stage 1ère année"
        verbose_name_plural = "Stages 1ère année"
        ordering = ['etudiant', 'date_debut']
    
    def __str__(self):
        service_display = self.get_service_display() if self.service != 'autre' else self.service_autre
        return f"{self.etudiant.username} - {service_display} ({self.date_debut})"


class MemoireFinEtude(models.Model):
    """Mémoire de fin d'étude pour la 4ème année du DESMFMC."""
    
    STATUT_CHOICES = [
        ('en_preparation', 'En préparation'),
        ('soumis', 'Soumis à la coordination'),
        ('en_evaluation', 'En évaluation'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
        ('soutenu', 'Soutenu'),
        ('valide', 'Validé'),
    ]
    
    etudiant = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='memoire_fin_etude',
        limit_choices_to={'type_utilisateur': 'etudiant'},
        verbose_name="Étudiant"
    )
    titre = models.CharField(
        max_length=500,
        verbose_name="Titre du mémoire"
    )
    structure_accueil = models.CharField(
        max_length=300,
        verbose_name="Structure d'accueil"
    )
    structure_autre = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Autre structure (si acceptée par coordination)"
    )
    cscom_choisi = models.ForeignKey(
        CSComUCentre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='memoires',
        verbose_name="CSCom-U choisi (si applicable)"
    )
    accepte_par_coordination = models.BooleanField(
        default=False,
        verbose_name="Structure acceptée par la coordination"
    )
    date_debut_memoire = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de début du mémoire"
    )
    date_soumission = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de soumission"
    )
    date_soutenance = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de soutenance"
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_preparation',
        verbose_name="Statut"
    )
    note = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('20.00'))],
        verbose_name="Note du mémoire (sur 20)"
    )
    resume = models.TextField(
        blank=True,
        verbose_name="Résumé du mémoire"
    )
    mots_cles = models.CharField(
        max_length=300,
        blank=True,
        verbose_name="Mots-clés"
    )
    directeur_memoire = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='memoires_diriges',
        limit_choices_to={'type_utilisateur': 'enseignant'},
        verbose_name="Directeur de mémoire"
    )
    commentaires_coordination = models.TextField(
        blank=True,
        verbose_name="Commentaires de la coordination"
    )
    fichier_memoire = models.FileField(
        upload_to='memoires/',
        null=True,
        blank=True,
        verbose_name="Fichier du mémoire"
    )
    
    class Meta:
        verbose_name = "Mémoire de fin d'étude"
        verbose_name_plural = "Mémoires de fin d'étude"
        ordering = ['-date_soumission']
    
    def __str__(self):
        return f"Mémoire {self.etudiant.username} - {self.titre[:50]}"