"""
Commande globale pour seed toutes les années du DESMFMC (1, 2, 3, 4).

Cette commande exécute séquentiellement toutes les commandes de seed pour chaque année.
Usage: python manage.py seed_all_desmfmc
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction


class Command(BaseCommand):
    help = "Seed toutes les années du DESMFMC (1, 2, 3, 4) en une seule commande"

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip les années déjà seedées (non implémenté pour l\'instant)',
        )
        parser.add_argument(
            '--year',
            type=int,
            choices=[1, 2, 3, 4],
            help='Seed uniquement une année spécifique (1, 2, 3, ou 4)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('  SEED COMPLET DU PROGRAMME DESMFMC'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')

        years_to_seed = [options['year']] if options['year'] else [1, 2, 3, 4]
        
        total_jalons = 0
        total_cours = 0
        total_lecons = 0

        for year in years_to_seed:
            self.stdout.write(self.style.WARNING(f'\n📚 ANNÉE {year} - DES-A{year}'))
            self.stdout.write('-' * 70)
            
            try:
                # Exécuter la commande de seed pour l'année
                call_command(f'seed_des{year}_jalons', classe=f'DES-A{year}', verbosity=1)
                self.stdout.write(self.style.SUCCESS(f'✅ Année {year} seedée avec succès'))
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Erreur lors du seed de l\'année {year}: {str(e)}')
                )
                if not options.get('continue_on_error', False):
                    raise

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('  SEED TERMINÉ'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Toutes les années ont été seedées : {", ".join([f"Année {y}" for y in years_to_seed])}'
            )
        )

