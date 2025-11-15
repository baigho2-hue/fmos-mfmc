# apps/utilisateurs/management/commands/reinitialiser_utilisateurs.py
"""
Commande pour supprimer tous les utilisateurs et créer un nouveau superutilisateur
Usage: python manage.py reinitialiser_utilisateurs
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from apps.utilisateurs.models import Utilisateur, CodeVerification

User = get_user_model()


class Command(BaseCommand):
    help = 'Supprime tous les utilisateurs et permet de creer un nouveau superutilisateur'

    def add_arguments(self, parser):
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='Ne pas demander de confirmation',
        )

    def handle(self, *args, **options):
        noinput = options['noinput']
        
        # Compter les utilisateurs
        total_users = Utilisateur.objects.count()
        
        if total_users == 0:
            self.stdout.write(self.style.SUCCESS('Aucun utilisateur a supprimer.'))
        else:
            if not noinput:
                self.stdout.write(self.style.WARNING(
                    f'ATTENTION: Cette commande va supprimer TOUS les {total_users} utilisateur(s) de la base de donnees.'
                ))
                confirm = input('Etes-vous sur de vouloir continuer? (oui/non): ')
                if confirm.lower() not in ['oui', 'o', 'yes', 'y']:
                    self.stdout.write(self.style.ERROR('Operation annulee.'))
                    return
            
            self.stdout.write(self.style.WARNING(f'Suppression de {total_users} utilisateur(s)...'))
            
            # Supprimer tous les codes de vérification d'abord
            codes_count = CodeVerification.objects.count()
            if codes_count > 0:
                CodeVerification.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'  - {codes_count} code(s) de verification supprime(s)'))
            
            # Supprimer tous les utilisateurs
            Utilisateur.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'  - {total_users} utilisateur(s) supprime(s)'))
            
            self.stdout.write(self.style.SUCCESS('\nTous les utilisateurs ont ete supprimes avec succes.'))
        
        # Proposer de créer un superutilisateur
        self.stdout.write(self.style.SUCCESS('\n=== Creation d\'un nouveau superutilisateur ==='))
        self.stdout.write('Vous allez maintenant creer un nouveau superutilisateur.')
        
        # Utiliser la commande createsuperuser de Django
        try:
            call_command('createsuperuser', interactive=True)
            self.stdout.write(self.style.SUCCESS('\nSuperutilisateur cree avec succes!'))
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nCreation du superutilisateur annulee.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nErreur lors de la creation du superutilisateur: {e}'))

