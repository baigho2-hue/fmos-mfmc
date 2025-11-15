# apps/utilisateurs/management/commands/creer_cours_med6.py
"""
Commande Django pour créer les cours et leçons de Médecine 6
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.utilisateurs.models_formation import Formation, Classe, Cours, Lecon


class Command(BaseCommand):
    help = 'Crée les cours et leçons pour la classe Médecine 6'

    def handle(self, *args, **options):
        # Chercher ou créer la classe Médecine 6
        classe_med6, created = Classe.objects.get_or_create(
            nom='Médecine 6',
            defaults={
                'formation': self.get_or_create_formation(),
                'code': 'MED6',
                'annee': 6,
                'description': 'Classe de 6ème année de médecine',
                'date_debut': timezone.now().date(),
                'date_fin': (timezone.now() + timedelta(days=365)).date(),
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Classe "{classe_med6.nom}" créée avec succès.'))
        else:
            self.stdout.write(self.style.WARNING(f'Classe "{classe_med6.nom}" existe déjà.'))
        
        # Créer le cours "Santé Communautaire" (20 heures)
        cours_sante_communautaire, created = Cours.objects.get_or_create(
            classe=classe_med6,
            code='MED6-SC',
            defaults={
                'titre': 'Santé Communautaire',
                'description': 'Cours de Santé Communautaire pour les étudiants de 6ème année de médecine',
                'contenu': 'Ce cours couvre les aspects fondamentaux de la santé communautaire, la mobilisation communautaire, le système de référence et d\'évacuation, et l\'organisation du système de santé au Mali.',
                'date_debut': timezone.now().date(),
                'date_fin': (timezone.now() + timedelta(days=180)).date(),
                'volume_horaire': 20,
                'ordre': 1,
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Cours "{cours_sante_communautaire.titre}" créé avec succès.'))
        else:
            self.stdout.write(self.style.WARNING(f'Cours "{cours_sante_communautaire.titre}" existe déjà.'))
        
        # Leçons pour Santé Communautaire
        lecons_sante_communautaire = [
            (1, 'Aperçu général sur la MF/MC'),
            (2, 'La Mobilisation Communautaire'),
            (3, 'Le Système de Référence évacuation'),
            (4, 'Fondemment de La Santé Communautaire'),
            (5, 'Diagnostic communauatire'),
            (6, 'Diagnostic Communautaire des troubles mentaux'),
            (7, 'Approche communautaire pour la mise en place d\'un CSCom'),
            (8, 'Organisation du Systéme de Santé Au Mali'),
            (9, 'La promotion de la Famille'),
            (10, 'Organisation de la Vaccination'),
            (11, 'Promotion de la Santé'),
        ]
        
        for numero, titre in lecons_sante_communautaire:
            lecon, created = Lecon.objects.get_or_create(
                cours=cours_sante_communautaire,
                numero=numero,
                defaults={
                    'titre': titre,
                    'type_lecon': 'lecon',
                    'contenu': f'Contenu de la leçon {numero}: {titre}',
                    'ordre': numero,
                    'duree_estimee': 0,  # Durée à définir selon le volume horaire
                    'actif': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [+] Leçon {numero}: "{titre}" créée.'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Leçon {numero}: "{titre}" existe déjà.'))
        
        # Créer le cours "Techniques de communications" (10 heures)
        cours_techniques_communication, created = Cours.objects.get_or_create(
            classe=classe_med6,
            code='MED6-TC',
            defaults={
                'titre': 'Techniques de communications',
                'description': 'Cours de Techniques de communications pour les étudiants de 6ème année de médecine',
                'contenu': 'Ce cours couvre les techniques de communication en santé, l\'entrevue en santé, les techniques d\'animation et l\'annonce d\'une mauvaise nouvelle.',
                'date_debut': timezone.now().date(),
                'date_fin': (timezone.now() + timedelta(days=180)).date(),
                'volume_horaire': 10,
                'ordre': 2,
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Cours "{cours_techniques_communication.titre}" créé avec succès.'))
        else:
            self.stdout.write(self.style.WARNING(f'Cours "{cours_techniques_communication.titre}" existe déjà.'))
        
        # Leçons pour Techniques de communications
        lecons_techniques_communication = [
            (1, 'Généralités'),
            (2, 'L\'entrevue en Santé'),
            (3, 'Technique d\'animation'),
            (4, 'L"annonce d\'une mauvaise Nouvelle'),
        ]
        
        for numero, titre in lecons_techniques_communication:
            lecon, created = Lecon.objects.get_or_create(
                cours=cours_techniques_communication,
                numero=numero,
                defaults={
                    'titre': titre,
                    'type_lecon': 'lecon',
                    'contenu': f'Contenu de la leçon {numero}: {titre}',
                    'ordre': numero,
                    'duree_estimee': 0,  # Durée à définir selon le volume horaire
                    'actif': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [+] Leçon {numero}: "{titre}" créée.'))
            else:
                self.stdout.write(self.style.WARNING(f'  - Leçon {numero}: "{titre}" existe déjà.'))
        
        self.stdout.write(self.style.SUCCESS('\n[OK] Création des cours et leçons de Médecine 6 terminée avec succès!'))
    
    def get_or_create_formation(self):
        """Récupère ou crée la formation pour Médecine 6"""
        formation, created = Formation.objects.get_or_create(
            code='MED6',
            defaults={
                'nom': 'Médecine 6ème année',
                'description': 'Formation de 6ème année de médecine',
                'type_formation': 'initiale',
                'nature': 'non_certifiante',
                'duree_annees': 1,
                'duree_heures': 30,  # 20 + 10 heures
                'objectifs_generaux': 'Renforcer les compétences des étudiants de 6ème année de médecine en santé communautaire et techniques de communication.',
                'competences_visées': 'Maîtrise des concepts de santé communautaire et des techniques de communication en santé.',
                'actif': True
            }
        )
        return formation

