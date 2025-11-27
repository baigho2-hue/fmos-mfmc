"""
Commande de seed pour les jalons, cours et leçons de la PREMIÈRE ANNÉE uniquement du DESMFMC.

⚠️  IMPORTANT: Cette commande est réservée à la classe DES-A1 (année 1) uniquement.
Pour les années 2, 3 et 4, créer des commandes similaires (seed_des2_jalons.py, etc.)
ou utiliser des données spécifiques à chaque année.

Source des données: Document "Compétences et jalons du programme de MFMC.pdf"
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


# ⚠️  DONNÉES UNIQUEMENT POUR LA PREMIÈRE ANNÉE (DES-A1)
DES1_JALONS_DATA = [
    {
        "competence": "Expert médical en MF/MC",
        "classe_code": "DES-A1",
        "titre": "Expert médical – Urgences et médecine de première ligne",
        "ordre": 10,
        "description": textwrap.dedent(
            """
            - Décrit les symptômes et les signes physiques des pathologies courantes.
            - Fait une histoire complète en recueillant des données fiables.
            - Réalise une analyse séméiologique satisfaisante et recherche adéquatement les signes à l'examen physique.
            - Effectue une synthèse structurée et propose au moins trois diagnostics différentiels classés par probabilité.
            - Reconnaît les situations urgentes et applique les gestes de base attendus.
            - Réalise la petite chirurgie (hernies, lipomes) pendant les stages de chirurgie.
            - Réanime un nouveau-né selon les protocoles.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A1-URG",
                "ordre": 1,
                "titre": "Urgence médicale",
                "volume_horaire": 20,
                "description": "Urgences majeures et situations critiques (20h).",
                "contenu": "Arrêt cardio-respiratoire, traumatismes, chocs, intoxications, brûlures, électrocutions et envenimations.",
                "lecons": [
                    {"numero": 1, "titre": "Arrêt cardio-respiratoire", "type": "atelier"},
                    {"numero": 2, "titre": "Traumatisme majeur", "type": "atelier"},
                    {"numero": 3, "titre": "Choc", "type": "atelier"},
                    {"numero": 4, "titre": "Intoxications", "type": "atelier"},
                    {"numero": 5, "titre": "Brûlures", "type": "atelier"},
                    {"numero": 6, "titre": "Électrocution", "type": "atelier"},
                    {"numero": 7, "titre": "Envenimations", "type": "atelier"},
                ],
            },
            {
                "code": "DES-A1-MED",
                "ordre": 2,
                "titre": "Médecine de première ligne",
                "volume_horaire": 44,
                "description": "Médecine interne et pathologies courantes (44h).",
                "contenu": "HTA, arythmies, insuffisance cardiaque, dyspnée, BPCO, diabète, troubles endocriniens et métaboliques.",
                "lecons": [
                    {"numero": 8, "titre": "Hypertension artérielle"},
                    {"numero": 9, "titre": "Arythmies cardiaques"},
                    {"numero": 10, "titre": "Insuffisance cardiaque"},
                    {"numero": 11, "titre": "Douleurs thoraciques"},
                    {"numero": 12, "titre": "Dyspnée cardiaque"},
                    {"numero": 13, "titre": "Toux persistante"},
                    {"numero": 14, "titre": "Épanchements pleuraux"},
                    {"numero": 15, "titre": "BPCO"},
                    {"numero": 16, "titre": "Diabète"},
                    {"numero": 17, "titre": "Troubles thyroïdiens"},
                    {"numero": 18, "titre": "Insuffisance rénale"},
                    {"numero": 19, "titre": "Obésité"},
                    {"numero": 20, "titre": "Dyslipidémies"},
                    {"numero": 21, "titre": "Désordres électrolytiques"},
                ],
            },
        ],
    },
    {
        "competence": "Communicateur",
        "classe_code": "DES-A1",
        "titre": "Communicateur – Documentation clinique et transmission",
        "ordre": 20,
        "description": textwrap.dedent(
            """
            - Note les informations pertinentes au dossier et transmet des synthèses fiables.
            - Rédige une note transférable qui ne nécessite que des corrections mineures.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A1-ANG",
                "ordre": 3,
                "titre": "Anglais médical",
                "volume_horaire": 20,
                "description": "Développement de la communication écrite et orale en anglais médical.",
                "contenu": "Terminologie médicale, présentation de cas cliniques, rédaction de notes.",
                "lecons": [
                    {"numero": 22, "titre": "Anglais médical appliqué"},
                ],
            },
        ],
    },
    {
        "competence": "Collaborateur",
        "classe_code": "DES-A1",
        "titre": "Collaborateur – Coordination interprofessionnelle",
        "ordre": 30,
        "description": textwrap.dedent(
            """
            - Reconnaît les caractéristiques d'une référence/évacuation bien réalisée.
            - Prépare des comptes-rendus contenant toutes les informations pertinentes pour la continuité des soins.
            - Prend des décisions en collégialité et respecte la hiérarchie lorsqu'elle est nécessaire.
            - Sollicite l'expertise des autres professionnels de santé et identifie les opportunités d'impliquer les associations de patients.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Promoteur de la santé",
        "classe_code": "DES-A1",
        "titre": "Promoteur – Santé communautaire et prévention",
        "ordre": 40,
        "description": textwrap.dedent(
            """
            - Vérifie systématiquement la couverture vaccinale.
            - Recherche les antécédents personnels et familiaux facteurs de risque.
            - Intègre les activités de dépistage (pression artérielle, diabète) dans ses consultations.
            - Connaît les messages et outils d'éducation pour les patients diabétiques et hypertendus.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A1-SPC",
                "ordre": 4,
                "titre": "Santé publique et communautaire",
                "volume_horaire": 10,
                "description": "Santé publique, indicateurs et systèmes d'information (10h).",
                "contenu": "Indicateurs de santé, politiques, paquet minimum d'activités et systèmes de référence.",
                "lecons": [
                    {"numero": 23, "titre": "Indicateurs de santé"},
                    {"numero": 24, "titre": "Politique sectorielle de santé"},
                    {"numero": 25, "titre": "Santé communautaire"},
                    {"numero": 26, "titre": "Paquet minimum d'activités"},
                    {"numero": 27, "titre": "Système d'information sanitaire"},
                    {"numero": 28, "titre": "Système de référence / évacuation"},
                ],
            },
        ],
    },
    {
        "competence": "Gestionnaire",
        "classe_code": "DES-A1",
        "titre": "Gestionnaire – Organisation des services",
        "ordre": 50,
        "description": textwrap.dedent(
            """
            - Participe aux comités (accueil, qualité, audit) et aux activités d'organisation des soins.
            - Contribue à la planification et à la mise en œuvre des services en fonction des besoins de la communauté.
            """
        ).strip(),
        "courses": [],
    },
    {
        "competence": "Professionnel",
        "classe_code": "DES-A1",
        "titre": "Professionnel – Éthique et posture clinique",
        "ordre": 60,
        "description": textwrap.dedent(
            """
            - Accueille et salue le malade avec respect.
            - Adopte une attitude professionnelle tenant compte des spécificités socioculturelles.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A1-ETH",
                "ordre": 5,
                "titre": "Éthique et déontologie",
                "volume_horaire": 10,
                "description": "Cadre légal et déontologique de la pratique (10h).",
                "contenu": "Droit, éthique, santé et médecine légale.",
                "lecons": [
                    {"numero": 29, "titre": "Droit, éthique et santé"},
                    {"numero": 30, "titre": "Médecine légale"},
                ],
            },
        ],
    },
    {
        "competence": "Érudit",
        "classe_code": "DES-A1",
        "titre": "Érudit – Compétences numériques et recherche",
        "ordre": 70,
        "description": textwrap.dedent(
            """
            - Réalise des présentations scientifiques de qualité.
            - Planifie le développement de ses compétences en fonction des besoins de sa communauté.
            """
        ).strip(),
        "courses": [
            {
                "code": "DES-A1-INF",
                "ordre": 6,
                "titre": "Informatique médicale",
                "volume_horaire": 10,
                "description": "Compétences numériques essentielles (10h).",
                "contenu": "Word, Excel, PowerPoint appliqués à la pratique clinique.",
                "lecons": [
                    {"numero": 31, "titre": "Word pour les synthèses cliniques"},
                    {"numero": 32, "titre": "Excel pour le suivi de cohorte"},
                    {"numero": 33, "titre": "PowerPoint pour les présentations"},
                ],
            },
            {
                "code": "DES-A1-METH",
                "ordre": 7,
                "titre": "Méthodologie de la recherche",
                "volume_horaire": 10,
                "description": "Méthodes et statistiques de base (10h).",
                "contenu": "Statistique descriptive et plan de recherche.",
                "lecons": [
                    {"numero": 34, "titre": "Statistique descriptive"},
                    {"numero": 35, "titre": "Plan de recherche"},
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Structure les jalons/cours/leçons UNIQUEMENT pour la PREMIÈRE ANNÉE (DES-A1) du DESMFMC selon le référentiel PDF. Pour les années 2, 3 et 4, utiliser d'autres commandes de seed."

    def add_arguments(self, parser):
        parser.add_argument(
            '--classe',
            default='DES-A1',
            help="Code de la classe cible - DOIT être DES-A1 pour la première année (défaut: DES-A1)."
        )

    @transaction.atomic
    def handle(self, *args, **options):
        classe_code = options['classe']
        try:
            formation = Formation.objects.get(code='DESMFMC')
        except Formation.DoesNotExist as exc:
            raise CommandError("Formation DESMFMC introuvable. Veuillez exécuter les seeds du programme au préalable.") from exc

        # Vérifier que c'est bien la première année
        if classe_code != 'DES-A1':
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️  ATTENTION: Cette commande est conçue pour la PREMIÈRE ANNÉE (DES-A1) uniquement. '
                    f'Vous avez spécifié {classe_code}. Les jalons peuvent ne pas correspondre.'
                )
            )
        
        try:
            classe = Classe.objects.get(code=classe_code, formation=formation)
            if classe.annee != 1:
                raise CommandError(
                    f"Cette commande est réservée à la PREMIÈRE ANNÉE (année=1). "
                    f"La classe {classe_code} est en année {classe.annee}."
                )
        except Classe.DoesNotExist as exc:
            raise CommandError(f"Classe {classe_code} introuvable pour la formation DESMFMC.") from exc

        base_date = classe.date_debut or datetime.date.today()
        cours_crees = 0
        lecons_creees = 0
        jalons_crees = 0

        for jalon_data in DES1_JALONS_DATA:
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

            for course_def in jalon_data.get('courses', []):
                cours_obj, created_cours = self._upsert_course(classe, base_date, course_def)
                cours_obj.jalons_competence.add(jalon)
                if created_cours:
                    cours_crees += 1

                created_lecons = self._sync_lecons(cours_obj, course_def.get('lecons', []))
                lecons_creees += created_lecons

        self.stdout.write(self.style.SUCCESS(
            f"Seed terminé : {jalons_crees} jalons créés/actualisés, "
            f"{cours_crees} cours créés, {lecons_creees} leçons synchronisées."
        ))

    def _get_competence(self, libelle):
        competence, _ = Competence.objects.get_or_create(
            libelle=libelle,
            defaults={
                'domaine': 'savoir_faire',
                'description': libelle,
                'niveau_attendu': "Maîtrise opérationnelle à l'issue du programme",
            }
        )
        return competence

    def _upsert_course(self, classe, base_date, course_def):
        date_debut = base_date + datetime.timedelta(days=7 * (course_def['ordre'] - 1))
        date_fin = date_debut + datetime.timedelta(days=6)

        cours_obj, created = Cours.objects.get_or_create(
            code=course_def['code'],
            defaults={
                'classe': classe,
                'titre': course_def['titre'],
                'description': course_def['description'],
                'contenu': course_def['contenu'],
                'volume_horaire': course_def['volume_horaire'],
                'date_debut': date_debut,
                'date_fin': date_fin,
                'ordre': course_def['ordre'],
            }
        )

        if not created:
            cours_obj.classe = classe
            cours_obj.titre = course_def['titre']
            cours_obj.description = course_def['description']
            cours_obj.contenu = course_def['contenu']
            cours_obj.volume_horaire = course_def['volume_horaire']
            cours_obj.date_debut = date_debut
            cours_obj.date_fin = date_fin
            cours_obj.ordre = course_def['ordre']
            cours_obj.save()

        return cours_obj, created

    def _sync_lecons(self, cours, lecons_def):
        created = 0
        existing_numbers = set()

        for lecon_def in lecons_def:
            numero = lecon_def['numero']
            existing_numbers.add(numero)
            lecon, lecon_created = Lecon.objects.get_or_create(
                cours=cours,
                numero=numero,
                defaults={
                    'titre': lecon_def['titre'],
                    'type_lecon': lecon_def.get('type', 'lecon'),
                    'ordre': numero,
                    'contenu': lecon_def.get('contenu', ''),
                    'duree_estimee': lecon_def.get('duree_estimee', 60),
                }
            )
            if not lecon_created:
                lecon.titre = lecon_def['titre']
                lecon.type_lecon = lecon_def.get('type', 'lecon')
                lecon.ordre = numero
                lecon.contenu = lecon_def.get('contenu', '')
                lecon.duree_estimee = lecon_def.get('duree_estimee', 60)
                lecon.save()
            else:
                created += 1

        # Optionally, deactivate leçons no longer listed
        cours.lecons.exclude(numero__in=existing_numbers).update(actif=False)
        return created

