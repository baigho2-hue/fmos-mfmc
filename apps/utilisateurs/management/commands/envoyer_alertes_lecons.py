# apps/utilisateurs/management/commands/envoyer_alertes_lecons.py
"""
Commande pour envoyer des alertes par email aux enseignants
- 1 semaine avant la dispensation d'une leçon
- 3 jours avant la dispensation d'une leçon
- Lors de la programmation d'une leçon
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Lecon, AlerteLecon


class Command(BaseCommand):
    help = 'Envoie des alertes par email aux enseignants pour les leçons programmées'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Affiche les alertes qui seraient envoyées sans les envoyer réellement',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        maintenant = timezone.now()
        
        # Date pour l'alerte 1 semaine avant
        date_semaine = maintenant + timedelta(days=7)
        # Date pour l'alerte 3 jours avant
        date_trois_jours = maintenant + timedelta(days=3)
        
        # Tolérance de ±1 jour pour les alertes
        tolerance = timedelta(days=1)
        
        alertes_envoyees = 0
        erreurs = []
        
        # Récupérer toutes les leçons actives avec une date de dispensation
        lecons = Lecon.objects.filter(
            actif=True,
            date_dispensation__isnull=False,
            date_dispensation__gte=maintenant  # Seulement les leçons futures
        ).select_related('cours', 'cours__enseignant', 'cours__classe')
        
        self.stdout.write(f"Vérification de {lecons.count()} leçon(s) programmée(s)...")
        
        for lecon in lecons:
            if not lecon.date_dispensation:
                continue
            
            enseignants = lecon.get_enseignants()
            
            if not enseignants:
                continue
            
            date_dispensation = lecon.date_dispensation
            
            # Vérifier si l'alerte "1 semaine avant" doit être envoyée
            if abs((date_dispensation - date_semaine).total_seconds()) < tolerance.total_seconds():
                for enseignant in enseignants:
                    if self._peut_envoyer_alerte(lecon, enseignant, 'semaine'):
                        if not dry_run:
                            if self._envoyer_alerte(lecon, enseignant, 'semaine', date_dispensation):
                                alertes_envoyees += 1
                            else:
                                erreurs.append(f"Erreur envoi alerte semaine - {lecon.titre} - {enseignant.email}")
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"[DRY-RUN] Alerte 1 semaine: {lecon.titre} -> {enseignant.email}"
                                )
                            )
                            alertes_envoyees += 1
            
            # Vérifier si l'alerte "3 jours avant" doit être envoyée
            if abs((date_dispensation - date_trois_jours).total_seconds()) < tolerance.total_seconds():
                for enseignant in enseignants:
                    if self._peut_envoyer_alerte(lecon, enseignant, 'trois_jours'):
                        if not dry_run:
                            if self._envoyer_alerte(lecon, enseignant, 'trois_jours', date_dispensation):
                                alertes_envoyees += 1
                            else:
                                erreurs.append(f"Erreur envoi alerte 3 jours - {lecon.titre} - {enseignant.email}")
                        else:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"[DRY-RUN] Alerte 3 jours: {lecon.titre} -> {enseignant.email}"
                                )
                            )
                            alertes_envoyees += 1
        
        # Résumé
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n[DRY-RUN] {alertes_envoyees} alerte(s) seraient envoyée(s)'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n{alertes_envoyees} alerte(s) envoyée(s) avec succès'
                )
            )
            if erreurs:
                self.stdout.write(
                    self.style.ERROR(
                        f'\n{len(erreurs)} erreur(s) lors de l\'envoi'
                    )
                )
                for erreur in erreurs:
                    self.stdout.write(self.style.ERROR(f"  - {erreur}"))
    
    def _peut_envoyer_alerte(self, lecon, enseignant, type_alerte):
        """Vérifie si l'alerte peut être envoyée (pas déjà envoyée)"""
        return not AlerteLecon.objects.filter(
            lecon=lecon,
            enseignant=enseignant,
            type_alerte=type_alerte
        ).exists()
    
    def _envoyer_alerte(self, lecon, enseignant, type_alerte, date_dispensation):
        """Envoie l'email d'alerte à l'enseignant"""
        try:
            # Déterminer le message selon le type d'alerte
            if type_alerte == 'semaine':
                jours_restants = "7 jours"
                sujet = f"📚 Rappel : Leçon programmée dans 7 jours - {lecon.titre}"
            elif type_alerte == 'trois_jours':
                jours_restants = "3 jours"
                sujet = f"📚 Rappel : Leçon programmée dans 3 jours - {lecon.titre}"
            else:
                jours_restants = "prochainement"
                sujet = f"📚 Nouvelle leçon programmée - {lecon.titre}"
            
            # Format de la date
            date_formatee = date_dispensation.strftime("%d/%m/%Y à %H:%M")
            
            message = f"""Bonjour {enseignant.get_full_name() or enseignant.username},

Vous avez une leçon programmée dans {jours_restants} :

📖 Leçon : {lecon.titre}
📚 Cours : {lecon.cours.titre}
🏫 Classe : {lecon.cours.classe.nom if hasattr(lecon.cours, 'classe') and lecon.cours.classe else 'N/A'}
📅 Date et heure : {date_formatee}
⏱️ Durée estimée : {lecon.duree_estimee} minutes
📝 Type : {lecon.get_type_lecon_display()}

Veuillez vous préparer en conséquence.

Cordialement,
L'équipe FMOS MFMC
"""
            
            # Envoyer l'email
            send_mail(
                sujet,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@fmos-mfmc.ml',
                [enseignant.email],
                fail_silently=False,
            )
            
            # Enregistrer l'alerte envoyée
            AlerteLecon.objects.create(
                lecon=lecon,
                enseignant=enseignant,
                type_alerte=type_alerte,
                envoye=True
            )
            
            # En mode développement, afficher aussi dans la console
            if settings.DEBUG:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Alerte {type_alerte} envoyée à {enseignant.email} pour {lecon.titre}"
                    )
                )
            
            return True
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"✗ Erreur lors de l'envoi à {enseignant.email}: {str(e)}"
                )
            )
            return False

