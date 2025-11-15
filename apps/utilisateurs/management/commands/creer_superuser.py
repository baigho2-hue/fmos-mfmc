# apps/utilisateurs/management/commands/creer_superuser.py
"""
Commande pour créer un superutilisateur avec des paramètres
Usage: python manage.py creer_superuser --username admin --email admin@example.com --password motdepasse
"""
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from apps.utilisateurs.models import Utilisateur


class Command(BaseCommand):
    help = 'Cree un superutilisateur avec des parametres en ligne de commande'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            required=True,
            help='Nom d\'utilisateur',
        )
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Adresse email',
        )
        parser.add_argument(
            '--password',
            type=str,
            required=True,
            help='Mot de passe',
        )
        parser.add_argument(
            '--first-name',
            type=str,
            default='',
            help='Prenom',
        )
        parser.add_argument(
            '--last-name',
            type=str,
            default='',
            help='Nom',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        first_name = options['first_name']
        last_name = options['last_name']
        
        # Vérifier si l'utilisateur existe déjà
        if Utilisateur.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'L\'utilisateur "{username}" existe deja.'))
            return
        
        if Utilisateur.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'L\'email "{email}" est deja utilise.'))
            return
        
        try:
            # Créer le superutilisateur
            user = Utilisateur.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                is_superuser=True,
                is_active=True,
                email_verifie=True  # Superutilisateur = email vérifié
            )
            
            self.stdout.write(self.style.SUCCESS(
                f'Superutilisateur "{username}" cree avec succes!\n'
                f'  - Username: {user.username}\n'
                f'  - Email: {user.email}\n'
                f'  - Superuser: {user.is_superuser}\n'
                f'  - Staff: {user.is_staff}'
            ))
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f'Erreur de validation: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de la creation: {e}'))

