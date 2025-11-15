# apps/utilisateurs/management/commands/liste_utilisateurs.py
"""
Commande pour lister les utilisateurs dans la base de données
Usage: python manage.py liste_utilisateurs [--email EMAIL]
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models import Utilisateur


class Command(BaseCommand):
    help = 'Liste les utilisateurs dans la base de données'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Rechercher un utilisateur par email',
        )

    def handle(self, *args, **options):
        email = options.get('email')
        
        if email:
            self.stdout.write(self.style.SUCCESS(f'=== Recherche de l\'utilisateur avec l\'email : {email} ===\n'))
            try:
                user = Utilisateur.objects.get(email=email)
                self.stdout.write(self.style.SUCCESS(f'Utilisateur trouve :'))
                self.stdout.write(f'  - Username: {user.username}')
                self.stdout.write(f'  - Email: {user.email}')
                self.stdout.write(f'  - Type: {user.get_type_utilisateur_display()}')
                self.stdout.write(f'  - Classe: {user.classe or "N/A"}')
                self.stdout.write(f'  - Date de creation: {user.date_joined}')
                self.stdout.write(f'  - Email verifie: {user.email_verifie}')
                self.stdout.write(f'  - Actif: {user.is_active}')
            except Utilisateur.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Aucun utilisateur trouve avec l\'email : {email}'))
            except Utilisateur.MultipleObjectsReturned:
                users = Utilisateur.objects.filter(email=email)
                self.stdout.write(self.style.WARNING(f'Plusieurs utilisateurs trouves avec l\'email : {email}'))
                for user in users:
                    self.stdout.write(f'  - {user.username} (ID: {user.id}, cree le: {user.date_joined})')
        else:
            self.stdout.write(self.style.SUCCESS('=== Liste des utilisateurs ===\n'))
            users = Utilisateur.objects.all().order_by('date_joined')
            self.stdout.write(f'Total: {users.count()} utilisateur(s)\n')
            
            for user in users:
                self.stdout.write(f'{user.username} ({user.email}) - {user.get_type_utilisateur_display()} - Cree le: {user.date_joined}')

