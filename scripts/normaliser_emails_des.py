#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Normalise les emails/usernames des étudiants (minuscules)."""
import os
import sys

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from apps.utilisateurs.models import Utilisateur


def main():
    qs = Utilisateur.objects.filter(type_utilisateur='etudiant')
    updated = 0
    for user in qs:
        if not user.email:
            continue
        normalized = user.email.strip().lower()
        if user.email != normalized or user.username != normalized:
            user.email = normalized
            user.username = normalized
            user.save(update_fields=['email', 'username'])
            updated += 1
    print(f"✅ Emails normalisés pour {updated} comptes étudiants.")


if __name__ == "__main__":
    main()

