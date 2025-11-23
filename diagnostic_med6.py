#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script de diagnostic pour le problème de connexion Med6"""
import os
import django
import sys

# Configurer l'encodage pour Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6

print("=" * 70)
print("DIAGNOSTIC MED6 - Vérification de la base de données")
print("=" * 70)

# 1. Vérifier les listes actives
print("\n1. LISTES ACTIVES:")
listes_actives = ListeMed6.objects.filter(active=True)
if listes_actives.exists():
    for liste in listes_actives:
        print(f"   [OK] Liste active trouvee: {liste}")
        print(f"     - Année: {liste.annee_universitaire}")
        print(f"     - Date clôture: {liste.date_cloture}")
        print(f"     - Expirée: {liste.est_expiree()}")
        print(f"     - Active: {liste.active}")
        
        # Compter les étudiants actifs
        etudiants_actifs = EtudiantMed6.objects.filter(liste=liste, actif=True)
        print(f"     - Étudiants actifs: {etudiants_actifs.count()}")
        
        # Afficher quelques exemples
        print(f"\n   Exemples d'étudiants dans cette liste:")
        for etudiant in etudiants_actifs[:5]:
            print(f"     - Matricule DB: {repr(etudiant.matricule)}")
            print(f"       Prenom DB: {repr(etudiant.prenom)}")
            print(f"       Nom DB: {repr(etudiant.nom)}")
            print(f"       Actif: {etudiant.actif}")
            print(f"       Utilisateur lié: {etudiant.utilisateur is not None}")
            print()
else:
    print("   [ERREUR] AUCUNE liste active trouvee!")

# 2. Vérifier la méthode get_etudiant_actif
print("\n2. TEST DE LA MÉTHODE get_etudiant_actif:")
liste = listes_actives.first()
if liste:
    etudiants = EtudiantMed6.objects.filter(liste=liste, actif=True)[:3]
    for etudiant in etudiants:
        print(f"\n   Test avec: {etudiant.nom_complet()}")
        print(f"   Données DB:")
        print(f"     - matricule: {repr(etudiant.matricule)}")
        print(f"     - prenom: {repr(etudiant.prenom)}")
        print(f"     - nom: {repr(etudiant.nom)}")
        
        # Test avec les valeurs exactes de la DB
        result1 = EtudiantMed6.get_etudiant_actif(
            etudiant.matricule,
            etudiant.prenom,
            etudiant.nom
        )
        print(f"   Test 1 (exact DB): {result1 is not None}")
        
        # Test avec les valeurs inversées (cas où l'utilisateur entre matricule dans prenom)
        result2 = EtudiantMed6.get_etudiant_actif(
            etudiant.prenom,  # Inversé
            etudiant.matricule,  # Inversé
            etudiant.nom
        )
        print(f"   Test 2 (inversé): {result2 is not None}")
        
        # Test avec verifier_identite
        verif1 = etudiant.verifier_identite(etudiant.matricule, etudiant.prenom, etudiant.nom)
        verif2 = etudiant.verifier_identite(etudiant.prenom, etudiant.matricule, etudiant.nom)
        print(f"   verifier_identite (exact): {verif1}")
        print(f"   verifier_identite (inversé): {verif2}")

# 3. Statistiques générales
print("\n3. STATISTIQUES:")
total_etudiants = EtudiantMed6.objects.count()
etudiants_actifs = EtudiantMed6.objects.filter(actif=True).count()
etudiants_avec_utilisateur = EtudiantMed6.objects.filter(actif=True, utilisateur__isnull=False).count()

print(f"   Total étudiants Med6: {total_etudiants}")
print(f"   Étudiants actifs: {etudiants_actifs}")
print(f"   Étudiants avec compte utilisateur: {etudiants_avec_utilisateur}")

# 4. Vérifier les listes inactives
print("\n4. LISTES INACTIVES:")
listes_inactives = ListeMed6.objects.filter(active=False)
if listes_inactives.exists():
    print(f"   {listes_inactives.count()} liste(s) inactive(s) trouvée(s)")
    for liste in listes_inactives[:3]:
        etudiants = EtudiantMed6.objects.filter(liste=liste, actif=True).count()
        print(f"     - {liste} ({liste.annee_universitaire}): {etudiants} étudiants actifs")
else:
    print("   Aucune liste inactive")

print("\n" + "=" * 70)
print("FIN DU DIAGNOSTIC")
print("=" * 70)

