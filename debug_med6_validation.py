#!/usr/bin/env python
"""
Script simple pour vérifier pourquoi l'authentification Med6 échoue
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

import django
django.setup()

from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6

# Récupérer l'étudiant de test
etudiant = EtudiantMed6.objects.filter(matricule='ML2018124275').first()

if etudiant:
    print(f"Étudiant trouvé dans la base de données:")
    print(f"  Matricule: '{etudiant.matricule}'")
    print(f"  Nom: '{etudiant.nom}'")
    print(f"  Prénom: '{etudiant.prenom}'")
    print(f"  Actif: {etudiant.actif}")
    print(f"  Liste: {etudiant.liste}")
    
    if etudiant.liste:
        print(f"\nInformations de la liste:")
        print(f"  Année: {etudiant.liste.annee_universitaire}")
        print(f"  Active: {etudiant.liste.active}")
        print(f"  Date import: {etudiant.liste.date_import}")
    
    # Test de la méthode get_etudiant_actif avec les informations exactes
    print(f"\n=== Test de get_etudiant_actif avec les informations exactes ===")
    result = EtudiantMed6.get_etudiant_actif(
        etudiant.matricule,
        etudiant.prenom,
        etudiant.nom
    )
    print(f"Résultat: {result}")
    
    # Test avec les variantes possibles
    print(f"\n=== Test avec 'YOUSSOUFABACAR' ===")
    result2 = EtudiantMed6.get_etudiant_actif(
        'ML2018124275',
        'Abacar',
        'YOUSSOUFABACAR'
    )
    print(f"Résultat: {result2}")
    
    # Test en minuscule
    print(f"\n=== Test en minuscule ===")
    result3 = EtudiantMed6.get_etudiant_actif(
        'ML2018124275',
        'abacar',
        'youssoufabacar'
    )
    print(f"Résultat: {result3}")
    
    # Vérifier les listes actives
    print(f"\n=== Listes Med6 ===")
    listes = ListeMed6.objects.all()
    for liste in listes:
        print(f"  {liste.annee_universitaire}: Active={liste.active}, Étudiants={liste.etudiants.count()}")
    
else:
    print("❌ Étudiant ML2018124275 non trouvé dans la base de données")

# Afficher tous les étudiants actifs
print(f"\n=== Tous les étudiants actifs ===")
etudiants_actifs = EtudiantMed6.objects.filter(actif=True)[:5]
for e in etudiants_actifs:
    print(f"  {e.matricule} - {e.nom} {e.prenom} - Liste active: {e.liste.active if e.liste else 'NO LIST'}")
