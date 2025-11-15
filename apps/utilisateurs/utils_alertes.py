# apps/utilisateurs/utils_alertes.py
"""
Utilitaires pour envoyer des alertes par email aux enseignants
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from apps.utilisateurs.models_formation import Lecon, AlerteLecon


def envoyer_alerte_programmation_lecon(lecon):
    """
    Envoie une alerte par email à tous les enseignants responsables
    lorsqu'une leçon est programmée (date_dispensation définie)
    """
    if not lecon.date_dispensation:
        return False
    
    enseignants = lecon.get_enseignants()
    if not enseignants:
        return False
    
    date_dispensation = lecon.date_dispensation
    date_formatee = date_dispensation.strftime("%d/%m/%Y à %H:%M")
    
    alertes_envoyees = 0
    
    for enseignant in enseignants:
        # Vérifier si l'alerte n'a pas déjà été envoyée
        if AlerteLecon.objects.filter(
            lecon=lecon,
            enseignant=enseignant,
            type_alerte='programmee'
        ).exists():
            continue
        
        try:
            sujet = f"📚 Nouvelle leçon programmée - {lecon.titre}"
            
            message = f"""Bonjour {enseignant.get_full_name() or enseignant.username},

Une nouvelle leçon a été programmée pour vous :

📖 Leçon : {lecon.titre}
📚 Cours : {lecon.cours.titre}
🏫 Classe : {lecon.cours.classe.nom if hasattr(lecon.cours, 'classe') and lecon.cours.classe else 'N/A'}
📅 Date et heure : {date_formatee}
⏱️ Durée estimée : {lecon.duree_estimee} minutes
📝 Type : {lecon.get_type_lecon_display()}

Vous recevrez des rappels :
- 7 jours avant la dispensation
- 3 jours avant la dispensation

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
                type_alerte='programmee',
                envoye=True
            )
            
            alertes_envoyees += 1
            
            # En mode développement, afficher aussi dans la console
            if settings.DEBUG:
                print(f"\n{'='*60}")
                print(f"ALERTE PROGRAMMATION LEÇON (MODE DEVELOPPEMENT)")
                print(f"{'='*60}")
                print(f"Enseignant: {enseignant.get_full_name()} ({enseignant.email})")
                print(f"Leçon: {lecon.titre}")
                print(f"Date: {date_formatee}")
                print(f"{'='*60}\n")
        
        except Exception as e:
            if settings.DEBUG:
                print(f"\n{'='*60}")
                print(f"ERREUR ENVOI ALERTE PROGRAMMATION")
                print(f"{'='*60}")
                print(f"Enseignant: {enseignant.email}")
                print(f"Leçon: {lecon.titre}")
                print(f"Erreur: {e}")
                print(f"{'='*60}\n")
            continue
    
    return alertes_envoyees > 0

