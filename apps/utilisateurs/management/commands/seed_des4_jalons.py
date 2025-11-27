"""
Commande de seed pour les jalons, cours et leçons de la QUATRIÈME ANNÉE uniquement du DESMFMC.

⚠️  IMPORTANT: Cette commande est réservée à la classe DES-A4 (année 4) uniquement.
Pour les années 1, 2 et 3, utiliser les commandes correspondantes.

Source des données: Programme DESMFMC - Année 4
"""
import datetime
import textwrap

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.utilisateurs.models_formation import (
    Formation,
    Classe,
    Cours,
    Lecon,
    Competence,
    CompetenceJalon,
)


# ⚠️  DONNÉES UNIQUEMENT POUR LA QUATRIÈME ANNÉE (DES-A4)
DES4_JALONS_DATA = [
    {
        "competence": "Expert médical en MF/MC",
        "classe_code": "DES-A4",
        "titre": "Expert médical – Soins de fin de vie et gestion des problèmes complexes",
        "ordre": 10,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Expert médical en quatrième année :
            
            1. Peut expliquer les mécanismes physiopathologiques des problèmes de santé, leurs présentations cliniques, les principes d'investigation et de traitement.
            
            2. Recueille les données cliniques pertinentes en fonction des hypothèses diagnostiques.
            
            3. Effectue adéquatement l'examen physique en s'assurant du confort du patient.
            
            4. Interprète les données en tenant compte de l'ensemble de la situation.
            
            5. Choisit un plan d'intervention approprié (investigation, traitement, suivi) qui tient compte du point de vue du patient.
            
            6. Exécute adéquatement les gestes techniques en s'assurant du confort du patient.
            
            7. Évalue et gère adéquatement le patient qui présente des problèmes indifférenciés, complexes ou multiples.
            
            8. Reconnaît les situations prioritaires ou urgentes et pose les gestes appropriés.
            
            9. Évalue les problèmes de façon globale et centrée sur le patient.
            
            10. Se positionne comme médecin traitant auprès des patients et assure la continuité des soins.
            
            11. Adapte son approche en fonction des différents contextes de pratique (ambulatoire, hospitalier, à domicile, à l'urgence).
            
            12. Réaliser échographie obstétricale.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A4-SOINS-FIN-VIE",
                "ordre": 1,
                "titre": "Soins de fin de vie",
                "volume_horaire": 15,
                "description": "Cours sur les soins de fin de vie en première ligne (15h).",
                "contenu": textwrap.dedent(
                    """
                    Prise en charge des soins de fin de vie :
                    douleur totale (nociceptive, neuropathique, morale), détresse respiratoire et douleur aiguë,
                    soins de confort (problèmes buccaux, cutanés, etc.).
                    """
                ).strip(),
                "lecons": [
                    {"numero": 1, "titre": "Douleur totale (nociceptive, neuropathique, morale)", "type": "lecon"},
                    {"numero": 2, "titre": "Détresse respiratoire et douleur aiguë", "type": "lecon"},
                    {"numero": 3, "titre": "Soins de confort (problèmes buccaux, cutanés, …)", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A4-GEST-FIN-VIE",
                "ordre": 2,
                "titre": "Gestion des problèmes de fin de vie",
                "volume_horaire": 15,
                "description": "Cours sur la gestion des problèmes complexes de fin de vie (15h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion des problèmes complexes en fin de vie :
                    nausées, constipation et diarrhée, anorexie, confusion et agitation,
                    soins des plaies, asthénie.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 4, "titre": "Nausées, Constipation et diarrhée", "type": "lecon"},
                    {"numero": 5, "titre": "Anorexie", "type": "lecon"},
                    {"numero": 6, "titre": "Confusion agitation", "type": "lecon"},
                    {"numero": 7, "titre": "Soins des plaies", "type": "lecon"},
                    {"numero": 8, "titre": "Asthénie", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Communicateur",
        "classe_code": "DES-A4",
        "titre": "Communicateur – Communication en contexte de fin de vie et situations complexes",
        "ordre": 20,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Communicateur en quatrième année :
            
            12. Démontre des habiletés relationnelles et de communication avec les patients et leur famille.
            
            13. Communique et collabore avec les autres membres du réseau de soins de manière respectueuse et efficace.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A4-COMM-BEHAV",
                "ordre": 1,
                "titre": "Communication et science comportementale",
                "volume_horaire": 9,
                "description": "Cours sur la communication et les sciences comportementales en contexte complexe (9h).",
                "contenu": textwrap.dedent(
                    """
                    Communication avancée et sciences comportementales :
                    deuil, mort et souffrance, approche familiale, gestion des comportements agressifs,
                    approche socio-culturelle, plan d'action de la politique nationale genre (PNG).
                    """
                ).strip(),
                "lecons": [
                    {"numero": 9, "titre": "Deuil, mort et souffrance", "type": "lecon"},
                    {"numero": 10, "titre": "Approche familiale", "type": "lecon"},
                    {"numero": 11, "titre": "Gestion des comportements agressifs", "type": "lecon"},
                    {"numero": 12, "titre": "Approche socio-culturelle", "type": "lecon"},
                    {"numero": 13, "titre": "Plan d'action de la politique nationale genre (PNG)", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Collaborateur",
        "classe_code": "DES-A4",
        "titre": "Collaborateur – Responsabilité administrative et collaboration avancée",
        "ordre": 30,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Collaborateur en quatrième année :
            
            13. Communique et collabore avec les autres membres du réseau de soins de manière respectueuse et efficace.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A4-RESP-ADMIN",
                "ordre": 1,
                "titre": "Responsabilité et tâches administratives et techniques",
                "volume_horaire": 3,
                "description": "Cours sur les responsabilités administratives et techniques (3h).",
                "contenu": textwrap.dedent(
                    """
                    Responsabilités administratives et techniques :
                    relations avec le personnel et l'ASACO, relations ASACO, Mairie, CSCom, HD.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 14, "titre": "Relations avec le personnel, l'ASACO", "type": "lecon"},
                    {"numero": 15, "titre": "Relations ASACO, Mairie, CSCom, HD", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A4-GEST-COLLAB",
                "ordre": 2,
                "titre": "Gestion",
                "volume_horaire": 9,
                "description": "Cours sur la gestion et la planification (9h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion et planification :
                    planification, animation de réunion et tenue des rapports.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 16, "titre": "Planification, animation de réunion et tenue des rapports", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Promoteur de la santé",
        "classe_code": "DES-A4",
        "titre": "Promoteur de la santé – Prévention et promotion de la santé",
        "ordre": 25,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Promoteur de la santé en quatrième année :
            
            14. Applique les notions de prévention et de promotion de la santé dans ses interventions cliniques.
            
            15. Agit à titre de « défenseur du patient » en veillant au meilleur intérêt de celui-ci dans le système de santé.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Gestionnaire",
        "classe_code": "DES-A4",
        "titre": "Gestionnaire – Gestion pratique avancée des services",
        "ordre": 40,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Gestionnaire en quatrième année :
            
            16. Rédige les notes cliniques et autres documents requis de façon structurée, pertinente et lisible.
            
            17. Organise et gère les différentes dimensions de son travail.
            
            18. Utilise judicieusement les ressources du système de santé et du réseau communautaire.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A4-GEST-PRATIQUE",
                "ordre": 1,
                "titre": "Gestions pratique",
                "volume_horaire": 30,
                "description": "Cours sur la gestion pratique avancée des services (30h).",
                "contenu": textwrap.dedent(
                    """
                    Gestion pratique avancée :
                    planification budgétaire et gestion administrative, planification et développement des services
                    et stratégies avancées, gestion et formation du personnel, gestion d'un environnement
                    de pratique sécuritaire incluant les déchets biomédicaux, organisation des services.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 17, "titre": "Planification budgétaire et gestion administrative", "type": "lecon"},
                    {"numero": 18, "titre": "Planification et développement des services et de stratégies avancées", "type": "lecon"},
                    {"numero": 19, "titre": "Gestion et formation du personnel", "type": "lecon"},
                    {"numero": 20, "titre": "Gestion d'un environnement de pratique sécuritaire incluant les déchets biomédicaux", "type": "lecon"},
                    {"numero": 21, "titre": "Organisation des services", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Érudit",
        "classe_code": "DES-A4",
        "titre": "Érudit – Érudition et rédaction scientifique",
        "ordre": 50,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Érudit en quatrième année :
            
            24. Fait preuve de curiosité scientifique et développe son esprit critique.
            
            25. Contribue aux différentes activités académiques (cours, staff, etc).
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A4-ERUDITION",
                "ordre": 1,
                "titre": "Érudition",
                "volume_horaire": 40,
                "description": "Cours sur l'érudition et la rédaction scientifique (40h).",
                "contenu": textwrap.dedent(
                    """
                    Développement de l'érudition médicale :
                    participation aux clubs de lecture, analyse critique de la littérature,
                    rédaction scientifique, contribution à la production de connaissances.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 22, "titre": "Clubs de lecture", "type": "lecon"},
                    {"numero": 23, "titre": "Rédaction scientifique", "type": "lecon"},
                ],
            },
        ],
    },
    {
        "competence": "Professionnel",
        "classe_code": "DES-A4",
        "titre": "Professionnel – Éthique et déontologie avancées",
        "ordre": 60,
        "description": textwrap.dedent(
            """
            Jalons pour la compétence Professionnel en quatrième année :
            
            19. Respecte la spécificité socioculturelle du patient dans son approche.
            
            20. Tient compte des dimensions éthiques dans les soins aux patients.
            
            21. Reconnaît ses limites et collabore activement à son processus d'apprentissage.
            
            22. Démontre respect et honnêteté dans ses rapports professionnels.
            
            23. Assure une bonne qualité de service à la communauté.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A4-ETHIQUE",
                "ordre": 1,
                "titre": "Éthique",
                "volume_horaire": 6,
                "description": "Cours sur l'éthique médicale avancée (6h).",
                "contenu": textwrap.dedent(
                    """
                    Éthique médicale avancée :
                    discussions éthiques, dilemmes éthiques en pratique médicale,
                    application des principes éthiques dans des situations complexes.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 24, "titre": "Discussions éthique", "type": "lecon"},
                ],
            },
            {
                "code": "DES-A4-DEONTOLOGIE",
                "ordre": 2,
                "titre": "Déontologie",
                "volume_horaire": 6,
                "description": "Cours sur la déontologie médicale (6h).",
                "contenu": textwrap.dedent(
                    """
                    Déontologie médicale :
                    code de bonne conduite professionnelle, cadre réglementaire de la prescription,
                    responsabilité médicale.
                    """
                ).strip(),
                "lecons": [
                    {"numero": 25, "titre": "Code de bonne conduite professionnelle", "type": "lecon"},
                    {"numero": 26, "titre": "Cadre réglementaire de la prescription", "type": "lecon"},
                    {"numero": 27, "titre": "Responsabilité médicale", "type": "lecon"},
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Structure les jalons/cours/leçons UNIQUEMENT pour la QUATRIÈME ANNÉE (DES-A4) du DESMFMC. Pour les autres années, utiliser les commandes correspondantes."

    def add_arguments(self, parser):
        parser.add_argument(
            '--classe',
            default='DES-A4',
            help="Code de la classe cible - DOIT être DES-A4 pour la quatrième année (défaut: DES-A4)."
        )

    @transaction.atomic
    def handle(self, *args, **options):
        classe_code = options['classe']
        try:
            formation = Formation.objects.get(code='DESMFMC')
        except Formation.DoesNotExist as exc:
            raise CommandError("Formation DESMFMC introuvable. Veuillez exécuter les seeds du programme au préalable.") from exc

        # Vérifier que c'est bien la quatrième année
        if classe_code != 'DES-A4':
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  ATTENTION: Cette commande est conçue pour la QUATRIÈME ANNÉE (DES-A4) uniquement. '
                    f'Vous avez spécifié {classe_code}. Les jalons peuvent ne pas correspondre.'
                )
            )
        
        try:
            classe = Classe.objects.get(code=classe_code, formation=formation)
            if classe.annee != 4:
                raise CommandError(
                    f"Cette commande est réservée à la QUATRIÈME ANNÉE (année=4). "
                    f"La classe {classe_code} est en année {classe.annee}."
                )
        except Classe.DoesNotExist as exc:
            raise CommandError(f"Classe {classe_code} introuvable pour la formation DESMFMC.") from exc

        base_date = classe.date_debut or datetime.date.today()
        cours_crees = 0
        lecons_creees = 0
        jalons_crees = 0

        for jalon_data in DES4_JALONS_DATA:
            if jalon_data['classe_code'] != classe_code:
                continue

            competence = self._get_competence(jalon_data['competence'])
            jalon, created = CompetenceJalon.objects.get_or_create(
                competence=competence,
                classe=classe,
                titre=jalon_data['titre'],
                defaults={
                    'description': jalon_data['description'],
                    'ordre': jalon_data['ordre'],
                }
            )

            if created:
                jalons_crees += 1
            else:
                jalon.description = jalon_data['description']
                jalon.ordre = jalon_data['ordre']
                jalon.save()

            # Créer/mettre à jour les cours et leçons
            for course_def in jalon_data.get('courses', []):
                cours_obj, created_cours = self._upsert_course(classe, base_date, course_def)
                if created_cours:
                    cours_crees += 1
                
                # Lier le cours au jalon
                cours_obj.jalons_competence.add(jalon)

                # Créer les leçons
                for lecon_def in course_def.get('lecons', []):
                    lecon_obj, created_lecon = self._upsert_lecon(cours_obj, lecon_def)
                    if created_lecon:
                        lecons_creees += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Seed terminé pour {classe_code}:\n'
                f'  - {jalons_crees} jalons créés\n'
                f'  - {cours_crees} cours créés\n'
                f'  - {lecons_creees} leçons créées\n'
            )
        )

    def _get_competence(self, libelle_competence):
        """Récupère ou crée une compétence par son libellé"""
        competence, _ = Competence.objects.get_or_create(
            libelle=libelle_competence,
            defaults={
                'domaine': 'savoir_faire',
                'description': f'Compétence: {libelle_competence}',
                'niveau_attendu': "Maîtrise opérationnelle à l'issue du programme",
            }
        )
        return competence

    def _upsert_course(self, classe, base_date, course_def):
        """Crée ou met à jour un cours"""
        cours_obj, created = Cours.objects.get_or_create(
            code=course_def['code'],
            classe=classe,
            defaults={
                'titre': course_def['titre'],
                'description': course_def.get('description', ''),
                'contenu': course_def.get('contenu', ''),
                'volume_horaire': course_def.get('volume_horaire', 0),
                'ordre': course_def.get('ordre', 0),
                'date_debut': base_date,
                'date_fin': classe.date_fin or base_date,
                'actif': True,
            }
        )
        
        if not created:
            cours_obj.titre = course_def['titre']
            cours_obj.description = course_def.get('description', '')
            cours_obj.contenu = course_def.get('contenu', '')
            cours_obj.volume_horaire = course_def.get('volume_horaire', 0)
            cours_obj.ordre = course_def.get('ordre', 0)
            cours_obj.save()

        return cours_obj, created

    def _upsert_lecon(self, cours, lecon_def):
        """Crée ou met à jour une leçon"""
        lecon_obj, created = Lecon.objects.get_or_create(
            cours=cours,
            numero=lecon_def['numero'],
            defaults={
                'titre': lecon_def['titre'],
                'type_lecon': lecon_def.get('type', 'lecon'),
                'ordre': lecon_def['numero'],
                'actif': True,
            }
        )
        
        if not created:
            lecon_obj.titre = lecon_def['titre']
            lecon_obj.type_lecon = lecon_def.get('type', 'lecon')
            lecon_obj.ordre = lecon_def['numero']
            lecon_obj.save()

        return lecon_obj, created

