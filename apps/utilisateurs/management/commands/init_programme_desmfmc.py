# apps/utilisateurs/management/commands/init_programme_desmfmc.py
"""
Commande Django pour initialiser la structure de base du programme DESMFMC
Usage: python manage.py init_programme_desmfmc
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from apps.utilisateurs.models_formation import Formation
from apps.utilisateurs.models_programme_desmfmc import JalonProgramme, ModuleProgramme


class Command(BaseCommand):
    help = 'Initialise la structure de base du programme DESMFMC avec jalons et modules'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Début de l\'initialisation du programme DESMFMC...'))
        
        # Récupérer ou créer la formation DESMFMC
        formation, created = Formation.objects.get_or_create(
            code='DESMFMC',
            defaults={
                'nom': 'Diplôme d\'Études Spécialisées en Médecine de Famille et Médecine Communautaire',
                'description': 'Programme de formation post-universitaire de 4 ans préparant les médecins à devenir des spécialistes en médecine de famille.',
                'type_formation': 'initiale',
                'nature': 'certifiante',
                'duree_annees': 4,
                'duree_heures': 0,  # Sera calculé automatiquement
                'objectifs_generaux': 'Former des médecins compétents en médecine de famille et communautaire, capables de prendre en charge les besoins de santé des populations dans divers contextes.',
                'competences_visées': 'Compétences en médecine générale, pédiatrie, gynécologie, psychiatrie, médecine d\'urgence, santé publique, communication, gestion de cas complexes.',
                'prerequis': 'Diplôme de médecine et réussite du concours d\'entrée.',
                'debouches': 'Médecin de famille, médecin communautaire, responsable de centre de santé, enseignant en médecine de famille.',
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Formation DESMFMC créée avec succès.'))
        else:
            self.stdout.write(self.style.WARNING(f'Formation DESMFMC existe déjà.'))
        
        # Structure de base du programme (à compléter avec le document fourni)
        structure_programme = {
            1: {  # Année 1
                1: {  # Semestre 1
                    'nom': 'Fondamentaux de la médecine de famille',
                    'code': 'DESMFMC-A1-S1',
                    'modules': [
                        {
                            'nom': 'Médecine générale de base',
                            'code': 'MGB-A1-S1',
                            'volume_horaire': 120,
                            'description': 'Introduction aux concepts fondamentaux de la médecine de famille et aux compétences de base.'
                        },
                        {
                            'nom': 'Communication médicale',
                            'code': 'COM-A1-S1',
                            'volume_horaire': 80,
                            'description': 'Techniques de communication patient-médecin et entretien clinique.'
                        },
                        {
                            'nom': 'Systèmes de santé et santé publique',
                            'code': 'SSP-A1-S1',
                            'volume_horaire': 60,
                            'description': 'Organisation des soins primaires, santé publique et épidémiologie.'
                        }
                    ]
                },
                2: {  # Semestre 2
                    'nom': 'Pathologies courantes en médecine de famille',
                    'code': 'DESMFMC-A1-S2',
                    'modules': [
                        {
                            'nom': 'Pathologies infectieuses',
                            'code': 'INF-A1-S2',
                            'volume_horaire': 100,
                            'description': 'Prise en charge des infections courantes en médecine de famille.'
                        },
                        {
                            'nom': 'Pathologies cardiovasculaires',
                            'code': 'CARD-A1-S2',
                            'volume_horaire': 100,
                            'description': 'Diagnostic et prise en charge des pathologies cardiovasculaires.'
                        },
                        {
                            'nom': 'Pathologies respiratoires',
                            'code': 'RESP-A1-S2',
                            'volume_horaire': 80,
                            'description': 'Prise en charge des pathologies respiratoires courantes.'
                        }
                    ]
                }
            },
            2: {  # Année 2
                1: {
                    'nom': 'Médecine spécialisée appliquée',
                    'code': 'DESMFMC-A2-S1',
                    'modules': [
                        {
                            'nom': 'Pédiatrie en médecine de famille',
                            'code': 'PED-A2-S1',
                            'volume_horaire': 120,
                            'description': 'Soins pédiatriques en contexte de médecine de famille.'
                        },
                        {
                            'nom': 'Gynécologie et obstétrique',
                            'code': 'GYN-A2-S1',
                            'volume_horaire': 100,
                            'description': 'Suivi gynécologique et obstétrical en soins primaires.'
                        }
                    ]
                },
                2: {
                    'nom': 'Médecine d\'urgence et soins critiques',
                    'code': 'DESMFMC-A2-S2',
                    'modules': [
                        {
                            'nom': 'Urgences médicales',
                            'code': 'URG-A2-S2',
                            'volume_horaire': 120,
                            'description': 'Prise en charge des urgences médicales en soins primaires.'
                        },
                        {
                            'nom': 'Réanimation et soins critiques',
                            'code': 'REA-A2-S2',
                            'volume_horaire': 80,
                            'description': 'Bases de la réanimation et des soins critiques.'
                        }
                    ]
                }
            },
            3: {  # Année 3
                1: {
                    'nom': 'Médecine communautaire et santé publique',
                    'code': 'DESMFMC-A3-S1',
                    'modules': [
                        {
                            'nom': 'Santé communautaire',
                            'code': 'SCOM-A3-S1',
                            'volume_horaire': 120,
                            'description': 'Approches communautaires de la santé et promotion de la santé.'
                        },
                        {
                            'nom': 'Épidémiologie et recherche',
                            'code': 'EPI-A3-S1',
                            'volume_horaire': 100,
                            'description': 'Méthodes épidémiologiques et initiation à la recherche.'
                        }
                    ]
                },
                2: {
                    'nom': 'Gestion et leadership en santé',
                    'code': 'DESMFMC-A3-S2',
                    'modules': [
                        {
                            'nom': 'Gestion des structures de santé',
                            'code': 'GEST-A3-S2',
                            'volume_horaire': 100,
                            'description': 'Gestion administrative et financière des structures de santé.'
                        },
                        {
                            'nom': 'Leadership et management d\'équipe',
                            'code': 'LEAD-A3-S2',
                            'volume_horaire': 80,
                            'description': 'Compétences en leadership et gestion d\'équipe médicale.'
                        }
                    ]
                }
            },
            4: {  # Année 4
                1: {
                    'nom': 'Stage clinique avancé et spécialisation',
                    'code': 'DESMFMC-A4-S1',
                    'modules': [
                        {
                            'nom': 'Stage en médecine de famille',
                            'code': 'STAGE-A4-S1',
                            'volume_horaire': 200,
                            'description': 'Stage pratique approfondi en médecine de famille.'
                        },
                        {
                            'nom': 'Mémoire de fin d\'études',
                            'code': 'MEM-A4-S1',
                            'volume_horaire': 100,
                            'description': 'Travail de recherche et rédaction du mémoire.'
                        }
                    ]
                },
                2: {
                    'nom': 'Préparation à la pratique professionnelle',
                    'code': 'DESMFMC-A4-S2',
                    'modules': [
                        {
                            'nom': 'Éthique et déontologie médicale',
                            'code': 'ETH-A4-S2',
                            'volume_horaire': 60,
                            'description': 'Éthique médicale et déontologie en pratique de famille.'
                        },
                        {
                            'nom': 'Insertion professionnelle',
                            'code': 'INS-A4-S2',
                            'volume_horaire': 80,
                            'description': 'Préparation à l\'insertion professionnelle et développement de carrière.'
                        }
                    ]
                }
            }
        }
        
        # Calculer la date de début (1er octobre de l'année en cours)
        annee_actuelle = date.today().year
        date_debut_base = date(annee_actuelle, 10, 1)
        
        total_heures = 0
        jalons_crees = 0
        modules_crees = 0
        
        # Créer les jalons et modules
        for annee, semestres in structure_programme.items():
            for semestre, jalon_data in semestres.items():
                # Calculer les dates du jalon (6 mois par semestre)
                date_debut = date_debut_base.replace(year=date_debut_base.year + annee - 1)
                if semestre == 2:
                    date_debut = date_debut.replace(month=4)  # Avril pour le semestre 2
                date_fin = date_debut + timedelta(days=180)  # ~6 mois
                
                # Calculer le volume horaire total du jalon
                volume_horaire_jalon = sum(m['volume_horaire'] for m in jalon_data['modules'])
                total_heures += volume_horaire_jalon
                
                # Créer le jalon
                jalon, created = JalonProgramme.objects.get_or_create(
                    formation=formation,
                    code=jalon_data['code'],
                    defaults={
                        'nom': jalon_data['nom'],
                        'annee': annee,
                        'semestre': semestre,
                        'ordre': semestre,
                        'date_debut': date_debut,
                        'date_fin': date_fin,
                        'volume_horaire_total': volume_horaire_jalon,
                        'description': f'Jalon {annee}-{semestre} du programme DESMFMC'
                    }
                )
                
                if created:
                    jalons_crees += 1
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Jalon créé : {jalon.nom}'))
                
                # Créer les modules du jalon
                for idx, module_data in enumerate(jalon_data['modules'], 1):
                    module, created = ModuleProgramme.objects.get_or_create(
                        jalon=jalon,
                        code=module_data['code'],
                        defaults={
                            'nom': module_data['nom'],
                            'description': module_data['description'],
                            'volume_horaire': module_data['volume_horaire'],
                            'ordre': idx,
                            'actif': True
                        }
                    )
                    
                    if created:
                        modules_crees += 1
                        self.stdout.write(self.style.SUCCESS(f'    ✓ Module créé : {module.nom}'))
        
        # Mettre à jour le volume horaire total de la formation
        formation.duree_heures = total_heures
        formation.save()
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Initialisation terminée !'))
        self.stdout.write(self.style.SUCCESS(f'  - Jalons créés : {jalons_crees}'))
        self.stdout.write(self.style.SUCCESS(f'  - Modules créés : {modules_crees}'))
        self.stdout.write(self.style.SUCCESS(f'  - Volume horaire total : {total_heures} heures'))
        self.stdout.write(self.style.WARNING(
            f'\n⚠️  PROCHAINES ÉTAPES :\n'
            f'1. Pour une structure plus détaillée, utilisez : python manage.py init_programme_desmfmc_detaille\n'
            f'2. Créer les cours dans les classes appropriées via l\'admin Django\n'
            f'3. Lier les cours aux modules via CoursProgramme\n'
            f'4. Ajouter les objectifs d\'apprentissage et compétences\n'
            f'5. Ajuster selon le PDF "Programme DES de MF-MC.pdf" si nécessaire'
        ))

