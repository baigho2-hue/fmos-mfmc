# PROGRAMME_DESMFMC_DONNEES.py
"""
Fichier de données pour le programme DESMFMC
À compléter avec les informations du PDF "Programme DES de MF-MC.pdf"

Structure attendue :
- Jalons par année et semestre
- Modules dans chaque jalon
- Cours dans chaque module (à créer dans les classes)
- Volumes horaires
- Objectifs et compétences
"""

# Structure du programme DESMFMC sur 4 ans
# À compléter avec les données exactes du PDF

PROGRAMME_DESMFMC = {
    'formation': {
        'nom': 'Diplôme d\'Études Spécialisées en Médecine de Famille et Médecine Communautaire',
        'code': 'DESMFMC',
        'type_formation': 'initiale',
        'nature': 'certifiante',
        'duree_annees': 4,
        'objectifs_generaux': '''
        Former des médecins compétents en médecine de famille et communautaire capables de :
        - Prendre en charge les besoins de santé des populations dans divers contextes
        - Développer des compétences approfondies en médecine générale
        - Maîtriser les approches communautaires de la santé
        - Contribuer à l'amélioration de l'accès aux soins de santé primaires
        ''',
        'competences_visées': '''
        - Compétences en médecine générale et soins primaires
        - Compétences en pédiatrie, gynécologie, psychiatrie
        - Compétences en médecine d'urgence
        - Compétences en santé publique et épidémiologie
        - Compétences en communication et relation patient
        - Compétences en gestion de cas complexes
        - Compétences en médecine communautaire
        ''',
        'prerequis': 'Diplôme de médecine et réussite du concours d\'entrée',
        'debouches': '''
        - Médecin de famille en pratique libérale ou publique
        - Médecin communautaire dans les CSCom
        - Responsable de centre de santé
        - Enseignant en médecine de famille
        - Chercheur en santé communautaire
        '''
    },
    
    # Structure par année et semestre
    'jalons': {
        1: {  # Année 1
            1: {  # Semestre 1
                'nom': 'Fondamentaux de la médecine de famille',
                'code': 'DESMFMC-A1-S1',
                'description': 'Introduction aux concepts fondamentaux et compétences de base',
                'modules': [
                    # À compléter avec les modules exacts du PDF
                    {
                        'nom': 'Médecine générale de base',
                        'code': 'MGB-A1-S1',
                        'volume_horaire': 0,  # À remplir
                        'description': '',
                        'cours': []  # Liste des cours à créer
                    }
                ]
            },
            2: {  # Semestre 2
                'nom': 'Pathologies courantes',
                'code': 'DESMFMC-A1-S2',
                'description': '',
                'modules': []
            }
        },
        2: {  # Année 2
            1: {
                'nom': 'Médecine spécialisée appliquée',
                'code': 'DESMFMC-A2-S1',
                'description': '',
                'modules': []
            },
            2: {
                'nom': 'Médecine d\'urgence',
                'code': 'DESMFMC-A2-S2',
                'description': '',
                'modules': []
            }
        },
        3: {  # Année 3
            1: {
                'nom': 'Médecine communautaire',
                'code': 'DESMFMC-A3-S1',
                'description': '',
                'modules': []
            },
            2: {
                'nom': 'Gestion et leadership',
                'code': 'DESMFMC-A3-S2',
                'description': '',
                'modules': []
            }
        },
        4: {  # Année 4
            1: {
                'nom': 'Stage clinique avancé',
                'code': 'DESMFMC-A4-S1',
                'description': '',
                'modules': []
            },
            2: {
                'nom': 'Préparation professionnelle',
                'code': 'DESMFMC-A4-S2',
                'description': '',
                'modules': []
            }
        }
    }
}

# Instructions pour compléter :
# 1. Lire le PDF "Programme DES de MF-MC.pdf"
# 2. Pour chaque année et semestre, noter :
#    - Le nom exact du jalon
#    - Les modules avec leurs volumes horaires
#    - Les cours dans chaque module
#    - Les objectifs et compétences
# 3. Mettre à jour ce fichier avec les données exactes
# 4. Exécuter : python manage.py init_programme_desmfmc

