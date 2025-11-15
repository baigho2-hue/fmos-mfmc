# apps/utilisateurs/management/commands/migrate_med6_existants.py
"""
Commande pour migrer les étudiants Med 6 existants vers une liste par défaut
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Migre les étudiants Med 6 existants vers une liste par défaut'

    def add_arguments(self, parser):
        parser.add_argument(
            '--annee',
            type=str,
            default='2024-2025',
            help='Année universitaire pour la liste par défaut'
        )
        parser.add_argument(
            '--date-cloture',
            type=str,
            help='Date de clôture (format: YYYY-MM-DD). Par défaut: 31 juillet 2025'
        )

    def handle(self, *args, **options):
        annee = options.get('annee', '2024-2025')
        date_cloture_str = options.get('date_cloture')
        
        # Compter les étudiants sans liste
        etudiants_sans_liste = EtudiantMed6.objects.filter(liste__isnull=True).count()
        
        if etudiants_sans_liste == 0:
            self.stdout.write(
                self.style.SUCCESS('Aucun étudiant sans liste à migrer.')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'{etudiants_sans_liste} étudiants sans liste trouvés.')
        )
        
        # Déterminer la date de clôture
        if date_cloture_str:
            try:
                date_cloture = datetime.strptime(date_cloture_str, '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(
                    self.style.ERROR('Format de date invalide. Utilisez YYYY-MM-DD')
                )
                return
        else:
            # Par défaut: 31 juillet de l'année suivante
            annee_suivante = int(annee.split('-')[1])
            date_cloture = datetime(annee_suivante, 7, 31).date()
        
        # Créer ou récupérer la liste par défaut
        liste, created = ListeMed6.objects.get_or_create(
            annee_universitaire=annee,
            defaults={
                'date_cloture': date_cloture,
                'fichier_source': 'Migration données existantes',
                'active': True,
                'nombre_etudiants': 0
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Liste {annee} créée avec date de clôture: {date_cloture}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Liste {annee} existante trouvée.')
            )
        
        # Migrer les étudiants
        etudiants_migres = EtudiantMed6.objects.filter(liste__isnull=True).update(liste=liste)
        
        # Mettre à jour le nombre d'étudiants
        liste.nombre_etudiants = EtudiantMed6.objects.filter(liste=liste).count()
        liste.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'{etudiants_migres} étudiants migrés vers la liste {annee}.')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total étudiants dans la liste: {liste.nombre_etudiants}')
        )

