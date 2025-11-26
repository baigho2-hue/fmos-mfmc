# apps/utilisateurs/models_formation.py
"""
Modèles pour le système de formation éducatif complet
Approche pédagogique de qualité avec objectifs d'apprentissage, progression, évaluation
"""
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from .models import Utilisateur


class Formation(models.Model):
    """Modèle représentant une formation (initiale ou continue, certifiante ou non)"""
    TYPE_FORMATION_CHOICES = [
        ('initiale', 'Formation initiale'),
        ('continue', 'Formation continue'),
    ]
    
    NATURE_CHOICES = [
        ('certifiante', 'Certifiante'),
        ('non_certifiante', 'Non certifiante'),
    ]
    
    nom = models.CharField(max_length=200, verbose_name='Nom de la formation')
    code = models.CharField(max_length=50, unique=True, verbose_name='Code de la formation')
    description = models.TextField(verbose_name='Description générale')
    type_formation = models.CharField(
        max_length=20,
        choices=TYPE_FORMATION_CHOICES,
        default='initiale',
        verbose_name='Type de formation'
    )
    nature = models.CharField(
        max_length=20,
        choices=NATURE_CHOICES,
        default='certifiante',
        verbose_name='Nature'
    )
    duree_annees = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name='Durée en années'
    )
    duree_heures = models.IntegerField(
        default=0,
        help_text="Nombre total d'heures de formation",
        validators=[MinValueValidator(0)],
        verbose_name='Durée totale en heures'
    )
    objectifs_generaux = models.TextField(
        help_text='Objectifs pédagogiques généraux de la formation',
        verbose_name='Objectifs généraux'
    )
    competences_visées = models.TextField(
        help_text='Liste des compétences que les étudiants doivent acquérir',
        verbose_name='Compétences visées'
    )
    prerequis = models.TextField(
        blank=True,
        help_text='Prérequis nécessaires pour suivre cette formation',
        null=True,
        verbose_name='Prérequis'
    )
    debouches = models.TextField(
        blank=True,
        help_text='Débouchés et opportunités professionnelles',
        null=True,
        verbose_name='Débouchés professionnels'
    )
    actif = models.BooleanField(default=True, verbose_name='Actif')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    
    class Meta:
        verbose_name = 'Formation'
        verbose_name_plural = 'Formations'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Classe(models.Model):
    """Modèle représentant une classe d'une formation"""
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='classes',
        verbose_name='Formation'
    )
    nom = models.CharField(max_length=100, verbose_name='Nom de la classe')
    code = models.CharField(max_length=50, verbose_name='Code de la classe')
    annee = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Année (1, 2, 3, 4...)'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    date_debut = models.DateField(verbose_name='Date de début')
    date_fin = models.DateField(verbose_name='Date de fin prévue')
    effectif_max = models.IntegerField(
        default=50,
        validators=[MinValueValidator(1)],
        verbose_name='Effectif maximum'
    )
    responsable = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='classes_responsables',
        verbose_name='Responsable pédagogique'
    )
    actif = models.BooleanField(default=True, verbose_name='Actif')
    
    class Meta:
        verbose_name = 'Classe'
        verbose_name_plural = 'Classes'
        ordering = ['formation', 'annee']
        unique_together = [['formation', 'annee', 'code']]
    
    def __str__(self):
        return f"{self.nom} ({self.formation.nom})"


class ObjectifApprentissage(models.Model):
    """Modèle représentant un objectif d'apprentissage basé sur la taxonomie de Bloom"""
    NIVEAU_CHOICES = [
        ('connaissance', 'Connaissance'),
        ('comprehension', 'Compréhension'),
        ('application', 'Application'),
        ('analyse', 'Analyse'),
        ('synthese', 'Synthèse'),
        ('evaluation', 'Évaluation'),
    ]
    
    libelle = models.CharField(max_length=500, verbose_name="Libellé de l'objectif")
    niveau = models.CharField(
        max_length=20,
        choices=NIVEAU_CHOICES,
        default='connaissance',
        verbose_name='Niveau taxonomique'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Description détaillée')
    criteres_evaluation = models.TextField(
        help_text="Comment évaluer si l'objectif est atteint",
        verbose_name="Critères d'évaluation"
    )
    
    class Meta:
        verbose_name = "Objectif d'apprentissage"
        verbose_name_plural = "Objectifs d'apprentissage"
        ordering = ['niveau', 'libelle']
    
    def __str__(self):
        return f"{self.get_niveau_display()}: {self.libelle[:50]}"


class MethodePedagogique(models.Model):
    """Modèle représentant une méthode pédagogique"""
    nom = models.CharField(max_length=200, unique=True, verbose_name='Nom de la méthode')
    description = models.TextField(verbose_name='Description')
    avantages = models.TextField(blank=True, null=True, verbose_name='Avantages')
    inconvenients = models.TextField(blank=True, null=True, verbose_name='Inconvénients')
    contexte_utilisation = models.TextField(
        blank=True,
        help_text='Quand et comment utiliser cette méthode',
        null=True,
        verbose_name="Contexte d'utilisation"
    )
    
    class Meta:
        verbose_name = 'Méthode pédagogique'
        verbose_name_plural = 'Méthodes pédagogiques'
        ordering = ['nom']
    
    def __str__(self):
        return self.nom


class Competence(models.Model):
    """
    Modèle représentant une compétence à acquérir.
    
    Les compétences sont organisées par :
    - Jalons du programme (via ManyToMany)
    - Classes (via ManyToMany)
    - Modules (via ModuleProgramme.competences_module)
    - Cours (via Cours.competences)
    """
    DOMAINE_CHOICES = [
        ('savoir', 'Savoir (connaissances)'),
        ('savoir_faire', 'Savoir-faire (habiletés)'),
        ('savoir_etre', 'Savoir-être (attitudes)'),
    ]
    
    libelle = models.CharField(max_length=300, verbose_name='Libellé de la compétence')
    domaine = models.CharField(
        max_length=20,
        choices=DOMAINE_CHOICES,
        default='savoir',
        verbose_name='Domaine'
    )
    description = models.TextField(verbose_name='Description')
    niveau_attendu = models.TextField(
        help_text='Description du niveau de maîtrise attendu',
        verbose_name='Niveau attendu'
    )
    
    # Relations avec jalons et classes (ajoutées pour organisation)
    # Note: Les compétences sont aussi liées via modules et cours
    jalons = models.ManyToManyField(
        'utilisateurs.JalonProgramme',
        related_name='competences_jalons',
        blank=True,
        verbose_name='Jalons associés',
        help_text='Jalons du programme où cette compétence est évaluée'
    )
    classes = models.ManyToManyField(
        'utilisateurs.Classe',
        related_name='competences_classes',
        blank=True,
        verbose_name='Classes associées',
        help_text='Classes où cette compétence est enseignée et évaluée'
    )
    
    class Meta:
        verbose_name = 'Compétence'
        verbose_name_plural = 'Compétences'
        ordering = ['domaine', 'libelle']
    
    def __str__(self):
        return f"{self.get_domaine_display()}: {self.libelle[:50]}"
    
    def get_jalons_display(self):
        """Retourne la liste des jalons associés"""
        return ", ".join([str(j) for j in self.jalons.all()[:3]])
    get_jalons_display.short_description = "Jalons"
    
    def get_classes_display(self):
        """Retourne la liste des classes associées"""
        return ", ".join([c.nom for c in self.classes.all()[:3]])
    get_classes_display.short_description = "Classes"


class Cours(models.Model):
    """Modèle représentant un cours d'une classe"""
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='cours',
        verbose_name='Classe'
    )
    titre = models.CharField(max_length=200, verbose_name='Titre du cours')
    code = models.CharField(max_length=50, verbose_name='Code du cours')
    description = models.TextField(verbose_name='Description')
    contenu = models.TextField(verbose_name='Contenu détaillé')
    description_methodes = models.TextField(
        blank=True,
        help_text='Comment les méthodes sont appliquées dans ce cours',
        null=True,
        verbose_name='Description des méthodes'
    )
    date_debut = models.DateField(verbose_name='Date de début')
    date_fin = models.DateField(verbose_name='Date de fin')
    volume_horaire = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Volume horaire (heures)'
    )
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    fichier_contenu = models.FileField(
        blank=True,
        help_text='Fichier PDF, Word, PowerPoint, etc. contenant le contenu du cours',
        null=True,
        upload_to='cours/fichiers/',
        verbose_name='Fichier du cours'
    )
    ressources_pedagogiques = models.TextField(
        blank=True,
        help_text='Liste des ressources (livres, articles, sites web, etc.)',
        null=True,
        verbose_name='Ressources pédagogiques'
    )
    enseignant = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='cours_enseignes',
        verbose_name='Enseignant principal'
    )
    co_enseignants = models.ManyToManyField(
        Utilisateur,
        blank=True,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='cours_co_enseignes',
        verbose_name='Co-enseignants'
    )
    objectifs_apprentissage = models.ManyToManyField(
        ObjectifApprentissage,
        blank=True,
        related_name='cours',
        verbose_name="Objectifs d'apprentissage"
    )
    competences = models.ManyToManyField(
        Competence,
        blank=True,
        related_name='cours',
        verbose_name='Compétences visées'
    )
    methodes_pedagogiques = models.ManyToManyField(
        MethodePedagogique,
        blank=True,
        related_name='cours',
        verbose_name='Méthodes pédagogiques'
    )
    actif = models.BooleanField(default=True, verbose_name='Actif')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'
        ordering = ['classe', 'ordre', 'date_debut']
    
    def __str__(self):
        return f"{self.titre} ({self.classe.nom})"


class Lecon(models.Model):
    """Modèle représentant une leçon d'un cours"""
    TYPE_LECON_CHOICES = [
        ('lecon', 'Leçon'),
        ('atelier', 'Atelier'),
        ('tp', 'Travaux pratiques'),
        ('td', 'Travaux dirigés'),
    ]
    
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='lecons',
        verbose_name='Cours'
    )
    titre = models.CharField(max_length=200, verbose_name='Titre de la leçon')
    numero = models.IntegerField(
        default=1,
        help_text="Numéro d'ordre dans le cours",
        validators=[MinValueValidator(1)],
        verbose_name='Numéro de la leçon'
    )
    type_lecon = models.CharField(
        max_length=20,
        choices=TYPE_LECON_CHOICES,
        default='lecon',
        verbose_name='Type de leçon'
    )
    contenu = models.TextField(
        blank=True,
        help_text='Contenu textuel de la leçon',
        null=True,
        verbose_name='Contenu de la leçon'
    )
    fichier_contenu = models.FileField(
        blank=True,
        help_text='Fichier PDF, Word, PowerPoint, etc. contenant le contenu de la leçon',
        null=True,
        upload_to='cours/lecons/',
        verbose_name='Fichier de contenu'
    )
    duree_estimee = models.IntegerField(
        default=0,
        help_text='Durée estimée pour compléter cette leçon',
        validators=[MinValueValidator(0)],
        verbose_name='Durée estimée (minutes)'
    )
    ressources = models.TextField(
        blank=True,
        help_text='Liens, références, documents supplémentaires',
        null=True,
        verbose_name='Ressources complémentaires'
    )
    ordre = models.IntegerField(
        default=0,
        help_text='Ordre dans le cours (utilisé pour trier les leçons)',
        verbose_name="Ordre d'affichage"
    )
    date_dispensation = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date et heure de dispensation",
        help_text="Date et heure prévues pour dispenser cette leçon"
    )
    actif = models.BooleanField(default=True, verbose_name='Actif')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Leçon'
        verbose_name_plural = 'Leçons'
        ordering = ['cours', 'ordre', 'numero']
        unique_together = [['cours', 'numero']]
    
    def __str__(self):
        return f"{self.titre} (Leçon {self.numero} - {self.cours.titre})"
    
    def get_enseignants(self):
        """Retourne la liste des enseignants responsables de cette leçon"""
        enseignants = []
        if self.cours.enseignant:
            enseignants.append(self.cours.enseignant)
        enseignants.extend(self.cours.co_enseignants.all())
        return list(set(enseignants))


class Planification(models.Model):
    """Modèle représentant une planification d'activité pédagogique"""
    TYPE_ACTIVITE_CHOICES = [
        ('cours', 'Cours magistral'),
        ('td', 'Travaux Dirigés (TD)'),
        ('tp', 'Travaux Pratiques (TP)'),
        ('stage', 'Stage'),
        ('examen', 'Examen'),
        ('evaluation', 'Évaluation'),
        ('conference', 'Conférence'),
        ('atelier', 'Atelier'),
        ('autre', 'Autre'),
    ]
    
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        related_name='planifications',
        verbose_name='Classe'
    )
    cours_lie = models.ForeignKey(
        Cours,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='planifications',
        verbose_name='Cours lié'
    )
    enseignant = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='planifications',
        verbose_name='Enseignant'
    )
    titre = models.CharField(max_length=200, verbose_name='Titre')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    type_activite = models.CharField(
        max_length=50,
        choices=TYPE_ACTIVITE_CHOICES,
        default='cours',
        verbose_name="Type d'activité"
    )
    date_debut = models.DateTimeField(verbose_name='Date et heure de début')
    date_fin = models.DateTimeField(verbose_name='Date et heure de fin')
    duree_heures = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Durée en heures'
    )
    lieu = models.CharField(blank=True, max_length=200, null=True, verbose_name='Lieu')
    methodes_utilisees = models.ManyToManyField(
        MethodePedagogique,
        blank=True,
        related_name='planifications',
        verbose_name='Méthodes pédagogiques utilisées'
    )
    objectifs_seance = models.ManyToManyField(
        ObjectifApprentissage,
        blank=True,
        related_name='planifications',
        verbose_name='Objectifs de la séance'
    )
    actif = models.BooleanField(default=True, verbose_name='Actif')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Planification'
        verbose_name_plural = 'Planifications'
        ordering = ['date_debut']
    
    def __str__(self):
        return f"{self.titre} - {self.classe.nom}"


class ProgressionEtudiant(models.Model):
    """Modèle représentant la progression d'un étudiant dans un cours"""
    STATUT_CHOICES = [
        ('non_commence', 'Non commencé'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('valide', 'Validé'),
        ('non_valide', 'Non validé'),
    ]
    
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='progressions',
        verbose_name='Étudiant'
    )
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='progressions',
        verbose_name='Cours'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='non_commence',
        verbose_name='Statut'
    )
    pourcentage_completion = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Pourcentage de complétion'
    )
    date_debut = models.DateTimeField(blank=True, null=True, verbose_name='Date de début')
    date_fin = models.DateTimeField(blank=True, null=True, verbose_name='Date de fin')
    derniere_activite = models.DateTimeField(auto_now=True, verbose_name='Dernière activité')
    notes = models.TextField(blank=True, null=True, verbose_name='Notes personnelles')
    commentaires_enseignant = models.TextField(
        blank=True,
        null=True,
        verbose_name="Commentaires de l'enseignant"
    )
    objectifs_atteints = models.ManyToManyField(
        ObjectifApprentissage,
        blank=True,
        related_name='progressions_objectifs',
        verbose_name='Objectifs atteints'
    )
    competences_acquises = models.ManyToManyField(
        Competence,
        blank=True,
        related_name='progressions_competences',
        verbose_name='Compétences acquises'
    )
    
    class Meta:
        verbose_name = 'Progression étudiant'
        verbose_name_plural = 'Progressions étudiants'
        ordering = ['-derniere_activite']
        unique_together = [['etudiant', 'cours']]
    
    def __str__(self):
        return f"{self.etudiant.get_full_name()} - {self.cours.titre} ({self.get_statut_display()})"


class SessionCoursEnLigne(models.Model):
    """Modèle représentant une session de cours en ligne"""
    STATUT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    
    cours = models.ForeignKey(
        Cours,
        on_delete=models.CASCADE,
        related_name='sessions_en_ligne',
        verbose_name='Cours'
    )
    enseignant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='sessions_cours_enseignees',
        verbose_name='Enseignant'
    )
    titre = models.CharField(max_length=200, verbose_name='Titre de la session')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    date_debut_prevue = models.DateTimeField(verbose_name='Date et heure de début prévue')
    date_fin_prevue = models.DateTimeField(verbose_name='Date et heure de fin prévue')
    date_debut_reelle = models.DateTimeField(blank=True, null=True, verbose_name='Date de début réelle')
    date_fin_reelle = models.DateTimeField(blank=True, null=True, verbose_name='Date de fin réelle')
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='planifiee',
        verbose_name='Statut'
    )
    contenu_session = models.TextField(
        blank=True,
        help_text='Contenu, présentation, documents partagés',
        null=True,
        verbose_name='Contenu de la session'
    )
    lien_session = models.URLField(
        blank=True,
        help_text='Lien pour rejoindre la session (Zoom, Teams, etc.)',
        null=True,
        verbose_name='Lien de la session'
    )
    participants_autorises = models.ManyToManyField(
        Utilisateur,
        blank=True,
        help_text='Si vide, tous les étudiants de la classe peuvent participer',
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='sessions_cours_participantes',
        verbose_name='Participants autorisés'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Session de cours en ligne'
        verbose_name_plural = 'Sessions de cours en ligne'
        ordering = ['-date_debut_prevue']
    
    def __str__(self):
        return f"{self.titre} - {self.cours.titre}"


class SessionEvaluationEnLigne(models.Model):
    """Modèle représentant une session d'évaluation en ligne"""
    STATUT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_attente', 'En attente de démarrage'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ]
    
    evaluation = models.ForeignKey(
        'evaluations.Evaluation',
        on_delete=models.CASCADE,
        related_name='sessions_en_ligne',
        verbose_name='Évaluation'
    )
    enseignant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'enseignant'},
        related_name='sessions_evaluation_enseignees',
        verbose_name='Enseignant'
    )
    titre = models.CharField(max_length=200, verbose_name='Titre de la session')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    date_debut_prevue = models.DateTimeField(verbose_name='Date et heure de début prévue')
    date_fin_prevue = models.DateTimeField(verbose_name='Date et heure de fin prévue')
    date_debut_reelle = models.DateTimeField(blank=True, null=True, verbose_name='Date de début réelle')
    date_fin_reelle = models.DateTimeField(blank=True, null=True, verbose_name='Date de fin réelle')
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='planifiee',
        verbose_name='Statut'
    )
    verrouillee = models.BooleanField(
        default=False,
        help_text='Si verrouillée, seuls les étudiants déjà connectés peuvent continuer',
        verbose_name='Session verrouillée'
    )
    date_verrouillage = models.DateTimeField(
        blank=True,
        help_text='Date à laquelle la session a été verrouillée',
        null=True,
        verbose_name='Date de verrouillage'
    )
    instructions = models.TextField(
        blank=True,
        help_text='Instructions spécifiques pour cette session',
        null=True,
        verbose_name='Instructions'
    )
    participants_autorises = models.ManyToManyField(
        Utilisateur,
        blank=True,
        help_text='Si vide, tous les étudiants de la classe peuvent participer',
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='sessions_evaluation_participantes',
        verbose_name='Participants autorisés'
    )
    etudiants_connectes = models.ManyToManyField(
        Utilisateur,
        blank=True,
        help_text='Étudiants qui étaient connectés au moment du verrouillage',
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='sessions_evaluation_connectees',
        verbose_name='Étudiants connectés'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Session d'évaluation en ligne"
        verbose_name_plural = "Sessions d'évaluation en ligne"
        ordering = ['-date_debut_prevue']
    
    def __str__(self):
        return f"{self.titre} - {self.evaluation.titre}"


class QuizLecon(models.Model):
    """Modèle représentant un quiz/exercice associé à une leçon"""
    TYPE_QUIZ_CHOICES = [
        ('quiz', 'Quiz'),
        ('exercice', 'Exercice'),
        ('evaluation', 'Évaluation'),
    ]
    
    lecon = models.ForeignKey(
        Lecon,
        on_delete=models.CASCADE,
        related_name='quiz',
        verbose_name='Leçon'
    )
    titre = models.CharField(max_length=200, verbose_name='Titre du quiz/exercice')
    type_quiz = models.CharField(
        max_length=20,
        choices=TYPE_QUIZ_CHOICES,
        default='quiz',
        verbose_name='Type'
    )
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    instructions = models.TextField(
        help_text='Instructions pour compléter le quiz/exercice',
        verbose_name='Instructions'
    )
    duree_minutes = models.IntegerField(
        default=0,
        help_text='0 = pas de limite de temps',
        validators=[MinValueValidator(0)],
        verbose_name='Durée estimée (minutes)'
    )
    note_maximale = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20.0,
        validators=[MinValueValidator(0)],
        verbose_name='Note maximale'
    )
    ordre = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    actif = models.BooleanField(default=True, verbose_name='Actif')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Quiz/Exercice de leçon'
        verbose_name_plural = 'Quiz/Exercices de leçons'
        ordering = ['lecon', 'ordre', 'date_creation']
    
    def __str__(self):
        return f"{self.titre} - {self.lecon.titre}"


class QuestionQuiz(models.Model):
    """Modèle représentant une question d'un quiz"""
    TYPE_REPONSE_CHOICES = [
        ('choix_unique', 'Choix unique'),
        ('choix_multiple', 'Choix multiple'),
        ('texte_libre', 'Texte libre'),
        ('vrai_faux', 'Vrai/Faux'),
    ]
    
    quiz = models.ForeignKey(
        QuizLecon,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Quiz'
    )
    enonce = models.TextField(verbose_name='Énoncé de la question')
    type_reponse = models.CharField(
        max_length=20,
        choices=TYPE_REPONSE_CHOICES,
        default='choix_unique',
        verbose_name='Type de réponse'
    )
    points = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0)],
        verbose_name='Points'
    )
    ordre = models.IntegerField(default=0, verbose_name='Ordre')
    explication = models.TextField(
        blank=True,
        help_text='Affichée après la correction',
        null=True,
        verbose_name='Explication de la réponse'
    )
    
    class Meta:
        verbose_name = 'Question de quiz'
        verbose_name_plural = 'Questions de quiz'
        ordering = ['quiz', 'ordre']
    
    def __str__(self):
        return f"{self.enonce[:50]}... ({self.quiz.titre})"


class ReponseQuestion(models.Model):
    """Modèle représentant une réponse possible à une question"""
    question = models.ForeignKey(
        QuestionQuiz,
        on_delete=models.CASCADE,
        related_name='reponses_possibles',
        verbose_name='Question'
    )
    texte = models.CharField(max_length=500, verbose_name='Texte de la réponse')
    est_correcte = models.BooleanField(default=False, verbose_name='Est correcte')
    ordre = models.IntegerField(default=0, verbose_name='Ordre')
    
    class Meta:
        verbose_name = 'Réponse possible'
        verbose_name_plural = 'Réponses possibles'
        ordering = ['question', 'ordre']
    
    def __str__(self):
        return f"{self.texte[:50]}... ({'✓' if self.est_correcte else '✗'})"


class ReponseEtudiantQuiz(models.Model):
    """Modèle représentant la réponse d'un étudiant à une question"""
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='reponses_quiz',
        verbose_name='Étudiant'
    )
    quiz = models.ForeignKey(
        QuizLecon,
        on_delete=models.CASCADE,
        related_name='reponses_etudiants',
        verbose_name='Quiz'
    )
    question = models.ForeignKey(
        QuestionQuiz,
        on_delete=models.CASCADE,
        related_name='reponses_etudiants',
        verbose_name='Question'
    )
    reponses_choisies = models.ManyToManyField(
        ReponseQuestion,
        blank=True,
        verbose_name='Réponses choisies (pour choix multiple/unique)'
    )
    reponse_texte = models.TextField(
        blank=True,
        null=True,
        verbose_name='Réponse texte (pour texte libre)'
    )
    points_obtenus = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0)],
        verbose_name='Points obtenus'
    )
    date_reponse = models.DateTimeField(auto_now_add=True, verbose_name='Date de réponse')
    
    class Meta:
        verbose_name = "Réponse d'étudiant"
        verbose_name_plural = "Réponses d'étudiants"
        ordering = ['-date_reponse']
        unique_together = [['etudiant', 'question']]
    
    def __str__(self):
        return f"{self.etudiant.get_full_name()} - {self.question.enonce[:30]}..."


class ResultatQuiz(models.Model):
    """Modèle représentant le résultat d'un étudiant à un quiz"""
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='resultats_quiz',
        verbose_name='Étudiant'
    )
    quiz = models.ForeignKey(
        QuizLecon,
        on_delete=models.CASCADE,
        related_name='resultats',
        verbose_name='Quiz'
    )
    note_finale = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0)],
        verbose_name='Note finale'
    )
    pourcentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Pourcentage'
    )
    date_debut = models.DateTimeField(blank=True, null=True, verbose_name='Date de début')
    date_fin = models.DateTimeField(blank=True, null=True, verbose_name='Date de fin')
    termine = models.BooleanField(default=False, verbose_name='Terminé')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Résultat de quiz'
        verbose_name_plural = 'Résultats de quiz'
        ordering = ['-date_creation']
        unique_together = [['etudiant', 'quiz']]
    
    def __str__(self):
        return f"{self.etudiant.get_full_name()} - {self.quiz.titre} ({self.note_finale}/{self.quiz.note_maximale})"


class CommentaireLecon(models.Model):
    """Modèle représentant un commentaire sur une leçon"""
    lecon = models.ForeignKey(
        Lecon,
        on_delete=models.CASCADE,
        related_name='commentaires',
        verbose_name='Leçon'
    )
    auteur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='commentaires_lecons',
        verbose_name='Auteur'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        help_text='Pour les réponses aux commentaires',
        null=True,
        related_name='reponses',
        verbose_name='Commentaire parent'
    )
    contenu = models.TextField(verbose_name='Contenu du commentaire')
    actif = models.BooleanField(default=True, verbose_name='Actif')
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    date_modification = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    
    class Meta:
        verbose_name = 'Commentaire de leçon'
        verbose_name_plural = 'Commentaires de leçons'
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.auteur.get_full_name()} - {self.lecon.titre} ({self.date_creation.strftime('%d/%m/%Y')})"


class ProgressionLecon(models.Model):
    """Modèle représentant la progression d'un étudiant dans une leçon"""
    STATUT_CHOICES = [
        ('non_commence', 'Non commencé'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('valide', 'Validé'),
    ]
    
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='progressions_lecons',
        verbose_name='Étudiant'
    )
    lecon = models.ForeignKey(
        Lecon,
        on_delete=models.CASCADE,
        related_name='progressions',
        verbose_name='Leçon'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='non_commence',
        verbose_name='Statut'
    )
    pourcentage_completion = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Pourcentage de complétion'
    )
    temps_passe_minutes = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Temps passé (minutes)'
    )
    date_debut = models.DateTimeField(blank=True, null=True, verbose_name='Date de début')
    date_fin = models.DateTimeField(blank=True, null=True, verbose_name='Date de fin')
    derniere_activite = models.DateTimeField(auto_now=True, verbose_name='Dernière activité')
    notes = models.TextField(
        blank=True,
        help_text="Notes que l'étudiant peut prendre sur cette leçon",
        null=True,
        verbose_name='Notes personnelles'
    )
    
    class Meta:
        verbose_name = 'Progression de leçon'
        verbose_name_plural = 'Progressions de leçons'
        ordering = ['lecon__ordre', 'lecon__numero']
        unique_together = [['etudiant', 'lecon']]
    
    def __str__(self):
        return f"{self.etudiant.get_full_name()} - {self.lecon.titre} ({self.get_statut_display()})"


class AlerteLecon(models.Model):
    """Modèle pour suivre les alertes envoyées aux enseignants pour les leçons"""
    TYPE_ALERTE_CHOICES = [
        ('semaine', '1 semaine avant'),
        ('trois_jours', '3 jours avant'),
        ('programmee', 'Lors de la programmation'),
    ]
    
    lecon = models.ForeignKey(
        Lecon,
        on_delete=models.CASCADE,
        related_name='alertes',
        verbose_name="Leçon"
    )
    enseignant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='alertes_lecons',
        limit_choices_to={'type_utilisateur': 'enseignant'},
        verbose_name="Enseignant"
    )
    type_alerte = models.CharField(
        max_length=20,
        choices=TYPE_ALERTE_CHOICES,
        verbose_name="Type d'alerte"
    )
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    envoye = models.BooleanField(default=True, verbose_name="Envoyé")
    
    class Meta:
        verbose_name = "Alerte de leçon"
        verbose_name_plural = "Alertes de leçons"
        unique_together = [['lecon', 'enseignant', 'type_alerte']]
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"Alerte {self.get_type_alerte_display()} - {self.lecon.titre} - {self.enseignant.get_full_name()}"


class PaiementFormation(models.Model):
    """Modèle représentant un paiement pour une formation"""
    MODE_PAIEMENT_CHOICES = [
        ('bancaire', 'Bancaire'),
        ('espece', 'Espèce'),
        ('orange_money', 'Orange Money'),
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]
    
    formation = models.ForeignKey(
        Formation,
        on_delete=models.CASCADE,
        related_name='paiements',
        verbose_name='Formation'
    )
    etudiant = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        limit_choices_to={'type_utilisateur': 'etudiant'},
        related_name='paiements_formations',
        verbose_name='Étudiant'
    )
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Montant'
    )
    mode_paiement = models.CharField(
        max_length=20,
        choices=MODE_PAIEMENT_CHOICES,
        default='bancaire',
        verbose_name='Mode de paiement'
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente',
        verbose_name='Statut'
    )
    reference_paiement = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Référence du paiement (numéro de transaction, etc.)",
        verbose_name='Référence de paiement'
    )
    preuve_paiement = models.FileField(
        upload_to='formations/preuves_paiement/',
        blank=True,
        null=True,
        help_text="Capture d'écran, reçu, etc.",
        verbose_name='Preuve de paiement'
    )
    date_paiement = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date de paiement'
    )
    date_validation = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Date de validation'
    )
    valideur = models.ForeignKey(
        Utilisateur,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='paiements_formations_valides',
        verbose_name='Validateur'
    )
    commentaires = models.TextField(
        blank=True,
        null=True,
        verbose_name='Commentaires'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Paiement de formation'
        verbose_name_plural = 'Paiements de formations'
        ordering = ['-date_paiement']
        unique_together = [['formation', 'etudiant']]
    
    def __str__(self):
        return f"{self.etudiant.get_full_name()} - {self.formation.nom} - {self.montant} FCFA ({self.get_mode_paiement_display()})"