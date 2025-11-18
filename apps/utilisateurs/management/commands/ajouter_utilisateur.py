"""
Commande Django pour ajouter facilement des utilisateurs
Usage: python manage.py ajouter_utilisateur
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models import Utilisateur
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Ajoute un nouvel utilisateur de manière interactive'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Nom d\'utilisateur'
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Adresse email'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Mot de passe'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['etudiant', 'enseignant'],
            default='etudiant',
            help='Type d\'utilisateur (etudiant ou enseignant)'
        )
        parser.add_argument(
            '--prenom',
            type=str,
            help='Prénom'
        )
        parser.add_argument(
            '--nom',
            type=str,
            help='Nom'
        )
        parser.add_argument(
            '--classe',
            type=str,
            help='Classe (pour étudiants)'
        )
        parser.add_argument(
            '--matieres',
            type=str,
            help='Matières enseignées (pour enseignants, séparées par des virgules)'
        )
        parser.add_argument(
            '--niveau-acces',
            type=str,
            choices=['limite', 'standard', 'complet'],
            default='standard',
            help='Niveau d\'accès (pour enseignants)'
        )
        parser.add_argument(
            '--superuser',
            action='store_true',
            help='Créer un superutilisateur'
        )
        parser.add_argument(
            '--non-interactif',
            action='store_true',
            help='Mode non-interactif (nécessite tous les paramètres)'
        )

    def handle(self, *args, **options):
        mode_interactif = not options.get('non_interactif', False)
        
        # Mode interactif
        if mode_interactif and not all([options.get('username'), options.get('email'), options.get('password')]):
            self.stdout.write(self.style.SUCCESS('\n=== Création d\'un nouvel utilisateur ===\n'))
            
            username = options.get('username') or input('Username: ')
            email = options.get('email') or input('Email: ')
            password = options.get('password') or input('Mot de passe: ')
            type_user = options.get('type') or input('Type (etudiant/enseignant) [etudiant]: ') or 'etudiant'
            prenom = options.get('prenom') or input('Prénom (optionnel): ')
            nom = options.get('nom') or input('Nom (optionnel): ')
            
            if type_user == 'etudiant':
                classe = options.get('classe') or input('Classe (ex: Médecine 6): ')
            else:
                classe = None
                matieres = options.get('matieres') or input('Matières enseignées (séparées par virgules): ')
                niveau_acces = options.get('niveau_acces') or input('Niveau d\'accès (limite/standard/complet) [standard]: ') or 'standard'
            
            superuser = options.get('superuser') or (input('Superutilisateur ? (o/n) [n]: ').lower() == 'o')
        else:
            # Mode non-interactif
            username = options['username']
            email = options['email']
            password = options['password']
            type_user = options['type']
            prenom = options.get('prenom', '')
            nom = options.get('nom', '')
            classe = options.get('classe')
            matieres = options.get('matieres')
            niveau_acces = options.get('niveau_acces', 'standard')
            superuser = options.get('superuser', False)
        
        # Validation
        if not username or not email or not password:
            self.stdout.write(self.style.ERROR('Erreur: Username, email et mot de passe sont obligatoires.'))
            return
        
        # Vérifier si l'utilisateur existe déjà
        if Utilisateur.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'Erreur: L\'utilisateur "{username}" existe déjà.'))
            return
        
        if Utilisateur.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'Erreur: L\'email "{email}" est déjà utilisé.'))
            return
        
        # Créer l'utilisateur
        try:
            if superuser:
                user = Utilisateur.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name=prenom,
                    last_name=nom,
                    type_utilisateur=type_user,
                    classe=classe if type_user == 'etudiant' else None,
                    matieres=matieres if type_user == 'enseignant' else None,
                    niveau_acces=niveau_acces if type_user == 'enseignant' else 'standard'
                )
            else:
                user = Utilisateur.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=prenom,
                    last_name=nom,
                    type_utilisateur=type_user,
                    classe=classe if type_user == 'etudiant' else None,
                    matieres=matieres if type_user == 'enseignant' else None,
                    niveau_acces=niveau_acces if type_user == 'enseignant' else 'standard'
                )
            
            self.stdout.write(self.style.SUCCESS(f'\n✓ Utilisateur "{user.username}" créé avec succès !'))
            self.stdout.write(f'  - ID: {user.id}')
            self.stdout.write(f'  - Email: {user.email}')
            self.stdout.write(f'  - Type: {user.get_type_utilisateur_display()}')
            if user.classe:
                self.stdout.write(f'  - Classe: {user.classe}')
            if user.is_superuser:
                self.stdout.write(f'  - Superutilisateur: Oui')
            
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f'Erreur de validation: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de la création: {e}'))

