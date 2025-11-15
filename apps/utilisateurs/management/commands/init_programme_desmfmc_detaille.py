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
            1: {  # ANNÉE 1
                1: {  # Semestre 1
                    'nom': 'Fondamentaux de la médecine de famille',
                    'code': 'DESMFMC-A1-S1',
                    'description': 'Introduction aux concepts fondamentaux de la médecine de famille et aux compétences de base',
                    'modules': [
                        {
                            'nom': 'Introduction à la médecine de famille',
                            'code': 'INTRO-MF-A1-S1',
                            'volume_horaire': 40,
                            'description': 'Concepts fondamentaux, histoire, philosophie et valeurs de la médecine de famille'
                        },
                        {
                            'nom': 'Médecine générale de base',
                            'code': 'MGB-A1-S1',
                            'volume_horaire': 120,
                            'description': 'Compétences de base en médecine générale, histoire clinique, examen physique, décision clinique'
                        },
                        {
                            'nom': 'Communication médicale',
                            'code': 'COM-A1-S1',
                            'volume_horaire': 80,
                            'description': 'Techniques de communication patient-médecin, entretien clinique, relation thérapeutique'
                        },
                        {
                            'nom': 'Systèmes de santé et santé publique',
                            'code': 'SSP-A1-S1',
                            'volume_horaire': 60,
                            'description': 'Organisation des soins primaires, systèmes de santé, santé publique, épidémiologie de base'
                        },
                        {
                            'nom': 'Anatomie et physiologie appliquées',
                            'code': 'ANA-PHY-A1-S1',
                            'volume_horaire': 60,
                            'description': 'Anatomie et physiologie appliquées à la pratique clinique'
                        }
                    ]
                },
                2: {  # Semestre 2
                    'nom': 'Pathologies courantes en médecine de famille',
                    'code': 'DESMFMC-A1-S2',
                    'description': 'Prise en charge des pathologies les plus fréquentes en médecine de famille',
                    'modules': [
                        {
                            'nom': 'Pathologies infectieuses',
                            'code': 'INF-A1-S2',
                            'volume_horaire': 100,
                            'description': 'Diagnostic et prise en charge des infections courantes (respiratoires, digestives, urinaires, cutanées)'
                        },
                        {
                            'nom': 'Pathologies cardiovasculaires',
                            'code': 'CARD-A1-S2',
                            'volume_horaire': 100,
                            'description': 'Hypertension, insuffisance cardiaque, cardiopathies ischémiques, troubles du rythme'
                        },
                        {
                            'nom': 'Pathologies respiratoires',
                            'code': 'RESP-A1-S2',
                            'volume_horaire': 80,
                            'description': 'Asthme, BPCO, pneumonies, tuberculose, pathologies respiratoires chroniques'
                        },
                        {
                            'nom': 'Pathologies digestives',
                            'code': 'DIG-A1-S2',
                            'volume_horaire': 60,
                            'description': 'Pathologies digestives courantes, hépatites, troubles digestifs fonctionnels'
                        },
                        {
                            'nom': 'Pathologies endocriniennes et métaboliques',
                            'code': 'ENDO-A1-S2',
                            'volume_horaire': 60,
                            'description': 'Diabète, troubles thyroïdiens, obésité, dyslipidémies'
                        }
                    ]
                }
            },
            2: {  # ANNÉE 2
                1: {  # Semestre 1
                    'nom': 'Médecine spécialisée appliquée',
                    'code': 'DESMFMC-A2-S1',
                    'description': 'Application des spécialités médicales en contexte de médecine de famille',
                    'modules': [
                        {
                            'nom': 'Pédiatrie en médecine de famille',
                            'code': 'PED-A2-S1',
                            'volume_horaire': 120,
                            'description': 'Soins pédiatriques, croissance et développement, pathologies pédiatriques courantes, vaccination'
                        },
                        {
                            'nom': 'Gynécologie et obstétrique',
                            'code': 'GYN-A2-S1',
                            'volume_horaire': 100,
                            'description': 'Suivi gynécologique, contraception, suivi de grossesse, accouchement normal, pathologies gynécologiques'
                        },
                        {
                            'nom': 'Psychiatrie et santé mentale',
                            'code': 'PSY-A2-S1',
                            'volume_horaire': 80,
                            'description': 'Troubles de l\'humeur, anxiété, psychoses, addictions, santé mentale en soins primaires'
                        },
                        {
                            'nom': 'Dermatologie',
                            'code': 'DERM-A2-S1',
                            'volume_horaire': 60,
                            'description': 'Pathologies dermatologiques courantes, infections cutanées, eczémas, dermatoses'
                        }
                    ]
                },
                2: {  # Semestre 2
                    'nom': 'Médecine d\'urgence et soins critiques',
                    'code': 'DESMFMC-A2-S2',
                    'description': 'Prise en charge des urgences médicales et situations critiques',
                    'modules': [
                        {
                            'nom': 'Urgences médicales',
                            'code': 'URG-A2-S2',
                            'volume_horaire': 120,
                            'description': 'Prise en charge des urgences médicales en soins primaires, triage, gestes d\'urgence'
                        },
                        {
                            'nom': 'Réanimation et soins critiques',
                            'code': 'REA-A2-S2',
                            'volume_horaire': 80,
                            'description': 'Bases de la réanimation, support vital de base et avancé, soins critiques'
                        },
                        {
                            'nom': 'Traumatologie',
                            'code': 'TRAUMA-A2-S2',
                            'volume_horaire': 60,
                            'description': 'Prise en charge des traumatismes, fractures, plaies, brûlures'
                        },
                        {
                            'nom': 'Toxicologie et intoxications',
                            'code': 'TOX-A2-S2',
                            'volume_horaire': 40,
                            'description': 'Intoxications aiguës, morsures, piqûres, toxicologie clinique'
                        }
                    ]
                }
            },
            3: {  # ANNÉE 3
                1: {  # Semestre 1
                    'nom': 'Médecine communautaire et santé publique',
                    'code': 'DESMFMC-A3-S1',
                    'description': 'Approches communautaires de la santé et santé publique',
                    'modules': [
                        {
                            'nom': 'Santé communautaire',
                            'code': 'SCOM-A3-S1',
                            'volume_horaire': 120,
                            'description': 'Approches communautaires de la santé, promotion de la santé, participation communautaire'
                        },
                        {
                            'nom': 'Épidémiologie et recherche',
                            'code': 'EPI-A3-S1',
                            'volume_horaire': 100,
                            'description': 'Méthodes épidémiologiques, recherche en santé, statistiques appliquées, lecture critique'
                        },
                        {
                            'nom': 'Médecine préventive',
                            'code': 'PREV-A3-S1',
                            'volume_horaire': 80,
                            'description': 'Dépistage, prévention primaire, secondaire, tertiaire, vaccination, éducation pour la santé'
                        },
                        {
                            'nom': 'Santé environnementale',
                            'code': 'ENV-A3-S1',
                            'volume_horaire': 40,
                            'description': 'Impact de l\'environnement sur la santé, santé au travail'
                        }
                    ]
                },
                2: {  # Semestre 2
                    'nom': 'Gestion et leadership en santé',
                    'code': 'DESMFMC-A3-S2',
                    'description': 'Compétences en gestion et leadership pour la pratique médicale',
                    'modules': [
                        {
                            'nom': 'Gestion des structures de santé',
                            'code': 'GEST-A3-S2',
                            'volume_horaire': 100,
                            'description': 'Gestion administrative, financière et logistique des structures de santé'
                        },
                        {
                            'nom': 'Leadership et management d\'équipe',
                            'code': 'LEAD-A3-S2',
                            'volume_horaire': 80,
                            'description': 'Compétences en leadership, gestion d\'équipe médicale, communication professionnelle'
                        },
                        {
                            'nom': 'Qualité et sécurité des soins',
                            'code': 'QUAL-A3-S2',
                            'volume_horaire': 60,
                            'description': 'Assurance qualité, gestion des risques, sécurité des patients'
                        },
                        {
                            'nom': 'Économie de la santé',
                            'code': 'ECO-A3-S2',
                            'volume_horaire': 40,
                            'description': 'Économie de la santé, financement, coûts des soins, efficience'
                        }
                    ]
                }
            },
            4: {  # ANNÉE 4
                1: {  # Semestre 1
                    'nom': 'Stage clinique avancé et spécialisation',
                    'code': 'DESMFMC-A4-S1',
                    'description': 'Stage pratique approfondi et travail de recherche',
                    'modules': [
                        {
                            'nom': 'Stage en médecine de famille',
                            'code': 'STAGE-A4-S1',
                            'volume_horaire': 200,
                            'description': 'Stage pratique approfondi en médecine de famille dans les CSCom-U et structures de soins primaires'
                        },
                        {
                            'nom': 'Mémoire de fin d\'études',
                            'code': 'MEM-A4-S1',
                            'volume_horaire': 100,
                            'description': 'Travail de recherche, rédaction et soutenance du mémoire de fin d\'études'
                        },
                        {
                            'nom': 'Préparation aux examens',
                            'code': 'EXAM-A4-S1',
                            'volume_horaire': 40,
                            'description': 'Préparation aux examens de fin de formation, révision, simulation'
                        }
                    ]
                },
                2: {  # Semestre 2
                    'nom': 'Préparation à la pratique professionnelle',
                    'code': 'DESMFMC-A4-S2',
                    'description': 'Finalisation de la formation et préparation à l\'insertion professionnelle',
                    'modules': [
                        {
                            'nom': 'Éthique et déontologie médicale',
                            'code': 'ETH-A4-S2',
                            'volume_horaire': 60,
                            'description': 'Éthique médicale, déontologie, responsabilité professionnelle, droits des patients'
                        },
                        {
                            'nom': 'Insertion professionnelle',
                            'code': 'INS-A4-S2',
                            'volume_horaire': 80,
                            'description': 'Préparation à l\'insertion professionnelle, développement de carrière, réseaux professionnels'
                        },
                        {
                            'nom': 'Formation continue et développement professionnel',
                            'code': 'FCDP-A4-S2',
                            'volume_horaire': 40,
                            'description': 'Stratégies de formation continue, développement professionnel continu, veille scientifique'
                        },
                        {
                            'nom': 'Projet professionnel',
                            'code': 'PROJ-A4-S2',
                            'volume_horaire': 40,
                            'description': 'Élaboration du projet professionnel, planification de carrière'
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

