# apps/utilisateurs/management/commands/init_programme_desmfmc_detaille.py
"""
Commande Django pour initialiser le programme DESMFMC avec structure détaillée
Basé sur le PDF "Programme DES de MF-MC.pdf"

Usage: python manage.py init_programme_desmfmc_detaille
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from apps.utilisateurs.models_formation import Formation
from apps.utilisateurs.models_programme_desmfmc import JalonProgramme, ModuleProgramme


class Command(BaseCommand):
    help = 'Initialise le programme DESMFMC avec structure détaillée basée sur le PDF'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Initialisation du programme DESMFMC ===\n'))
        
        # Récupérer ou créer la formation DESMFMC
        formation, created = Formation.objects.get_or_create(
            code='DESMFMC',
            defaults={
                'nom': 'Diplôme d\'Études Spécialisées en Médecine de Famille et Médecine Communautaire',
                'description': '''Le DESMFMC est un programme de formation post-universitaire de 4 ans qui prépare 
                les médecins à devenir des spécialistes en médecine de famille. Ce programme combine formation 
                théorique rigoureuse et expérience clinique pratique dans divers contextes de soins, notamment 
                dans les Centres de Santé Communautaires à vocation universitaire (CSCom-U).''',
                'type_formation': 'initiale',
                'nature': 'certifiante',
                'duree_annees': 4,
                'duree_heures': 0,  # Sera calculé
                'objectifs_generaux': '''Former des médecins compétents en médecine de famille et communautaire 
                capables de prendre en charge les besoins de santé des populations dans divers contextes, 
                développer des compétences approfondies en médecine générale, maîtriser les approches communautaires 
                de la santé, et contribuer à l'amélioration de l'accès aux soins de santé primaires.''',
                'competences_visées': '''Compétences en médecine générale et soins primaires, pédiatrie, gynécologie, 
                psychiatrie, médecine d'urgence, santé publique et épidémiologie, communication et relation patient, 
                gestion de cas complexes, médecine communautaire.''',
                'prerequis': 'Diplôme de médecine et réussite du concours d\'entrée',
                'debouches': '''Médecin de famille en pratique libérale ou publique, médecin communautaire dans les 
                CSCom, responsable de centre de santé, enseignant en médecine de famille, chercheur en santé communautaire.''',
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Formation DESMFMC creee'))
        else:
            self.stdout.write(self.style.WARNING('[INFO] Formation DESMFMC existe deja'))
        
        # ============================================
        # STRUCTURE DÉTAILLÉE DU PROGRAMME
        # À compléter avec les données exactes du PDF
        # ============================================
        
        structure_programme = {
            1: {  # ANNÉE 1 (144h Théorie + Stages cliniques)
                1: {  # Semestre 1
                    'nom': 'Fondamentaux et Urgences',
                    'code': 'DESMFMC-A1-S1',
                    'description': 'Formation théorique fondamentale et début des rotations cliniques',
                    'modules': [
                        {
                            'nom': 'Soins aux enfants (Pédiatrie)',
                            'code': 'PED-A1',
                            'volume_horaire': 20,
                            'description': 'Problèmes courants chez l\'enfant, maladies fébriles, infections, développement'
                        },
                        {
                            'nom': 'Soins périnataux',
                            'code': 'PERI-A1',
                            'volume_horaire': 15,
                            'description': 'Grossesse, accouchement, allaitement, planification familiale'
                        },
                        {
                            'nom': 'Soins en santé mentale',
                            'code': 'PSY-A1',
                            'volume_horaire': 20,
                            'description': 'Problèmes de santé mentale courants, anxiété, dépression'
                        },
                        {
                            'nom': 'Soins urgents majeurs',
                            'code': 'URG-A1',
                            'volume_horaire': 20,
                            'description': 'Arrêt cardio-respiratoire, coma, traumatisme, choc'
                        },
                        {
                            'nom': 'Réanimation du nouveau-né',
                            'code': 'REA-NN-A1',
                            'volume_horaire': 6,
                            'description': 'Techniques de réanimation néonatale'
                        },
                        {
                            'nom': 'Urgences obstétricales (Niveau I)',
                            'code': 'URG-OBS1-A1',
                            'volume_horaire': 21,
                            'description': 'GESTA - Niveau I'
                        },
                        {
                            'nom': 'Habiletés chirurgicales',
                            'code': 'CHIR-A1',
                            'volume_horaire': 35,
                            'description': 'FIRST - Techniques chirurgicales de base'
                        }
                    ]
                },
                2: {  # Semestre 2
                    'nom': 'Pratique Clinique et Éthique',
                    'code': 'DESMFMC-A1-S2',
                    'description': 'Suite des rotations cliniques et formation éthique',
                    'modules': [
                        {
                            'nom': 'Discussions éthiques (Niveau 1)',
                            'code': 'ETH-A1',
                            'volume_horaire': 3,
                            'description': 'Introduction à l\'éthique médicale'
                        },
                        {
                            'nom': 'Responsabilités administratives',
                            'code': 'ADM-A1',
                            'volume_horaire': 4,
                            'description': 'Relations avec le personnel et instances locales'
                        }
                    ]
                }
            },
            2: {  # ANNÉE 2 (165h Théorie + CSCOM-U)
                1: {  # Semestre 1
                    'nom': 'Pathologies et Urgences Avancées',
                    'code': 'DESMFMC-A2-S1',
                    'description': 'Approfondissement des pathologies et urgences',
                    'modules': [
                        {
                            'nom': 'Troubles psychiatriques aigus',
                            'code': 'PSY-AIGU-A2',
                            'volume_horaire': 6,
                            'description': 'Psychose aiguë, tentative suicidaire'
                        },
                        {
                            'nom': 'Urgences obstétricales (Niveau II)',
                            'code': 'URG-OBS2-A2',
                            'volume_horaire': 21,
                            'description': 'GESTA - Niveau II'
                        },
                        {
                            'nom': 'Problèmes urgents courants',
                            'code': 'URG-COUR-A2',
                            'volume_horaire': 30,
                            'description': 'Infections aiguës, traumatismes mineurs, douleur aiguë'
                        },
                        {
                            'nom': 'Cardiologie',
                            'code': 'CARD-A2',
                            'volume_horaire': 18,
                            'description': 'HTA, arythmies, insuffisance cardiaque'
                        },
                        {
                            'nom': 'Pneumologie',
                            'code': 'PNEU-A2',
                            'volume_horaire': 12,
                            'description': 'Toux, épanchements pleuraux'
                        }
                    ]
                },
                2: {  # Semestre 2
                    'nom': 'Médecine Spécialisée et Chronique',
                    'code': 'DESMFMC-A2-S2',
                    'description': 'Prise en charge des maladies chroniques et spécialités',
                    'modules': [
                        {
                            'nom': 'Endocrinologie',
                            'code': 'ENDO-A2',
                            'volume_horaire': 14,
                            'description': 'Diabète, désordres thyroïdiens'
                        },
                        {
                            'nom': 'Santé des femmes',
                            'code': 'FEM-A2',
                            'volume_horaire': 20,
                            'description': 'Gynécologie courante, ménopause, violence'
                        },
                        {
                            'nom': 'Problèmes fréquents adulte/ado',
                            'code': 'FREQ-A2',
                            'volume_horaire': 20,
                            'description': 'Asthme, dermato, gastro, locomoteur'
                        },
                        {
                            'nom': 'Suivi maladies chroniques',
                            'code': 'CHRON-A2',
                            'volume_horaire': 20,
                            'description': 'HTA, diabète, VIH, Tuberculose'
                        },
                        {
                            'nom': 'Discussions éthiques (Niveau 2)',
                            'code': 'ETH-A2',
                            'volume_horaire': 4,
                            'description': 'Éthique clinique'
                        }
                    ]
                }
            },
            3: {  # ANNÉE 3 (175h Théorie + CSCOM-U)
                1: {  # Semestre 1
                    'nom': 'Gériatrie et Communication',
                    'code': 'DESMFMC-A3-S1',
                    'description': 'Soins aux personnes âgées et communication',
                    'modules': [
                        {
                            'nom': 'Soins aux personnes âgées',
                            'code': 'GER-A3',
                            'volume_horaire': 24,
                            'description': 'Problèmes gériatriques, démence, chutes'
                        },
                        {
                            'nom': 'Soins en fin de vie',
                            'code': 'PAL-A3',
                            'volume_horaire': 30,
                            'description': 'Gestion de la douleur et problèmes de fin de vie'
                        },
                        {
                            'nom': 'Communication médecin-patient',
                            'code': 'COM-PAT-A3',
                            'volume_horaire': 18,
                            'description': 'Entrevue, approche centrée patient'
                        },
                        {
                            'nom': 'Communication et sc. comportementales',
                            'code': 'COM-COMP-A3',
                            'volume_horaire': 21,
                            'description': 'Troubles psychiques, annonce mauvaise nouvelle'
                        }
                    ]
                },
                2: {  # Semestre 2
                    'nom': 'Santé Publique et Recherche',
                    'code': 'DESMFMC-A3-S2',
                    'description': 'Santé communautaire, gestion et recherche',
                    'modules': [
                        {
                            'nom': 'Communication (Deuil/Mort)',
                            'code': 'COM-DEUIL-A3',
                            'volume_horaire': 9,
                            'description': 'Deuil, mort, souffrance, approche familiale'
                        },
                        {
                            'nom': 'Santé publique/communautaire',
                            'code': 'SP-A3',
                            'volume_horaire': 20,
                            'description': 'Indicateurs, politique sectorielle, PMA'
                        },
                        {
                            'nom': 'Suivi enfant et prévention',
                            'code': 'PREV-A3',
                            'volume_horaire': 9,
                            'description': 'Vaccination, examen périodique'
                        },
                        {
                            'nom': 'Modification habitudes de vie',
                            'code': 'HAB-A3',
                            'volume_horaire': 6,
                            'description': 'Modèles de changement'
                        },
                        {
                            'nom': 'Planification et réunions',
                            'code': 'PLAN-A3',
                            'volume_horaire': 9,
                            'description': 'Animation de réunions, rapports'
                        },
                        {
                            'nom': 'Informatique médicale',
                            'code': 'INFO-A3',
                            'volume_horaire': 10,
                            'description': 'Outils informatiques'
                        },
                        {
                            'nom': 'Méthodologie de la recherche',
                            'code': 'RECH-A3',
                            'volume_horaire': 10,
                            'description': 'Bases de la recherche'
                        },
                        {
                            'nom': 'Clubs de lecture (Niveau 1)',
                            'code': 'CLUB-A3',
                            'volume_horaire': 10,
                            'description': 'Analyse critique'
                        }
                    ]
                }
            },
            4: {  # ANNÉE 4 (133h Théorie + CSCOM non-U)
                1: {  # Semestre 1
                    'nom': 'Gestion et Professionnalisme',
                    'code': 'DESMFMC-A4-S1',
                    'description': 'Gestion pratique et aspects légaux',
                    'modules': [
                        {
                            'nom': 'Gestion pratique',
                            'code': 'GEST-A4',
                            'volume_horaire': 30,
                            'description': 'Planification budgétaire, gestion personnel'
                        },
                        {
                            'nom': 'Clubs de lecture (Niveau 2)',
                            'code': 'CLUB-A4',
                            'volume_horaire': 10,
                            'description': 'Analyse critique avancée'
                        },
                        {
                            'nom': 'Rédaction scientifique',
                            'code': 'RED-A4',
                            'volume_horaire': 30,
                            'description': 'Rédaction mémoire/thèse'
                        },
                        {
                            'nom': 'Anglais médical',
                            'code': 'ANG-A4',
                            'volume_horaire': 20,
                            'description': 'Anglais professionnel'
                        }
                    ]
                },
                2: {  # Semestre 2
                    'nom': 'Éthique et Déontologie',
                    'code': 'DESMFMC-A4-S2',
                    'description': 'Aspects légaux et déontologiques',
                    'modules': [
                        {
                            'nom': 'Droit éthique et santé',
                            'code': 'DROIT-A4',
                            'volume_horaire': 10,
                            'description': 'Droit médical'
                        },
                        {
                            'nom': 'Médecine légale',
                            'code': 'LEG-A4',
                            'volume_horaire': 10,
                            'description': 'Bases de médecine légale'
                        },
                        {
                            'nom': 'Aspects déontologiques',
                            'code': 'DEON-A4',
                            'volume_horaire': 6,
                            'description': 'Code de déontologie, responsabilité'
                        },
                        {
                            'nom': 'Discussions éthiques (Final)',
                            'code': 'ETH-A4',
                            'volume_horaire': 17,
                            'description': 'Synthèse éthique'
                        }
                    ]
                }
            }
        }
        
        # Calculer les dates (année académique : octobre à septembre)
        annee_actuelle = date.today().year
        date_debut_base = date(annee_actuelle, 10, 1)  # 1er octobre
        
        total_heures = 0
        jalons_crees = 0
        modules_crees = 0
        
        self.stdout.write(self.style.SUCCESS('\n=== Création des jalons et modules ===\n'))
        
        # Créer les jalons et modules
        for annee, semestres in structure_programme.items():
            self.stdout.write(self.style.SUCCESS(f'\n--- Année {annee} ---'))
            
            for semestre, jalon_data in semestres.items():
                # Calculer les dates du jalon
                annee_jalon = annee_actuelle + annee - 1
                if semestre == 1:
                    date_debut = date(annee_jalon, 10, 1)  # Octobre
                    date_fin = date(annee_jalon + 1, 3, 31)  # Fin mars
                else:  # semestre 2
                    date_debut = date(annee_jalon + 1, 4, 1)  # Avril
                    date_fin = date(annee_jalon + 1, 9, 30)  # Fin septembre
                
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
                        'description': jalon_data.get('description', '')
                    }
                )
                
                if created:
                    jalons_crees += 1
                    self.stdout.write(self.style.SUCCESS(f'  [OK] Jalon cree : {jalon.nom} ({volume_horaire_jalon}h)'))
                else:
                    self.stdout.write(self.style.WARNING(f'  [INFO] Jalon existe deja : {jalon.nom}'))
                
                # Créer les modules du jalon
                for idx, module_data in enumerate(jalon_data['modules'], 1):
                    module, created = ModuleProgramme.objects.get_or_create(
                        jalon=jalon,
                        code=module_data['code'],
                        defaults={
                            'nom': module_data['nom'],
                            'description': module_data.get('description', ''),
                            'volume_horaire': module_data['volume_horaire'],
                            'ordre': idx,
                            'actif': True
                        }
                    )
                    
                    if created:
                        modules_crees += 1
                        self.stdout.write(self.style.SUCCESS(f'    [OK] Module : {module.nom} ({module.volume_horaire}h)'))
                    else:
                        self.stdout.write(self.style.WARNING(f'    [INFO] Module existe deja : {module.nom}'))
        
        # Mettre à jour le volume horaire total de la formation
        formation.duree_heures = total_heures
        formation.save()
        
        self.stdout.write(self.style.SUCCESS(f'\n=== Resume ==='))
        self.stdout.write(self.style.SUCCESS(f'[OK] Jalons crees/mis a jour : {jalons_crees}'))
        self.stdout.write(self.style.SUCCESS(f'[OK] Modules crees/mis a jour : {modules_crees}'))
        self.stdout.write(self.style.SUCCESS(f'[OK] Volume horaire total : {total_heures} heures'))
        self.stdout.write(self.style.WARNING(
            f'\n[INFO] PROCHAINES ETAPES :\n'
            f'1. Creer les cours dans les classes appropriees via l\'admin Django\n'
            f'2. Lier les cours aux modules via CoursProgramme\n'
            f'3. Ajouter les objectifs d\'apprentissage et competences\n'
            f'4. Assigner les enseignants aux cours\n'
            f'5. Ajuster les volumes horaires selon le PDF si necessaire'
        ))

