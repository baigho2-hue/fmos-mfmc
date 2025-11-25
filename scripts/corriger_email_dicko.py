#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Corriger l'email d'Oumar Dicko."""
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

# Chercher Oumar Dicko
u = Utilisateur.objects.filter(
    first_name__icontains='Oumar',
    last_name__icontains='Dicko'
).first()

if u:
    print(f"✅ Étudiant trouvé: {u.get_full_name()}")
    print(f"   Email actuel: {u.email}")
    print(f"   Username actuel: {u.username}")
    
    u.email = 'oumardicko735@gmail.com'
    u.username = 'oumardicko735@gmail.com'
    u.save(update_fields=['email', 'username'])
    
    print(f"\n✅ Email corrigé:")
    print(f"   Nouvel email: {u.email}")
    print(f"   Nouveau username: {u.username}")
else:
    print("❌ Oumar Dicko non trouvé")

