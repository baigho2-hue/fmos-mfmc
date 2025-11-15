# apps/utilisateurs/management/commands/creer_utilisateurs_test.py
"""
Commande pour créer des utilisateurs de test (étudiants et enseignants)
Usage: python manage.py creer_utilisateurs_test
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models import Utilisateur


class Command(BaseCommand):
    help = 'Cree des utilisateurs de test (etudiants et enseignants)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Creation des utilisateurs de test ===\n'))
        
        # Liste des étudiants de test
        etudiants = [
            {
                'username': 'etudiant1',
                'email': 'etudiant1@fmos-mfmc.ml',
                'password': 'etudiant123',
                'first_name': 'Amadou',
                'last_name': 'Diallo',
                'classe': 'DESMFMC 1ère année',
                'type_utilisateur': 'etudiant'
            },
            {
                'username': 'etudiant2',
                'email': 'etudiant2@fmos-mfmc.ml',
                'password': 'etudiant123',
                'first_name': 'Fatoumata',
                'last_name': 'Traoré',
                'classe': 'DESMFMC 1ère année',
                'type_utilisateur': 'etudiant'
            },
            {
                'username': 'etudiant3',
                'email': 'etudiant3@fmos-mfmc.ml',
                'password': 'etudiant123',
                'first_name': 'Ibrahim',
                'last_name': 'Keita',
                'classe': 'DESMFMC 2ème année',
                'type_utilisateur': 'etudiant'
            },
            {
                'username': 'etudiant4',
                'email': 'etudiant4@fmos-mfmc.ml',
                'password': 'etudiant123',
                'first_name': 'Aissata',
                'last_name': 'Sangaré',
                'classe': 'DESMFMC 2ème année',
                'type_utilisateur': 'etudiant'
            },
            {
                'username': 'etudiant5',
                'email': 'etudiant5@fmos-mfmc.ml',
                'password': 'etudiant123',
                'first_name': 'Moussa',
                'last_name': 'Coulibaly',
                'classe': 'DESMFMC 3ème année',
                'type_utilisateur': 'etudiant'
            },
        ]
        
        # Liste des enseignants de test
        enseignants = [
            {
                'username': 'enseignant1',
                'email': 'enseignant1@fmos-mfmc.ml',
                'password': 'enseignant123',
                'first_name': 'Dr. Mamadou',
                'last_name': 'Diakité',
                'matieres': 'Médecine de famille, Pathologies courantes',
                'type_utilisateur': 'enseignant',
                'niveau_acces': 'complet'
            },
            {
                'username': 'enseignant2',
                'email': 'enseignant2@fmos-mfmc.ml',
                'password': 'enseignant123',
                'first_name': 'Dr. Awa',
                'last_name': 'Konaté',
                'matieres': 'Médecine communautaire, Santé publique',
                'type_utilisateur': 'enseignant',
                'niveau_acces': 'complet'
            },
            {
                'username': 'enseignant3',
                'email': 'enseignant3@fmos-mfmc.ml',
                'password': 'enseignant123',
                'first_name': 'Dr. Boubacar',
                'last_name': 'Sissoko',
                'matieres': 'Pédiatrie, Gynécologie et obstétrique',
                'type_utilisateur': 'enseignant',
                'niveau_acces': 'standard'
            },
            {
                'username': 'enseignant4',
                'email': 'enseignant4@fmos-mfmc.ml',
                'password': 'enseignant123',
                'first_name': 'Dr. Kadiatou',
                'last_name': 'Dembélé',
                'matieres': 'Médecine d\'urgence, Soins critiques',
                'type_utilisateur': 'enseignant',
                'niveau_acces': 'complet'
            },
        ]
        
        etudiants_crees = 0
        enseignants_crees = 0
        erreurs = 0
        
        # Créer les étudiants
        self.stdout.write(self.style.SUCCESS('\n--- Creation des etudiants ---'))
        for etudiant_data in etudiants:
            username = etudiant_data['username']
            email = etudiant_data['email']
            
            # Vérifier si l'utilisateur existe déjà
            if Utilisateur.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'  [SKIP] {username} existe deja'))
                continue
            
            if Utilisateur.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f'  [SKIP] Email {email} existe deja'))
                continue
            
            try:
                user = Utilisateur.objects.create_user(
                    username=username,
                    email=email,
                    password=etudiant_data['password'],
                    first_name=etudiant_data['first_name'],
                    last_name=etudiant_data['last_name'],
                    classe=etudiant_data['classe'],
                    type_utilisateur=etudiant_data['type_utilisateur'],
                    email_verifie=True,  # Pour les tests, on considère les emails vérifiés
                    is_active=True
                )
                etudiants_crees += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  [OK] {username} ({etudiant_data["first_name"]} {etudiant_data["last_name"]}) - {etudiant_data["classe"]}'
                ))
            except Exception as e:
                erreurs += 1
                self.stdout.write(self.style.ERROR(f'  [ERREUR] {username}: {e}'))
        
        # Créer les enseignants
        self.stdout.write(self.style.SUCCESS('\n--- Creation des enseignants ---'))
        for enseignant_data in enseignants:
            username = enseignant_data['username']
            email = enseignant_data['email']
            
            # Vérifier si l'utilisateur existe déjà
            if Utilisateur.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f'  [SKIP] {username} existe deja'))
                continue
            
            if Utilisateur.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f'  [SKIP] Email {email} existe deja'))
                continue
            
            try:
                user = Utilisateur.objects.create_user(
                    username=username,
                    email=email,
                    password=enseignant_data['password'],
                    first_name=enseignant_data['first_name'],
                    last_name=enseignant_data['last_name'],
                    matieres=enseignant_data['matieres'],
                    type_utilisateur=enseignant_data['type_utilisateur'],
                    niveau_acces=enseignant_data['niveau_acces'],
                    email_verifie=True,  # Pour les tests, on considère les emails vérifiés
                    is_active=True
                )
                enseignants_crees += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  [OK] {username} ({enseignant_data["first_name"]} {enseignant_data["last_name"]}) - {enseignant_data["niveau_acces"]}'
                ))
            except Exception as e:
                erreurs += 1
                self.stdout.write(self.style.ERROR(f'  [ERREUR] {username}: {e}'))
        
        # Résumé
        self.stdout.write(self.style.SUCCESS(
            f'\n=== Resume ===\n'
            f'Etudiants crees: {etudiants_crees}/{len(etudiants)}\n'
            f'Enseignants crees: {enseignants_crees}/{len(enseignants)}\n'
            f'Erreurs: {erreurs}'
        ))
        
        if etudiants_crees > 0 or enseignants_crees > 0:
            self.stdout.write(self.style.SUCCESS(
                f'\n=== Identifiants de connexion ===\n'
                f'ETUDIANTS:\n'
                f'  - Username: etudiant1, etudiant2, etc.\n'
                f'  - Password: etudiant123\n\n'
                f'ENSEIGNANTS:\n'
                f'  - Username: enseignant1, enseignant2, etc.\n'
                f'  - Password: enseignant123'
            ))

