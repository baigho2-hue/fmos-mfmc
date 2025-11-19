"""
Commande Django pour générer automatiquement les étudiants Med6
à partir de la liste active.
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models_med6 import ListeMed6
from apps.utilisateurs.services.med6_import import sync_etudiants_from_excel


class Command(BaseCommand):
    help = 'Génère automatiquement les étudiants Med6 à partir de la liste active'

    def add_arguments(self, parser):
        parser.add_argument(
            '--annee',
            type=str,
            help='Année universitaire de la liste à utiliser (ex: 2024-2025). Si non spécifié, utilise la liste active.',
        )

    def handle(self, *args, **options):
        annee = options.get('annee')
        
        # Récupérer la liste
        if annee:
            try:
                liste = ListeMed6.objects.get(annee_universitaire=annee)
            except ListeMed6.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Aucune liste trouvée pour l\'année {annee}')
                )
                return
        else:
            # Chercher la liste active
            listes_actives = ListeMed6.objects.filter(active=True)
            if not listes_actives.exists():
                self.stdout.write(
                    self.style.ERROR('Aucune liste active trouvée.')
                )
                self.stdout.write(
                    self.style.WARNING('Utilisez --annee pour spécifier une année, ou activez une liste dans l\'admin.')
                )
                return
            
            liste = listes_actives.first()
            if listes_actives.count() > 1:
                self.stdout.write(
                    self.style.WARNING(
                        f'Plusieurs listes actives trouvées. Utilisation de: {liste.annee_universitaire}'
                    )
                )

        if not liste.fichier_source:
            self.stdout.write(
                self.style.ERROR(
                    f'La liste {liste.annee_universitaire} n\'a pas de fichier source défini.'
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'Génération des étudiants pour: {liste.annee_universitaire}')
        )
        self.stdout.write(f'Fichier source: {liste.fichier_source}')

        try:
            result = sync_etudiants_from_excel(liste, liste.fichier_source)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nRésultat:\n'
                    f'  - {result["imported"]} étudiants importés\n'
                    f'  - {result["updated"]} étudiants mis à jour\n'
                    f'  - {result["errors"]} erreurs\n'
                    f'  - Total: {result["total"]} étudiants dans la liste'
                )
            )
            
            if result["errors"] > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f'\nAttention: {result["errors"]} erreurs ont été rencontrées. '
                        f'Vérifiez les logs pour plus de détails.'
                    )
                )

        except FileNotFoundError as e:
            self.stdout.write(
                self.style.ERROR(f'Fichier introuvable: {e}')
            )
        except ImportError as e:
            self.stdout.write(
                self.style.ERROR(f'Module manquant: {e}')
            )
        except Exception as e:  # pylint: disable=broad-except
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de la génération: {e}')
            )

