"""
Commande pour mettre à jour les compétences avec les 7 compétences générales
Remplace les compétences spécifiques par les 7 compétences générales du programme DESMFMC
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.utilisateurs.models_formation import Competence


# Les 7 compétences générales du programme DESMFMC
COMPETENCES_GENERALES = [
    {
        'libelle': 'Expert médical',
        'domaine': 'savoir_faire',
        'description': 'Démontre un bon niveau de connaissances théoriques et cliniques dans l\'évaluation et les soins qu\'il prodigue aux patients. Recueille les données cliniques pertinentes, effectue adéquatement l\'examen physique, interprète les données et choisit un plan d\'intervention approprié.',
        'niveau_attendu': 'Maîtrise des compétences cliniques de base et avancées en médecine de famille et communautaire, capacité à gérer les problèmes de santé courants et complexes.'
    },
    {
        'libelle': 'Communicateur',
        'domaine': 'savoir_etre',
        'description': 'Démontre des habiletés relationnelles et de communication empreintes d\'empathie et de respect avec les patients et leur famille. Transmet clairement les informations médicales dans un langage adapté. Rédige les documents médicaux de façon claire et pertinente.',
        'niveau_attendu': 'Communication efficace avec les patients, les familles et les membres de l\'équipe de soins, adaptation du langage au contexte et à l\'auditoire.'
    },
    {
        'libelle': 'Collaborateur',
        'domaine': 'savoir_etre',
        'description': 'Reconnaît l\'expertise et la contribution des autres professionnels de la santé dans les soins aux patients et dans son propre apprentissage. Sollicite de façon pertinente la collaboration de tous les acteurs pour optimiser la qualité des soins.',
        'niveau_attendu': 'Travail en équipe efficace, reconnaissance de l\'expertise des autres, collaboration interprofessionnelle et communautaire.'
    },
    {
        'libelle': 'Promoteur de la Santé',
        'domaine': 'savoir_faire',
        'description': 'Démontre qu\'il connaît les recommandations des programmes nationaux. Identifie les facteurs de risque et de récidive de certaines pathologies. Inclut systématiquement dans ses consultations les recommandations de dépistage et de guidance quant à la malnutrition, infections respiratoires, maladies diarrhéiques, paludisme, VIH-SIDA, IST.',
        'niveau_attendu': 'Application des principes de prévention et de promotion de la santé, intégration des programmes nationaux de santé publique dans la pratique clinique.'
    },
    {
        'libelle': 'Gestionnaire',
        'domaine': 'savoir_faire',
        'description': 'Peut expliquer le fonctionnement et le rôle des ASACO dans l\'organisation des services et la prestation des soins. Participe activement aux différents comités d\'évaluation et aux activités de monitorage. Contribue à l\'élaboration et à l\'implantation des stratégies avancées et du micro plan sanitaire. Démontre des connaissances de base en comptabilité et gestion.',
        'niveau_attendu': 'Gestion efficace des ressources, participation à la planification et à l\'organisation des services de santé, maîtrise des outils de gestion de base.'
    },
    {
        'libelle': 'Professionnel',
        'domaine': 'savoir_etre',
        'description': 'Respecte la spécificité socioculturelle du patient et tient compte des dimensions éthiques dans son approche. Démontre respect et honnêteté dans ses rapports professionnels. Assure une bonne qualité et continuité de service aux patients et à la communauté en se positionnant comme médecin traitant et gestionnaire responsable.',
        'niveau_attendu': 'Pratique professionnelle éthique, respect des valeurs et de la culture des patients, engagement envers la qualité des soins et la continuité.'
    },
    {
        'libelle': 'Érudit',
        'domaine': 'savoir',
        'description': 'Contribue à l\'éducation des patients, de la communauté et des différents membres de l\'équipe de soins en partageant de manière adaptée son savoir. Fait preuve de curiosité scientifique et collabore activement au développement de ses compétences. Applique de façon critique les données probantes selon le contexte de pratique et la réalité des patients et des communautés.',
        'niveau_attendu': 'Apprentissage continu, application de la médecine fondée sur les preuves, contribution à l\'éducation et à la formation, développement professionnel continu.'
    },
]


class Command(BaseCommand):
    help = "Met à jour les compétences avec les 7 compétences générales du programme DESMFMC"

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force la mise à jour même si les compétences existent déjà'
        )
        parser.add_argument(
            '--delete-old',
            action='store_true',
            help='Supprime les anciennes compétences qui ne correspondent pas aux 7 compétences générales'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        force = options.get('force', False)
        delete_old = options.get('delete_old', False)
        
        print('\n' + '=' * 70)
        print('  MISE À JOUR DES COMPÉTENCES GÉNÉRALES')
        print('=' * 70 + '\n')
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('  MISE À JOUR DES COMPÉTENCES GÉNÉRALES'))
        self.stdout.write(self.style.SUCCESS('=' * 70 + '\n'))
        
        # Compter les compétences existantes
        competences_existantes = Competence.objects.all()
        self.stdout.write(f'Compétences existantes : {competences_existantes.count()}')
        
        # Créer ou mettre à jour les 7 compétences générales
        competences_creees = []
        competences_mises_a_jour = []
        
        for comp_data in COMPETENCES_GENERALES:
            libelle = comp_data['libelle']
            competence, created = Competence.objects.get_or_create(
                libelle=libelle,
                defaults={
                    'domaine': comp_data['domaine'],
                    'description': comp_data['description'],
                    'niveau_attendu': comp_data['niveau_attendu']
                }
            )
            
            if created:
                competences_creees.append(libelle)
                self.stdout.write(self.style.SUCCESS(f'✅ Créée : {libelle}'))
            else:
                if force:
                    # Mettre à jour les champs
                    competence.domaine = comp_data['domaine']
                    competence.description = comp_data['description']
                    competence.niveau_attendu = comp_data['niveau_attendu']
                    competence.save()
                    competences_mises_a_jour.append(libelle)
                    self.stdout.write(self.style.WARNING(f'🔄 Mise à jour : {libelle}'))
                else:
                    self.stdout.write(self.style.HTTP_INFO(f'ℹ️  Existe déjà : {libelle}'))
        
        # Supprimer les anciennes compétences si demandé
        if delete_old:
            libelles_generales = [c['libelle'] for c in COMPETENCES_GENERALES]
            anciennes_competences = Competence.objects.exclude(libelle__in=libelles_generales)
            count_anciennes = anciennes_competences.count()
            
            if count_anciennes > 0:
                self.stdout.write(f'\n⚠️  {count_anciennes} ancienne(s) compétence(s) à supprimer :')
                for comp in anciennes_competences:
                    self.stdout.write(f'   - {comp.libelle}')
                
                # Vérifier si ces compétences sont liées à des jalons ou cours
                for comp in anciennes_competences:
                    jalons_count = comp.jalons_competence.count()
                    if jalons_count > 0:
                        self.stdout.write(
                            self.style.WARNING(
                                f'   ⚠️  {comp.libelle} est liée à {jalons_count} jalon(s) - non supprimée'
                            )
                        )
                    else:
                        comp.delete()
                        self.stdout.write(self.style.SUCCESS(f'   ✅ Supprimée : {comp.libelle}'))
        
        # Résumé
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('  RÉSUMÉ'))
        self.stdout.write('=' * 70)
        self.stdout.write(f'Compétences créées : {len(competences_creees)}')
        self.stdout.write(f'Compétences mises à jour : {len(competences_mises_a_jour)}')
        self.stdout.write(f'Total des compétences générales : {Competence.objects.filter(libelle__in=[c["libelle"] for c in COMPETENCES_GENERALES]).count()}/7')
        self.stdout.write(self.style.SUCCESS('\n✅ Mise à jour terminée !\n'))

