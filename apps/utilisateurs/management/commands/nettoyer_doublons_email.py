# apps/utilisateurs/management/commands/nettoyer_doublons_email.py
"""
Commande pour nettoyer les doublons d'email dans la base de données
Usage: python manage.py nettoyer_doublons_email
"""
from django.core.management.base import BaseCommand
from django.db.models import Count
from apps.utilisateurs.models import Utilisateur


class Command(BaseCommand):
    help = 'Nettoie les doublons d\'email dans la base de données'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche les doublons sans les modifier',
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Supprime les doublons (garde le premier)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        delete_mode = options['delete']
        
        self.stdout.write(self.style.SUCCESS('=== Recherche des doublons d\'email ===\n'))
        
        # Trouver les emails en double
        doublons = Utilisateur.objects.values('email').annotate(
            count=Count('email')
        ).filter(count__gt=1).order_by('-count')
        
        if not doublons.exists():
            self.stdout.write(self.style.SUCCESS('Aucun doublon d\'email trouve.'))
            return
        
        self.stdout.write(self.style.WARNING(f'Nombre d\'emails en double : {doublons.count()}\n'))
        
        total_supprimes = 0
        
        for doublon in doublons:
            email = doublon['email']
            count = doublon['count']
            
            if not email:  # Ignorer les emails vides
                continue
            
            self.stdout.write(self.style.WARNING(f'\nEmail en double : {email} ({count} occurrences)'))
            
            # Récupérer tous les utilisateurs avec cet email
            utilisateurs = Utilisateur.objects.filter(email=email).order_by('date_joined')
            
            # Garder le premier (le plus ancien)
            premier = utilisateurs.first()
            autres = utilisateurs.exclude(id=premier.id)
            
            self.stdout.write(f'  - Garde : {premier.username} (ID: {premier.id}, cree le: {premier.date_joined})')
            
            for autre in autres:
                self.stdout.write(f'  - A supprimer/modifier : {autre.username} (ID: {autre.id}, cree le: {autre.date_joined})')
                
                if delete_mode:
                    # Supprimer l'utilisateur en double
                    autre.delete()
                    total_supprimes += 1
                    self.stdout.write(self.style.SUCCESS(f'    [SUPPRIME] Utilisateur {autre.username} supprime'))
                elif not dry_run:
                    # Modifier l'email pour le rendre unique
                    nouveau_email = f"{autre.username}@duplicate.{email.split('@')[1] if '@' in email else 'local'}"
                    autre.email = nouveau_email
                    autre.save()
                    total_supprimes += 1
                    self.stdout.write(self.style.SUCCESS(f'    [MODIFIE] Email change en : {nouveau_email}'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING(
                f'\n=== MODE DRY-RUN ===\n'
                f'Aucune modification effectuee.\n'
                f'Utilisez --delete pour supprimer les doublons\n'
                f'ou sans --dry-run pour modifier les emails.'
            ))
        elif delete_mode:
            self.stdout.write(self.style.SUCCESS(
                f'\n=== Resume ===\n'
                f'Utilisateurs supprimes : {total_supprimes}'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'\n=== Resume ===\n'
                f'Emails modifies : {total_supprimes}'
            ))

