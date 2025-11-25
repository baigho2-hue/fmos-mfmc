#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Envoie un email de rappel de connexion aux étudiants DESMFMC.
Usage :
    python scripts/envoyer_email_connexion_des.py
"""
import os
import sys
from django.core.mail import get_connection, EmailMessage
from email.utils import make_msgid

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django  # noqa: E402
django.setup()

from django.conf import settings  # noqa: E402
from apps.utilisateurs.models import Utilisateur  # noqa: E402

RECIPIENT_EMAILS = [
    'm.coumaré6@gmail.com',
    'boubacarc8@gmail.com',
]

def main():
    utilisateurs = Utilisateur.objects.filter(email__in=RECIPIENT_EMAILS)

    if not utilisateurs.exists():
        print("❌ Aucun utilisateur n'a été trouvé avec ces emails.")
        return

    sujet = "FMOS MFMC – Accès à votre compte étudiant DESMFMC"
    connection = get_connection(fail_silently=False)
    for user in utilisateurs:
        message = (
            f"Bonjour {user.first_name or 'Étudiant'},\n\n"
            "Votre compte FMOS MFMC est prêt. Vous pouvez vous connecter sur la plateforme :\n"
            "https://fmos-mfmc.onrender.com\n\n"
            f"Identifiant : {user.email}\n"
            "Mot de passe initial : etudiant123\n\n"
            "➡️ Merci de changer votre mot de passe après connexion.\n"
            "En cas de difficulté, contactez la coordination MFMC.\n\n"
            "Cordialement,\n"
            "Coordination DESMFMC – FMOS"
        )
        email = EmailMessage(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            connection=connection,
        )
        email.extra_headers = email.extra_headers or {}
        email.extra_headers['Message-ID'] = make_msgid(domain='localhost.localdomain')
        email.send(fail_silently=False)
        print(f"✅ Email envoyé à {user.get_full_name()} ({user.email}).")

if __name__ == "__main__":
    main()

