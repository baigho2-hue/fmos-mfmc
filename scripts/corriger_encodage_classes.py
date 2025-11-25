#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour corriger l'encodage des classes DESMFMC dans la base de données.
"""
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

# Mapping des classes mal encodées vers les bonnes
corrections = {
    '2me A': '2ème A',
    '3me A': '3ème A',
    '4me A': '4ème A',
}

print("=" * 70)
print("CORRECTION DE L'ENCODAGE DES CLASSES DESMFMC")
print("=" * 70)

total_corriges = 0

for classe_incorrecte, classe_correcte in corrections.items():
    etudiants = Utilisateur.objects.filter(
        type_utilisateur='etudiant',
        classe=classe_incorrecte
    )
    
    count = etudiants.count()
    if count > 0:
        etudiants.update(classe=classe_correcte)
        print(f"✅ {count} étudiants mis à jour : '{classe_incorrecte}' → '{classe_correcte}'")
        total_corriges += count

print("\n" + "=" * 70)
print(f"Total corrigé : {total_corriges} étudiants")
print("=" * 70)

# Vérification
print("\nVérification finale :")
etudiants_des = Utilisateur.objects.filter(
    type_utilisateur='etudiant',
    classe__in=['2ème A', '3ème A', '4ème A']
)
print(f"✅ {etudiants_des.count()} étudiants DESMFMC trouvés avec les classes correctes")

