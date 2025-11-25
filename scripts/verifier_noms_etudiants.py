#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Vérifier les noms des étudiants DESMFMC."""
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
from django.db.models import Q

etudiants = Utilisateur.objects.filter(
    type_utilisateur='etudiant'
).filter(
    Q(classe__icontains='2') | Q(classe__icontains='3') | Q(classe__icontains='4')
)

print("=" * 80)
print("VÉRIFICATION DES NOMS DES ÉTUDIANTS DESMFMC")
print("=" * 80)

for e in etudiants:
    nom_complet = e.get_full_name()
    print(f"\nUsername: {e.username}")
    print(f"  First name: {repr(e.first_name)}")
    print(f"  Last name: {repr(e.last_name)}")
    print(f"  get_full_name(): {repr(nom_complet)}")
    print(f"  Classe: {repr(e.classe)}")
    if not nom_complet:
        print(f"  ⚠️  PROBLÈME: Pas de nom complet disponible")

