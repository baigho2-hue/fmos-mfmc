# apps/utilisateurs/management/commands/recuperer_code_verification.py
"""
Commande pour récupérer le dernier code de vérification d'un utilisateur
Usage: python manage.py recuperer_code_verification --username etudiant1
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.utilisateurs.models import Utilisateur, CodeVerification


class Command(BaseCommand):
    help = 'Recupere le dernier code de verification d\'un utilisateur'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Nom d\'utilisateur',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Adresse email',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        
        if not username and not email:
            self.stdout.write(self.style.ERROR('Vous devez fournir --username ou --email'))
            return
        
        try:
            if username:
                user = Utilisateur.objects.get(username=username)
            else:
                user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Utilisateur non trouve'))
            return
        
        # Récupérer le dernier code non utilisé
        code_verif = CodeVerification.objects.filter(
            user=user,
            utilise=False
        ).order_by('-cree_le').first()
        
        if not code_verif:
            self.stdout.write(self.style.WARNING(f'Aucun code de verification actif pour {user.username}'))
            return
        
        # Vérifier si le code est encore valide
        est_valide = code_verif.est_valide()
        
        self.stdout.write(self.style.SUCCESS(f'\n=== Code de verification pour {user.username} ==='))
        self.stdout.write(f'Email: {user.email}')
        self.stdout.write(f'Code: {code_verif.code}')
        self.stdout.write(f'Cree le: {code_verif.cree_le}')
        self.stdout.write(f'Expire le: {code_verif.expire_le}')
        self.stdout.write(f'Utilise: {code_verif.utilise}')
        self.stdout.write(f'Valide: {"OUI" if est_valide else "NON (expire)"}')
        
        if not est_valide:
            self.stdout.write(self.style.WARNING('\nLe code a expire. Vous devez en generer un nouveau.'))
        else:
            temps_restant = code_verif.expire_le - timezone.now()
            minutes_restantes = int(temps_restant.total_seconds() / 60)
            self.stdout.write(self.style.SUCCESS(f'\nTemps restant: {minutes_restantes} minutes'))

