"""
Commande Django pour envoyer les emails de confirmation d'admission
aux candidats acceptés pour les formations autres que DESMFMC.
"""
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from apps.admissions.models import DecisionAdmission, DossierCandidature


class Command(BaseCommand):
    help = 'Envoie les emails de confirmation aux candidats admis (formations autres que DESMFMC)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Renvoyer les emails même s\'ils ont déjà été envoyés',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Afficher ce qui serait envoyé sans réellement envoyer',
        )

    def handle(self, *args, **options):
        force = options['force']
        dry_run = options['dry_run']
        
        # Récupérer les décisions d'admission pour les formations autres que DESMFMC
        decisions = DecisionAdmission.objects.filter(
            decision='admis',
        ).exclude(
            dossier__formation__code='DESMFMC'
        ).select_related('dossier__candidat', 'dossier__formation')
        
        if not force:
            # Exclure ceux qui ont déjà reçu un email
            decisions = decisions.filter(email_confirmation_envoye=False)
        
        if not decisions.exists():
            self.stdout.write(
                self.style.WARNING('Aucune décision d\'admission à traiter.')
            )
            return
        
        self.stdout.write(f"Traitement de {decisions.count()} décision(s) d'admission...\n")
        
        envoyes = 0
        erreurs = 0
        
        for decision in decisions:
            candidat = decision.dossier.candidat
            formation = decision.dossier.formation
            
            if not candidat.email:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️  Pas d'email pour {candidat.username} - Dossier {decision.dossier.reference}"
                    )
                )
                erreurs += 1
                continue
            
            # Préparer l'email
            sujet = f"Confirmation d'admission - {formation.nom}"
            message = self._generer_message_confirmation(decision, candidat, formation)
            
            if dry_run:
                self.stdout.write(f"\n{'='*60}")
                self.stdout.write(f"DRY RUN - Email pour {candidat.email}")
                self.stdout.write(f"Sujet: {sujet}")
                self.stdout.write(f"Message:\n{message}")
                self.stdout.write(f"{'='*60}\n")
                envoyes += 1
            else:
                try:
                    send_mail(
                        sujet,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [candidat.email],
                        fail_silently=False,
                    )
                    
                    # Marquer comme envoyé
                    decision.email_confirmation_envoye = True
                    decision.date_envoi_email = timezone.now()
                    decision.save()
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ Email envoyé à {candidat.email} - Dossier {decision.dossier.reference}"
                        )
                    )
                    envoyes += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"❌ Erreur lors de l'envoi à {candidat.email}: {e}"
                        )
                    )
                    erreurs += 1
        
        self.stdout.write(f"\n{'='*60}")
        self.stdout.write(
            self.style.SUCCESS(f"✅ {envoyes} email(s) envoyé(s)")
        )
        if erreurs > 0:
            self.stdout.write(
                self.style.WARNING(f"⚠️  {erreurs} erreur(s)")
            )
    
    def _generer_message_confirmation(self, decision, candidat, formation):
        """Génère le message de confirmation d'admission."""
        nom_complet = candidat.get_full_name() or candidat.username
        
        message = f"""
Bonjour {nom_complet},

Nous avons le plaisir de vous informer que votre candidature pour la formation "{formation.nom}" a été acceptée.

Référence du dossier : {decision.dossier.reference}
Date de décision : {decision.date_decision.strftime('%d/%m/%Y')}

Prochaines étapes :
- Vous recevrez prochainement les informations concernant l'inscription administrative
- Veuillez vous assurer que tous les documents requis sont à jour

Si vous avez des questions, n'hésitez pas à nous contacter.

Cordialement,
L'équipe de la FMOS
"""
        return message.strip()

