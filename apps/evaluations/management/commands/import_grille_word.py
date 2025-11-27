"""
Commande pour importer une grille d'évaluation depuis un document Word
Usage: python manage.py import_grille_word --file chemin/vers/fichier.docx --type-grille 1
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.evaluations.importers.import_word_grille import WordGrilleImporter
from apps.evaluations.models_grilles import TypeGrilleEvaluation


class Command(BaseCommand):
    help = "Importe une grille d'évaluation depuis un document Word (.docx)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            required=True,
            help='Chemin vers le fichier Word (.docx) à importer'
        )
        parser.add_argument(
            '--type-grille',
            type=int,
            required=True,
            help='ID du type de grille (voir TypeGrilleEvaluation)'
        )
        parser.add_argument(
            '--cours',
            type=int,
            help='ID du cours associé (optionnel)'
        )
        parser.add_argument(
            '--classe',
            type=int,
            help='ID de la classe associée (optionnel)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche les données parsées sans créer la grille'
        )

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = options['file']
        type_grille_id = options['type_grille']
        cours_id = options.get('cours')
        classe_id = options.get('classe')
        dry_run = options.get('dry_run', False)
        
        # Vérifier que le fichier existe
        import os
        if not os.path.exists(file_path):
            raise CommandError(f"Le fichier {file_path} n'existe pas.")
        
        if not file_path.endswith('.docx'):
            raise CommandError("Le fichier doit être au format .docx")
        
        # Vérifier le type de grille
        try:
            type_grille = TypeGrilleEvaluation.objects.get(pk=type_grille_id)
        except TypeGrilleEvaluation.DoesNotExist:
            raise CommandError(f"Type de grille {type_grille_id} introuvable.")
        
        self.stdout.write(self.style.SUCCESS(f'📄 Import du fichier : {file_path}'))
        self.stdout.write(f'📋 Type de grille : {type_grille.nom}')
        
        # Parser le document
        try:
            importer = WordGrilleImporter(file_path)
            grille_data = importer.parse_document()
            
            self.stdout.write('\n' + '=' * 70)
            self.stdout.write('DONNÉES PARSÉES')
            self.stdout.write('=' * 70)
            self.stdout.write(f'\nTitre : {grille_data.get("titre", "N/A")}')
            self.stdout.write(f'Description : {grille_data.get("description", "N/A")[:100]}...')
            self.stdout.write(f'\nNombre de critères : {len(grille_data.get("criteres", []))}')
            
            for critere in grille_data.get('criteres', []):
                self.stdout.write(f'\n  {critere["ordre"]}. {critere["libelle"]}')
                if critere.get('description'):
                    self.stdout.write(f'     Description : {critere["description"][:50]}...')
                self.stdout.write(f'     Éléments : {len(critere.get("elements", []))}')
                for elem in critere.get('elements', []):
                    self.stdout.write(f'       - {elem["libelle"][:60]}...')
            
            if dry_run:
                self.stdout.write(self.style.WARNING('\n⚠ Mode dry-run : aucune grille créée'))
                return
            
            # Créer la grille
            self.stdout.write('\n' + '=' * 70)
            self.stdout.write('CRÉATION DE LA GRILLE')
            self.stdout.write('=' * 70)
            
            grille = importer.create_grille(
                type_grille_id=type_grille_id,
                cours_id=cours_id,
                classe_id=classe_id,
                createur=None  # Peut être ajouté via request.user dans une vue
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✅ Grille créée avec succès !\n'
                    f'  - ID : {grille.id}\n'
                    f'  - Titre : {grille.titre}\n'
                    f'  - Critères : {grille.criteres.count()}\n'
                    f'  - Éléments totaux : {ElementEvaluation.objects.filter(critere__grille=grille).count()}'
                )
            )
            
        except Exception as e:
            raise CommandError(f"Erreur lors de l'import : {str(e)}") from e

