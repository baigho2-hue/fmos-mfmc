# apps/utilisateurs/management/commands/attribuer_classes_desmfmc.py
"""
Commande pour attribuer/réattribuer les classes DESMFMC aux étudiants
Usage: 
    python manage.py attribuer_classes_desmfmc                    # Attribue toutes les classes
    python manage.py attribuer_classes_desmfmc --annee 2           # Attribue uniquement l'année 2
    python manage.py attribuer_classes_desmfmc --username user1   # Attribue pour un étudiant spécifique
    python manage.py attribuer_classes_desmfmc --dry-run           # Affiche ce qui serait fait sans modifier
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Formation, Classe
from apps.utilisateurs.models_programme_desmfmc import ResultatAnneeDES


class Command(BaseCommand):
    help = 'Attribue ou réattribue les classes DESMFMC aux étudiants selon leur progression'

    def add_arguments(self, parser):
        parser.add_argument(
            '--annee',
            type=int,
            choices=[1, 2, 3, 4],
            help='Attribuer uniquement pour une année spécifique (1, 2, 3 ou 4)',
        )
        parser.add_argument(
            '--username',
            type=str,
            help='Attribuer uniquement pour un étudiant spécifique (username)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche ce qui serait fait sans modifier la base de données',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force la réattribution même si l\'étudiant a déjà une classe DESMFMC valide',
        )

    def handle(self, *args, **options):
        annee_filter = options.get('annee')
        username_filter = options.get('username')
        dry_run = options.get('dry_run', False)
        force = options.get('force', False)
        
        if dry_run:
            self.stdout.write(self.style.WARNING('=== MODE DRY-RUN : Aucune modification ne sera effectuée ===\n'))
        
        # Récupérer la formation DESMFMC
        try:
            formation = Formation.objects.get(code='DESMFMC')
        except Formation.DoesNotExist:
            self.stdout.write(self.style.ERROR('Erreur : La formation DESMFMC n\'existe pas.'))
            self.stdout.write('Exécutez d\'abord la migration pour créer la formation.')
            return
        
        # Récupérer les classes DESMFMC
        classes_map = {}
        for annee in [1, 2, 3, 4]:
            classe = Classe.objects.filter(
                formation=formation,
                annee=annee,
                actif=True
            ).first()
            if classe:
                classes_map[annee] = classe
            else:
                self.stdout.write(self.style.WARNING(f'Attention : La classe pour l\'année {annee} n\'existe pas.'))
        
        if not classes_map:
            self.stdout.write(self.style.ERROR('Erreur : Aucune classe DESMFMC trouvée.'))
            return
        
        # Filtrer les étudiants
        etudiants_query = Utilisateur.objects.filter(
            type_utilisateur='etudiant',
            is_active=True
        )
        
        if username_filter:
            etudiants_query = etudiants_query.filter(username=username_filter)
        
        etudiants = list(etudiants_query)
        
        if not etudiants:
            self.stdout.write(self.style.WARNING('Aucun étudiant trouvé avec les critères spécifiés.'))
            return
        
        # Statistiques
        stats = {
            'total': 0,
            'attribues': 0,
            'deja_attribues': 0,
            'non_desmfmc': 0,
            'erreurs': 0,
            'par_annee': {1: 0, 2: 0, 3: 0, 4: 0}
        }
        
        self.stdout.write(self.style.SUCCESS(f'=== Attribution des classes DESMFMC ===\n'))
        self.stdout.write(f'Nombre d\'étudiants à traiter : {len(etudiants)}\n')
        
        with transaction.atomic():
            for etudiant in etudiants:
                stats['total'] += 1
                
                try:
                    # Vérifier si l'étudiant est dans le DESMFMC
                    est_desmfmc = False
                    if etudiant.classe:
                        est_desmfmc = 'DESMFMC' in etudiant.classe or 'DES-A' in etudiant.classe
                    else:
                        est_desmfmc = ResultatAnneeDES.objects.filter(
                            etudiant=etudiant,
                            formation=formation
                        ).exists()
                    
                    # Ne traiter que les étudiants du DESMFMC ou ceux sans classe
                    if not est_desmfmc and etudiant.classe:
                        stats['non_desmfmc'] += 1
                        continue
                    
                    # Déterminer l'année de l'étudiant
                    annee_etudiant = self._determiner_annee_etudiant(etudiant, formation)
                    
                    # Filtrer par année si spécifié
                    if annee_filter and annee_etudiant != annee_filter:
                        continue
                    
                    # Vérifier si déjà attribué correctement
                    if not force and etudiant.classe:
                        classe_actuelle = None
                        for annee, classe in classes_map.items():
                            if classe.nom == etudiant.classe:
                                classe_actuelle = classe
                                break
                        
                        if classe_actuelle and classe_actuelle.annee == annee_etudiant:
                            stats['deja_attribues'] += 1
                            continue
                    
                    # Attribuer la classe
                    if annee_etudiant in classes_map:
                        classe_attribuee = classes_map[annee_etudiant]
                        ancienne_classe = etudiant.classe or '(aucune)'
                        
                        if not dry_run:
                            etudiant.classe = classe_attribuee.nom
                            etudiant.save()
                        
                        stats['attribues'] += 1
                        stats['par_annee'][annee_etudiant] += 1
                        
                        self.stdout.write(
                            f'[{"SIMULÉ" if dry_run else "OK"}] {etudiant.username}: '
                            f'{ancienne_classe} → {classe_attribuee.nom}'
                        )
                    else:
                        stats['erreurs'] += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f'[ERREUR] {etudiant.username}: Impossible de déterminer la classe '
                                f'(année calculée: {annee_etudiant})'
                            )
                        )
                
                except Exception as e:
                    stats['erreurs'] += 1
                    self.stdout.write(
                        self.style.ERROR(f'[ERREUR] {etudiant.username}: {str(e)}')
                    )
        
        # Afficher les statistiques
        self.stdout.write(self.style.SUCCESS('\n=== Statistiques ==='))
        self.stdout.write(f'Total d\'étudiants traités : {stats["total"]}')
        self.stdout.write(f'Classes attribuées : {stats["attribues"]}')
        self.stdout.write(f'Déjà attribués correctement : {stats["deja_attribues"]}')
        self.stdout.write(f'Non DESMFMC (ignorés) : {stats["non_desmfmc"]}')
        self.stdout.write(f'Erreurs : {stats["erreurs"]}')
        
        self.stdout.write('\n=== Répartition par année ===')
        for annee in [1, 2, 3, 4]:
            count = stats['par_annee'][annee]
            classe = classes_map.get(annee)
            classe_nom = classe.nom if classe else 'N/A'
            self.stdout.write(f'  Année {annee} ({classe_nom}) : {count} étudiant(s)')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n=== MODE DRY-RUN : Aucune modification effectuée ==='))
            self.stdout.write('Exécutez la commande sans --dry-run pour appliquer les modifications.')
        else:
            self.stdout.write(self.style.SUCCESS('\n[OK] Attribution des classes terminée !'))
    
    def _determiner_annee_etudiant(self, etudiant, formation):
        """Détermine l'année de l'étudiant basée sur ses résultats"""
        try:
            # Chercher le résultat le plus récent
            resultats = ResultatAnneeDES.objects.filter(
                etudiant=etudiant,
                formation=formation
            ).order_by('-annee')
            
            if resultats.exists():
                dernier_resultat = resultats.first()
                
                # Si l'étudiant a été admis en année N, il est maintenant en année N+1
                if dernier_resultat.decision == 'admis':
                    return dernier_resultat.annee + 1
                # Si l'étudiant est diplômé, il reste en année 4
                elif dernier_resultat.decision == 'diplome':
                    return 4
                # Si l'étudiant est en cours d'évaluation ou ajourné, il reste dans la même année
                else:
                    return dernier_resultat.annee
            else:
                # Si l'étudiant n'a pas de résultat mais a une classe DESMFMC, essayer de déterminer depuis la classe
                if etudiant.classe:
                    if 'Année 1' in etudiant.classe or 'DES-A1' in etudiant.classe:
                        return 1
                    elif 'Année 2' in etudiant.classe or 'DES-A2' in etudiant.classe:
                        return 2
                    elif 'Année 3' in etudiant.classe or 'DES-A3' in etudiant.classe:
                        return 3
                    elif 'Année 4' in etudiant.classe or 'DES-A4' in etudiant.classe:
                        return 4
                
                # Par défaut, année 1 pour les nouveaux étudiants
                return 1
        except Exception:
            # En cas d'erreur, mettre en année 1 par défaut
            return 1

