#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
import django
django.setup()

from apps.utilisateurs.models_med6 import EtudiantMed6

# Test direct de la méthode
print("=== TEST DE get_etudiant_actif ===\n")

# D'abord, trouver l'étudiant dans la base
etudiant_db = EtudiantMed6.objects.filter(matricule='ML2018124275').first()
if etudiant_db:
    print("Étudiant trouvé dans la base:")
    print(f"  Matricule: '{etudiant_db.matricule}'")
    print(f"  Nom: '{etudiant_db.nom}'")
    print(f"  Prénom: '{etudiant_db.prenom}'")
    print(f"  Actif: {etudiant_db.actif}")
    if etudiant_db.liste:
        print(f"  Liste: {etudiant_db.liste.annee_universitaire} (Active={etudiant_db.liste.active})")
    else:
        print(f"  ❌ AUCUNE LISTE!")
    print()
    
    # Maintenant test de get_etudiant_actif
    print("Test 1: Avec les données exactes de la base")
    result = EtudiantMed6.get_etudiant_actif(
        matricule=etudiant_db.matricule,
        prenom=etudiant_db.prenom,
        nom=etudiant_db.nom
    )
    print(f"Résultat: {result}\n")
    
    print("Test 2: Avec ABOUBACAR et YOUSSOUFA")
    result2 = EtudiantMed6.get_etudiant_actif(
        matricule='ML2018124275',
        prenom='YOUSSOUFA',
        nom='ABOUBACAR'
    )
    print(f"Résultat: {result2}\n")
    
    print("Test 3: Vérification d'identité directe")
    match = etudiant_db.verifier_identite('ML2018124275', 'YOUSSOUFA', 'ABOUBACAR')
    print(f"verifier_identite: {match}\n")
    
else:
    print("❌ Étudiant ML2018124275 non trouvé!")
