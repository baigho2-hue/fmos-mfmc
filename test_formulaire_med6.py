#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test interactif du formulaire Med6 avec simulation utilisateur"""
import os
import django
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.utilisateurs.forms_med6 import LoginMed6Form
from apps.utilisateurs.models_med6 import EtudiantMed6

print("=" * 70)
print("TEST INTERACTIF DU FORMULAIRE MED6")
print("=" * 70)

# Récupérer un étudiant de la liste
liste = EtudiantMed6.objects.filter(liste__active=True, actif=True).first().liste
etudiant = EtudiantMed6.objects.filter(liste=liste, actif=True).first()

print(f"\nEtudiant de test: {etudiant.nom_complet()}")
print(f"Donnees dans la DB:")
print(f"  - Matricule DB: {repr(etudiant.matricule)}")
print(f"  - Prenom DB: {repr(etudiant.prenom)}")
print(f"  - Nom DB: {repr(etudiant.nom)}")

print("\n" + "=" * 70)
print("SCENARIOS DE TEST")
print("=" * 70)

# Scénario 1: Utilisateur entre son VRAI matricule dans le champ matricule
print("\n[SCENARIO 1] Utilisateur entre son vrai matricule dans le champ 'matricule'")
print("  (Ce qu'un utilisateur normal ferait)")
vrai_matricule = etudiant.prenom  # Le vrai matricule est dans prenom DB
vrai_prenom = etudiant.matricule  # Le prénom est dans matricule DB (numéro simple)
vrai_nom = etudiant.nom

print(f"  Formulaire:")
print(f"    - Matricule: {repr(vrai_matricule)}")
print(f"    - Prenom: {repr(vrai_prenom)}")
print(f"    - Nom: {repr(vrai_nom)}")

form_data = {
    'matricule': vrai_matricule,
    'prenom': vrai_prenom,
    'nom': vrai_nom
}

form = LoginMed6Form(data=form_data)
if form.is_valid():
    print("  [OK] Formulaire valide!")
    print(f"  Etudiant trouve: {form.cleaned_data['etudiant']}")
else:
    print("  [ECHEC] Formulaire invalide")
    print(f"  Erreurs: {form.errors}")

# Scénario 2: Utilisateur entre les données comme elles sont dans la DB
print("\n[SCENARIO 2] Utilisateur entre les donnees comme dans la DB")
print("  (Cas improbable mais possible)")
form_data2 = {
    'matricule': etudiant.matricule,  # "1", "2", etc.
    'prenom': etudiant.prenom,  # Vrai matricule
    'nom': etudiant.nom
}

print(f"  Formulaire:")
print(f"    - Matricule: {repr(etudiant.matricule)}")
print(f"    - Prenom: {repr(etudiant.prenom)}")
print(f"    - Nom: {repr(etudiant.nom)}")

form2 = LoginMed6Form(data=form_data2)
if form2.is_valid():
    print("  [OK] Formulaire valide!")
    print(f"  Etudiant trouve: {form2.cleaned_data['etudiant']}")
else:
    print("  [ECHEC] Formulaire invalide")
    print(f"  Erreurs: {form2.errors}")

# Scénario 3: Test avec des données incorrectes
print("\n[SCENARIO 3] Test avec des donnees incorrectes")
form_data3 = {
    'matricule': 'INCORRECT',
    'prenom': 'INCORRECT',
    'nom': 'INCORRECT'
}

form3 = LoginMed6Form(data=form_data3)
if form3.is_valid():
    print("  [PROBLEME] Formulaire devrait etre invalide!")
else:
    print("  [OK] Formulaire correctement invalide")
    print(f"  Erreurs: {form3.non_field_errors()}")

print("\n" + "=" * 70)
print("RECOMMANDATIONS")
print("=" * 70)
print("\nPour qu'un utilisateur puisse se connecter, il doit entrer:")
print(f"  - Matricule: {repr(vrai_matricule)} (son vrai matricule)")
print(f"  - Prenom: {repr(vrai_prenom)} (le numero simple de la liste)")
print(f"  - Nom: {repr(vrai_nom)} (son nom de famille)")
print("\nOU")
print(f"  - Matricule: {repr(etudiant.matricule)} (le numero simple)")
print(f"  - Prenom: {repr(etudiant.prenom)} (son vrai matricule)")
print(f"  - Nom: {repr(etudiant.nom)} (son nom de famille)")
print("\nLes deux methodes devraient fonctionner grace a la logique d'inversion.")

