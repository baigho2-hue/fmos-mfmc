#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Vérifier pourquoi les étudiants ne s'affichent pas dans l'admin."""
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

# Liste des emails des étudiants DESMFMC
emails = [
    'simbocoulibaly500@gmail.com',
    'yayiagnid@yahoo.fr',
    'drkebemahamadou@gamil.com',
    'sangareami99@gmail.com',
    'tim04diawara@gmail.com',
    'm.coumare6@gmail.com',
    'baigho2@gmail.com',
    'boubacarc8@gmail.com',
    'marikan@yahoo.fr',
    'ouumardicko735@gmail.com',
    'mbare1032@gmail.com',
    'traoredrsoumaonofadie@gmail.com',
    'issoufoutoure92@gmail.com',
    'drcoulibaly601@gmail.com',
    'amadoust14@gmail.com',
    'nabiissakone@gmail.com',
    'mohamednarembasoumaoro@gmail.com',
    'maigaseydou579@gmail.com',
]

print("=" * 80)
print("VÉRIFICATION DES ÉTUDIANTS DESMFMC DANS LA BASE")
print("=" * 80)

trouves = 0
non_trouves = []

for email in emails:
    u = Utilisateur.objects.filter(email__iexact=email).first()
    if u:
        trouves += 1
        print(f"\n✅ {u.get_full_name()}")
        print(f"   Email: {u.email}")
        print(f"   Username: {u.username}")
        print(f"   Classe: {repr(u.classe)}")
        print(f"   Type: {u.type_utilisateur}")
        print(f"   Actif: {u.is_active}")
        print(f"   Email vérifié: {u.email_verifie}")
        print(f"   Staff: {u.is_staff}")
        print(f"   Superuser: {u.is_superuser}")
    else:
        non_trouves.append(email)
        print(f"\n❌ NON TROUVÉ: {email}")

print("\n" + "=" * 80)
print(f"RÉSUMÉ: {trouves} trouvés sur {len(emails)}")
if non_trouves:
    print(f"Non trouvés: {len(non_trouves)}")
    for email in non_trouves:
        print(f"  - {email}")

# Vérifier tous les étudiants DESMFMC
print("\n" + "=" * 80)
print("TOUS LES ÉTUDIANTS DESMFMC (par classe)")
print("=" * 80)

etudiants_des = Utilisateur.objects.filter(
    type_utilisateur='etudiant'
).exclude(
    classe__isnull=True
).exclude(
    classe=''
)

classes_des = {}
for etudiant in etudiants_des:
    classe = etudiant.classe or 'Non renseignée'
    if '2' in classe or '3' in classe or '4' in classe or '1ère' in classe or 'DESMFMC' in classe:
        if classe not in classes_des:
            classes_des[classe] = []
        classes_des[classe].append(etudiant)

for classe, etudiants in sorted(classes_des.items()):
    print(f"\n[{classe}] - {len(etudiants)} étudiants")
    for e in etudiants[:5]:  # Afficher les 5 premiers
        print(f"  - {e.get_full_name()} ({e.email})")

