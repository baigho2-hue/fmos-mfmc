# apps/utilisateurs/management/commands/init_couts_formations.py
"""
Commande pour initialiser les coûts des formations
"""
from django.core.management.base import BaseCommand
from apps.utilisateurs.models_cout import CoutFormation


class Command(BaseCommand):
    help = 'Initialise les coûts des formations avec les valeurs par défaut'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initialisation des coûts des formations...'))
        
        # DESMFMC
        cout_desmfmc, created = CoutFormation.objects.get_or_create(
            formation_slug='desmfmc',
            defaults={
                'nom_formation': 'DESMFMC - Diplôme d\'Études Spécialisées en Médecine de Famille et Médecine Communautaire',
                'niveau': 'annuel',
                'cout_principal': 450000,
                'modalite_paiement': 'unique',
                'conditions_paiement': 'Paiement en une seule tranche avant le début de l\'évaluation finale.',
                'informations_supplementaires': '''• Accès aux épreuves pratiques : Si le paiement n'est pas effectué avant le début de l'évaluation finale, l'étudiant n'aura pas accès à la salle des épreuves pratiques, même s'il a validé ses stages.
• Validation des stages : La validation des stages pendant la formation est la condition obligatoire pour pouvoir passer les épreuves écrites.
• Inscription sans frais : L'étudiant peut être inscrit sans frais après validation du probatoire écrit et de l'entretien.''',
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('OK - Cout DESMFMC cree'))
        else:
            self.stdout.write(self.style.WARNING('ATTENTION - Cout DESMFMC existe deja'))
        
        # Sante Communautaire
        cout_sante, created = CoutFormation.objects.get_or_create(
            formation_slug='sante-communautaire',
            defaults={
                'nom_formation': 'Sante Communautaire',
                'niveau': 'unique',
                'cout_principal': 0,
                'cout_diu': 750000,
                'cout_licence': 1000000,
                'cout_master': 2000000,
                'modalite_paiement': 'unique',
                'conditions_paiement': 'Paiement en une seule tranche.',
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('OK - Cout Sante Communautaire cree'))
        else:
            self.stdout.write(self.style.WARNING('ATTENTION - Cout Sante Communautaire existe deja'))
        
        # Recherche
        cout_recherche, created = CoutFormation.objects.get_or_create(
            formation_slug='recherche',
            defaults={
                'nom_formation': 'Recherche (Formation complete)',
                'niveau': 'unique',
                'cout_principal': 750000,
                'modalite_paiement': 'tranches',
                'conditions_paiement': 'Paiement en deux tranches : avant le debut de la formation et au milieu de la formation.',
                'informations_supplementaires': 'Duree : 6 mois\n\nPrerequis :\n• Minimum un diplome de licence\n• Maitrise de l\'informatique de base (Word, Excel)',
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('OK - Cout Recherche cree'))
        else:
            self.stdout.write(self.style.WARNING('ATTENTION - Cout Recherche existe deja'))
        
        # Logiciels d'analyse
        cout_logiciels, created = CoutFormation.objects.get_or_create(
            formation_slug='logiciels-analyse',
            defaults={
                'nom_formation': 'Logiciels d\'analyse',
                'niveau': 'unique',
                'cout_principal': 350000,
                'modalite_paiement': 'unique',
                'conditions_paiement': '',
                'informations_supplementaires': 'Duree : 3 mois\n\nNiveau requis : Baccalaureat',
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('OK - Cout Logiciels d\'analyse cree'))
        else:
            self.stdout.write(self.style.WARNING('ATTENTION - Cout Logiciels d\'analyse existe deja'))
        
        # Echographie de premiere ligne
        cout_echographie, created = CoutFormation.objects.get_or_create(
            formation_slug='echographie-base',
            defaults={
                'nom_formation': 'Echographie de premiere ligne',
                'niveau': 'unique',
                'cout_principal': 500000,
                'modalite_paiement': 'unique',
                'conditions_paiement': '',
                'informations_supplementaires': 'Duree : 6 mois\n\nNiveau requis : Minimum Diplome de technicien superieur en Sante ou equivalent',
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('OK - Cout Echographie de premiere ligne cree'))
        else:
            self.stdout.write(self.style.WARNING('ATTENTION - Cout Echographie de premiere ligne existe deja'))
        
        # Pedagogie en Sante
        cout_pedagogie, created = CoutFormation.objects.get_or_create(
            formation_slug='pedagogie-sante',
            defaults={
                'nom_formation': 'Pedagogie en Sante',
                'niveau': 'annuel',
                'cout_principal': 900000,
                'modalite_paiement': 'unique',
                'conditions_paiement': '',
                'informations_supplementaires': 'Duree : 1 annee\n\nNiveau requis : Minimum Technicien Superieur de sante',
                'actif': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('OK - Cout Pedagogie en Sante cree'))
        else:
            self.stdout.write(self.style.WARNING('ATTENTION - Cout Pedagogie en Sante existe deja'))
        
        self.stdout.write(self.style.SUCCESS('\nInitialisation terminee !'))
        self.stdout.write(self.style.SUCCESS('Vous pouvez maintenant modifier les coûts dans l\'admin Django.'))

