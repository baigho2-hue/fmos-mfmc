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
        
        # Les 7 compétences de base du MFMC (CanMEDS adapté)
        competences_mfmc = [
            {
                'libelle': 'Expert médical',
                'domaine': 'savoir_faire',
                'description': textwrap.dedent("""
                    Le médecin de famille et communautaire est un expert médical qui :
                    • Dispense des soins curatifs, préventifs et promotionnels de première ligne
                    • Prend en charge les besoins de santé des populations dans divers contextes
                    • Développe des compétences approfondies en médecine générale
                    • Maîtrise les soins aux enfants, aux femmes, aux adultes et aux personnes âgées
                    • Gère les urgences et les cas complexes en contexte de ressources limitées
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Maîtrise des compétences cliniques essentielles en médecine de famille, capacité à 
                    diagnostiquer et traiter les problèmes de santé courants et complexes, aptitude à 
                    gérer les situations d'urgence en contexte de soins primaires.
                """).strip(),
            },
            {
                'libelle': 'Communicateur',
                'domaine': 'savoir_etre',
                'description': textwrap.dedent("""
                    Le médecin de famille et communautaire est un communicateur qui :
                    • Établit une relation thérapeutique continue et personnalisée avec les patients
                    • Communique efficacement avec les patients, les familles et les communautés
                    • Adapte sa communication au contexte culturel et linguistique
                    • Facilite la compréhension et l'adhésion aux soins
                    • Transmet des informations de santé de manière claire et accessible
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Capacité à établir une relation de confiance avec les patients et leur famille, 
                    maîtrise des techniques de communication thérapeutique, aptitude à adapter le 
                    message selon le niveau de compréhension et le contexte culturel.
                """).strip(),
            },
            {
                'libelle': 'Collaborateur',
                'domaine': 'savoir_etre',
                'description': textwrap.dedent("""
                    Le médecin de famille et communautaire est un collaborateur qui :
                    • Travaille en équipe avec les professionnels de santé et les acteurs communautaires
                    • Collabore avec les ressources professionnelles et communautaires du réseau de soins
                    • Participe activement aux équipes multidisciplinaires
                    • Coordonne les soins avec les autres intervenants du système de santé
                    • Développe des partenariats efficaces pour améliorer l'accès aux soins
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Capacité à travailler en équipe, aptitude à coordonner les soins avec d'autres 
                    professionnels, compétence à développer et maintenir des partenariats efficaces 
                    dans le réseau de soins.
                """).strip(),
            },
            {
                'libelle': 'Promoteur de la santé',
                'domaine': 'savoir_faire',
                'description': textwrap.dedent("""
                    Le médecin de famille et communautaire est un promoteur de la santé qui :
                    • Assure le leadership en prévention, promotion de la santé et intervention communautaire
                    • Développe et met en œuvre des programmes de promotion de la santé
                    • Éduque les patients et les communautés sur les comportements favorables à la santé
                    • Participe aux activités de santé publique et d'éducation sanitaire
                    • Contribue à l'amélioration de la santé de la population
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Capacité à concevoir et mettre en œuvre des interventions de promotion de la santé, 
                    aptitude à éduquer et sensibiliser les populations, compétence à développer des 
                    programmes de prévention adaptés au contexte communautaire.
                """).strip(),
            },
            {
                'libelle': 'Gestionnaire',
                'domaine': 'savoir_faire',
                'description': textwrap.dedent("""
                    Le médecin de famille et communautaire est un gestionnaire qui :
                    • Gère et organise des services de santé accessibles, disponibles et de qualité
                    • Assure la gestion des services de première ligne et des programmes nationaux
                    • Optimise l'utilisation des ressources disponibles
                    • Planifie et coordonne les activités de soins
                    • Assure la continuité et la qualité des soins
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Capacité à gérer efficacement les ressources humaines, matérielles et financières, 
                    aptitude à organiser et coordonner les services de santé, compétence à assurer 
                    la qualité et la continuité des soins.
                """).strip(),
            },
            {
                'libelle': 'Érudit',
                'domaine': 'savoir',
                'description': textwrap.dedent("""
                    Le médecin de famille et communautaire est un érudit qui :
                    • Maintient et développe ses compétences par une démarche d'auto-apprentissage
                    • Pratique la médecine fondée sur les preuves (evidence-based medicine)
                    • Développe une capacité d'analyse critique et de recherche-action
                    • Contribue à la production de connaissances en santé communautaire
                    • Partage ses connaissances avec ses pairs et la communauté
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Capacité à maintenir ses compétences à jour, aptitude à analyser de manière critique 
                    la littérature médicale, compétence à mener des activités de recherche-action et 
                    à contribuer à l'avancement des connaissances.
                """).strip(),
            },
            {
                'libelle': 'Professionnel',
                'domaine': 'savoir_etre',
                'description': textwrap.dedent("""
                    Le médecin de famille et communautaire est un professionnel qui :
                    • Intervient avec professionnalisme et éthique dans tous les contextes de pratique
                    • Respecte les valeurs professionnelles et les principes déontologiques
                    • Développe une pratique réflexive et améliore continuellement sa pratique
                    • S'engage envers la communauté et la santé publique
                    • Fait preuve d'intégrité, d'empathie et de responsabilité
                """).strip(),
                'niveau_attendu': textwrap.dedent("""
                    Capacité à exercer avec intégrité et éthique, aptitude à développer une pratique 
                    réflexive, compétence à s'engager de manière responsable envers les patients, 
                    la communauté et la profession.
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

