# apps/utilisateurs/utils_2fa.py
"""
Utilitaires pour la double authentification (2FA)
"""
import random
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import Code2FA, Utilisateur


def generer_code_2fa(user, request=None):
    """
    Génère un code de double authentification à 6 chiffres et l'envoie par email
    """
    # Générer un code à 6 chiffres
    code = str(random.randint(100000, 999999))
    
    # Créer le code 2FA (expire dans 5 minutes)
    code_2fa = Code2FA.objects.create(
        user=user,
        code=code,
        expire_le=timezone.now() + timedelta(minutes=5),
        ip_address=request.META.get('REMOTE_ADDR') if request else None,
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:255] if request else ''
    )
    
    # Envoyer l'email
    sujet = "Code de double authentification (2FA) - FMOS MFMC"
    message = f"""
Bonjour {user.get_full_name() or user.username},

Vous avez demandé un code de double authentification pour accéder à une fonctionnalité sécurisée.

Votre code de vérification est :

{code}

Ce code est valide pendant 5 minutes.

Si vous n'avez pas demandé ce code, veuillez ignorer cet email et contacter l'administration.

Cordialement,
L'équipe FMOS MFMC
"""
    
    try:
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@fmos-mfmc.ml',
            [user.email],
            fail_silently=False,
        )
        
        # En mode développement, afficher aussi le code dans la console
        if settings.DEBUG:
            print(f"\n{'='*60}")
            print(f"CODE 2FA (MODE DEVELOPPEMENT)")
            print(f"{'='*60}")
            print(f"Utilisateur: {user.username} ({user.email})")
            print(f"Code 2FA: {code}")
            print(f"Valide jusqu'à: {code_2fa.expire_le}")
            print(f"{'='*60}\n")
        
        return code_2fa
    except Exception as e:
        # En cas d'erreur d'envoi, ne pas supprimer le code en mode développement
        if settings.DEBUG:
            print(f"\n{'='*60}")
            print(f"ERREUR ENVOI EMAIL 2FA - CODE DISPONIBLE (MODE DEVELOPPEMENT)")
            print(f"{'='*60}")
            print(f"Utilisateur: {user.username} ({user.email})")
            print(f"Code 2FA: {code}")
            print(f"Valide jusqu'à: {code_2fa.expire_le}")
            print(f"Erreur: {e}")
            print(f"{'='*60}\n")
            return code_2fa
        else:
            # En production, supprimer le code en cas d'erreur
            code_2fa.delete()
            raise e


def verifier_code_2fa(user, code_saisi):
    """
    Vérifie si le code 2FA saisi est valide pour l'utilisateur
    """
    try:
        code_2fa = Code2FA.objects.filter(
            user=user,
            code=code_saisi,
            utilise=False
        ).order_by('-cree_le').first()
        
        if code_2fa and code_2fa.est_valide():
            # Marquer le code comme utilisé
            code_2fa.utilise = True
            code_2fa.save()
            return True
        return False
    except Exception:
        return False


def verifier_2fa_requis(user):
    """
    Vérifie si l'utilisateur doit utiliser le 2FA pour accéder à certaines fonctionnalités
    """
    # Le 2FA est requis pour les superviseurs/CEC et la coordination
    return user.est_superviseur_cec() or user.est_membre_coordination()

