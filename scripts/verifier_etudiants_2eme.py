#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Vérification des étudiants en 2ème année."""
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
from apps.utilisateurs.models_programme_desmfmc import ResultatAnneeDES

emails = [
    'Simbocoulibaly500@gmail.com',
    'yayiagnid@yahoo.fr',
    'Drkebemahamadou@gamil.com',
    'Sangareami99@gmail.com',
    'Tim04diawara@gmail.com',
    'm.coumaré6@gmail.com',
    'baigho2@gmail.com',
]

print("=" * 70)
print("VÉRIFICATION DES ÉTUDIANTS EN 2ÈME ANNÉE")
print("=" * 70)

etudiants = Utilisateur.objects.filter(email__in=emails)
print(f"\nNombre d'étudiants trouvés: {etudiants.count()}\n")

for etudiant in etudiants:
    print(f"✅ {etudiant.get_full_name()}")
    print(f"   Email: {etudiant.email}")
    print(f"   Username: {etudiant.username}")
    print(f"   Classe: {etudiant.classe}")
    print(f"   Actif: {etudiant.is_active}")
    print(f"   Email vérifié: {etudiant.email_verifie}")
    
    # Vérifier le résultat année 1
    resultat = ResultatAnneeDES.objects.filter(etudiant=etudiant, annee=1).first()
    if resultat:
        print(f"   Résultat année 1: {resultat.decision} (cours: {resultat.cours_theoriques_valides}, stages: {resultat.stages_valides})")
    else:
        print(f"   ⚠️  Résultat année 1: NON TROUVÉ")
    print()

print("=" * 70)

