# apps/utilisateurs/management/commands/parse_pdf_programme.py
"""
Commande pour parser le PDF du programme DESMFMC et créer la structure
Usage: python manage.py parse_pdf_programme "Programme DES de MF-MC.pdf"
"""
from django.core.management.base import BaseCommand
import os
import sys

class Command(BaseCommand):
    help = 'Parse le PDF du programme DESMFMC et crée la structure complète'

    def add_arguments(self, parser):
        parser.add_argument('pdf_path', type=str, help='Chemin vers le fichier PDF')

    def handle(self, *args, **options):
        pdf_path = options['pdf_path']
        
        if not os.path.exists(pdf_path):
            self.stdout.write(self.style.ERROR(f'Le fichier {pdf_path} n\'existe pas.'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Lecture du fichier PDF : {pdf_path}'))
        
        # Essayer d'extraire le texte du PDF
        try:
            # Essayer avec PyPDF2
            try:
                import PyPDF2
                with open(pdf_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ''
                    for page in reader.pages:
                        text += page.extract_text() + '\n'
            except ImportError:
                # Essayer avec pdfplumber
                try:
                    import pdfplumber
                    text = ''
                    with pdfplumber.open(pdf_path) as pdf:
                        for page in pdf.pages:
                            text += page.extract_text() + '\n'
                except ImportError:
                    # Essayer avec pypdf
                    try:
                        from pypdf import PdfReader
                        reader = PdfReader(pdf_path)
                        text = ''
                        for page in reader.pages:
                            text += page.extract_text() + '\n'
                    except ImportError:
                        self.stdout.write(self.style.ERROR(
                            'Aucune bibliothèque PDF trouvée. Installez PyPDF2, pdfplumber ou pypdf:\n'
                            'pip install PyPDF2\n'
                            'ou\n'
                            'pip install pdfplumber\n'
                            'ou\n'
                            'pip install pypdf'
                        ))
                        return
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de la lecture du PDF : {str(e)}'))
            return
        
        # Afficher un extrait du texte pour vérification
        self.stdout.write(self.style.SUCCESS(f'\nExtrait du PDF (premiers 2000 caractères) :\n'))
        self.stdout.write(text[:2000])
        
        # Sauvegarder le texte extrait dans un fichier pour analyse
        output_file = 'programme_desmfmc_extrait.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Texte extrait sauvegardé dans : {output_file}'))
        self.stdout.write(self.style.WARNING(
            '\n⚠️  Analysez le fichier texte et mettez à jour le script init_programme_desmfmc.py '
            'avec les informations exactes du programme.'
        ))

