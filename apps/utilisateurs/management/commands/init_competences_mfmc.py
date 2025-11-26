# apps/utilisateurs/management/commands/init_competences_mfmc.py
"""
Commande pour initialiser les 7 compétences de base du Médecin de Famille Médecin Communautaire (MFMC)
Basées sur le cadre CanMEDS adapté au contexte du DESMFMC
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models_formation import Competence
import textwrap


class Command(BaseCommand):
    help = 'Initialise les 7 compétences de base du Médecin de Famille Médecin Communautaire (MFMC)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Initialisation des 7 compétences de base MFMC ===\n'))
        
        # Les 7 compétences générales de base du DESMFMC
        competences_mfmc = [
            {
                'libelle': 'Expert médical en MF/MC',
                'domaine': 'savoir_faire',
                'description': textwrap.dedent("""
                    Dispenser l'ensemble des soins curatifs, préventifs et promotionnels de première
                    ligne dans une aire de santé ou auprès d'une population dont il a la responsabilité.
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Maîtrise opérationnelle à l'issue du programme.
                """).strip(),
            },
            {
                'libelle': 'Communicateur',
                'domaine': 'savoir_etre',
                'description': textwrap.dedent("""
                    Développer une relation de confiance, continue et personnalisée avec les patients et
                    leur communauté, basée sur la compréhension globale de leur réalité et leurs perspectives.
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Maîtrise opérationnelle à l'issue du programme.
                """).strip(),
            },
            {
                'libelle': 'Collaborateur',
                'domaine': 'savoir_etre',
                'description': textwrap.dedent("""
                    Travailler en étroite collaboration avec les différentes ressources professionnelles et
                    communautaires de son milieu de même qu'avec celles du réseau de soins.
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Maîtrise opérationnelle à l'issue du programme.
                """).strip(),
            },
            {
                'libelle': 'Promoteur de la santé',
                'domaine': 'savoir_faire',
                'description': textwrap.dedent("""
                    Assumer un leadership en matière de prévention, de promotion de la santé et
                    d'intervention communautaire auprès de la population qu'il dessert.
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Maîtrise opérationnelle à l'issue du programme.
                """).strip(),
            },
            {
                'libelle': 'Gestionnaire',
                'domaine': 'savoir_faire',
                'description': textwrap.dedent("""
                    Gérer la planification et la mise en œuvre de services de qualité et de stratégies
                    avancées efficaces en fonction des besoins de la communauté.
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Maîtrise opérationnelle à l'issue du programme.
                """).strip(),
            },
            {
                'libelle': 'Professionnel',
                'domaine': 'savoir_etre',
                'description': textwrap.dedent("""
                    Intervenir avec professionnalisme et de manière éthique auprès des patients et des
                    autres membres du réseau de soins.
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Maîtrise opérationnelle à l'issue du programme.
                """).strip(),
            },
            {
                'libelle': 'Érudit',
                'domaine': 'savoir',
                'description': textwrap.dedent("""
                    Planifier le maintien et le développement de ses compétences professionnelles en
                    fonction des besoins normatifs et de sa communauté.
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Maîtrise opérationnelle à l'issue du programme.
                """).strip(),
            },
        ]
        
        competences_creees = 0
        competences_mises_a_jour = 0
        
        for comp_data in competences_mfmc:
            competence, created = Competence.objects.get_or_create(
                libelle=comp_data['libelle'],
                defaults={
                    'domaine': comp_data['domaine'],
                    'description': comp_data['description'],
                    'niveau_attendu': comp_data['niveau_attendu'],
                }
            )
            
            if created:
                competences_creees += 1
                self.stdout.write(
                    self.style.SUCCESS(f'[OK] Competence creee : {comp_data["libelle"]}')
                )
            else:
                # Mettre à jour les compétences existantes
                competence.domaine = comp_data['domaine']
                competence.description = comp_data['description']
                competence.niveau_attendu = comp_data['niveau_attendu']
                competence.save()
                competences_mises_a_jour += 1
                self.stdout.write(
                    self.style.WARNING(f'[UPDATE] Competence mise a jour : {comp_data["libelle"]}')
                )
        
        self.stdout.write(self.style.SUCCESS(
            f'\n=== Résumé ===\n'
            f'Compétences créées : {competences_creees}\n'
            f'Compétences mises à jour : {competences_mises_a_jour}\n'
            f'Total : {len(competences_mfmc)} compétences de base MFMC\n'
        ))
        
        # Afficher la liste complète
        self.stdout.write(self.style.SUCCESS('\n=== Liste des 7 compétences de base MFMC ==='))
        for i, comp in enumerate(competences_mfmc, 1):
            self.stdout.write(f'{i}. {comp["libelle"]} ({comp["domaine"]})')

