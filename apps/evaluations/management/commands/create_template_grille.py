"""
Commande pour créer un modèle Word pour les grilles d'évaluation
Usage: python manage.py create_template_grille --output template_grille.docx
"""
from django.core.management.base import BaseCommand
from apps.evaluations.importers.import_word_grille import create_word_template
import os


class Command(BaseCommand):
    help = "Crée un modèle Word pour les grilles d'évaluation"

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='template_grille_evaluation.docx',
            help='Chemin de sortie pour le modèle (défaut: template_grille_evaluation.docx)'
        )

    def handle(self, *args, **options):
        output_path = options['output']
        
        # Créer le répertoire si nécessaire
        output_dir = os.path.dirname(output_path) if os.path.dirname(output_path) else '.'
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        try:
            create_word_template(output_path)
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Modèle créé avec succès : {output_path}\n'
                    f'Vous pouvez maintenant ouvrir ce fichier, le remplir et l\'importer.'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Erreur lors de la création du modèle : {str(e)}')
            )
            raise

