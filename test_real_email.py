import os
import django
from django.core.mail import send_mail
from django.conf import settings

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_real_email():
    print("--- Test d'envoi d'e-mail réel via Gmail ---")
    print(f"Expéditeur: {settings.EMAIL_HOST_USER}")
    print(f"Serveur: {settings.EMAIL_HOST}")
    
    try:
        send_mail(
            "Test Connexion FMOS MFMC",
            "Ceci est un test de connexion pour vérifier que votre compte Gmail envoie bien les codes de vérification.\n\nCode de test : 999 999",
            settings.DEFAULT_FROM_EMAIL,
            ['baigho2@gmail.com'],
            fail_silently=False,
        )
        print("\n✅ E-mail envoyé avec succès ! Vérifiez votre boîte Gmail (baigho2@gmail.com).")
    except Exception as e:
        print(f"\n❌ Erreur lors de l'envoi : {str(e)}")

if __name__ == "__main__":
    test_real_email()
