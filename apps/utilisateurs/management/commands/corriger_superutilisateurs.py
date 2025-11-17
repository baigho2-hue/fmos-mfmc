# apps/utilisateurs/management/commands/corriger_superutilisateurs.py
"""
Commande pour corriger les superutilisateurs existants
Définit type_utilisateur='enseignant' et niveau_acces='complet' pour tous les superutilisateurs
Usage: python manage.py corriger_superutilisateurs
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models import Utilisateur


class Command(BaseCommand):
    help = 'Corrige les superutilisateurs existants pour les definir comme enseignants avec acces complet'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default=None,
            help='Corriger uniquement cet utilisateur (par username)',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        
        if username:
            # Corriger un utilisateur spécifique
            try:
                user = Utilisateur.objects.get(username=username)
                if not user.is_superuser:
                    self.stdout.write(self.style.WARNING(
                        f'L\'utilisateur "{username}" n\'est pas un superutilisateur.'
                    ))
                    return
                
                user.type_utilisateur = 'enseignant'
                user.niveau_acces = 'complet'
                user.save()
                
                self.stdout.write(self.style.SUCCESS(
                    f'Superutilisateur "{username}" corrigé avec succès!\n'
                    f'  - Type: {user.get_type_utilisateur_display()}\n'
                    f'  - Niveau d\'accès: {user.get_niveau_acces_display()}'
                ))
            except Utilisateur.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Utilisateur "{username}" introuvable.'))
        else:
            # Corriger tous les superutilisateurs
            superusers = Utilisateur.objects.filter(is_superuser=True)
            count = 0
            
            for user in superusers:
                if user.type_utilisateur != 'enseignant' or user.niveau_acces != 'complet':
                    user.type_utilisateur = 'enseignant'
                    user.niveau_acces = 'complet'
                    user.save()
                    count += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'✅ "{user.username}" corrigé (enseignant, accès complet)'
                    ))
                else:
                    self.stdout.write(
                        f'⏭️  "{user.username}" déjà correct'
                    )
            
            if count > 0:
                self.stdout.write(self.style.SUCCESS(
                    f'\n{count} superutilisateur(s) corrigé(s) avec succès!'
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    '\nTous les superutilisateurs sont déjà correctement configurés.'
                ))

