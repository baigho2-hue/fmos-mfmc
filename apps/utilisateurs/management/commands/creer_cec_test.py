# apps/utilisateurs/management/commands/creer_cec_test.py
"""
Commande pour créer un utilisateur CEC (Chargé d'Encadrement Clinique) de test
Usage: python manage.py creer_cec_test
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_programme_desmfmc import CSComUCentre


class Command(BaseCommand):
    help = 'Crée un utilisateur CEC (superviseur clinique) de test pour tester le système d\'évaluations de stages'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Création d\'un utilisateur CEC de test ===\n'))
        
        # Informations de l'utilisateur CEC de test
        username = 'cec_test'
        email = 'cec_test@fmos-mfmc.ml'
        password = 'cec123456'
        
        # Récupérer ou créer un centre CSCom-U de test pour le superviseur
        centre_test = CSComUCentre.objects.filter(actif=True).first()
        if not centre_test:
            # Créer un centre de test si aucun n'existe
            centre_test = CSComUCentre.objects.create(
                nom='CSCom-U Test',
                code='CSCOM-TEST',
                type_centre='urbain',
                localisation='Bamako',
                actif=True
            )
            self.stdout.write(self.style.SUCCESS(f'[OK] Centre de test "{centre_test.nom}" cree.'))
        
        # Vérifier si l'utilisateur existe déjà
        if Utilisateur.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'L\'utilisateur "{username}" existe deja.'))
            user = Utilisateur.objects.get(username=username)
            
            # Mettre à jour les champs nécessaires
            user.type_utilisateur = 'enseignant'
            user.superviseur_cec = True
            user.centre_supervision = centre_test
            user.email_verifie = True
            user.is_active = True
            user.set_password(password)
            user.save()
            
            self.stdout.write(self.style.SUCCESS(f'[OK] Utilisateur "{username}" mis a jour avec le statut CEC et centre de supervision.'))
        else:
            # Créer l'utilisateur
            user = Utilisateur.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='Dr. Mamadou',
                last_name='Cisse',
                telephone='+223 20 12 34 56',
                type_utilisateur='enseignant',
                superviseur_cec=True,
                centre_supervision=centre_test,
                email_verifie=True,
                is_active=True,
                matieres='Medecine de famille, Sante communautaire, Encadrement clinique',
                niveau_acces='complet'
            )
            
            self.stdout.write(self.style.SUCCESS(f'[OK] Utilisateur CEC "{username}" cree avec succes.'))
        
        # Afficher les informations de connexion
        self.stdout.write(self.style.SUCCESS('\n=== Informations de connexion ==='))
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'\nStatut: Enseignant + Superviseur/CEC')
        self.stdout.write(f'Centre de supervision: {user.centre_supervision.nom if user.centre_supervision else "Non assigne"}')
        self.stdout.write(f'Email verifie: Oui')
        self.stdout.write(f'Actif: Oui')
        
        self.stdout.write(self.style.SUCCESS('\n=== Instructions de test ==='))
        self.stdout.write('1. Connectez-vous avec les identifiants ci-dessus')
        self.stdout.write('2. Allez dans "Espace Enseignant" -> "Evaluations de stages"')
        self.stdout.write('3. Les evaluations seront automatiquement filtrees par votre centre de supervision')
        self.stdout.write('4. Vous devrez activer le 2FA (double authentification)')
        self.stdout.write('5. Apres activation du 2FA, vous pourrez acceder aux evaluations de stages')
        self.stdout.write('\n=== URLs de test ===')
        self.stdout.write('- Connexion: http://127.0.0.1:8000/login/')
        self.stdout.write('- Dashboard enseignant: http://127.0.0.1:8000/dashboard/enseignant/')
        self.stdout.write('- Evaluations de stages: http://127.0.0.1:8000/superviseur/evaluations-stages/')
        self.stdout.write('- Activer 2FA: http://127.0.0.1:8000/2fa/activer/')
        
        self.stdout.write(self.style.SUCCESS('\n[OK] Utilisateur CEC de test pret !'))

