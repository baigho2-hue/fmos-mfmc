#!/usr/bin/env python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
import django
django.setup()

from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6

print("=== LISTES MED6 ===")
listes = ListeMed6.objects.all()
for liste in listes:
    print(f"{liste.annee_universitaire}: Active={liste.active}, Étudiants={liste.etudiants.count()}")

print("\n=== ÉTUDIANTS ACTIFS AVEC LISTE ACTIVE ===")
etudiants = EtudiantMed6.objects.filter(actif=True, liste__active=True)[:10]
print(f"Total: {etudiants.count()}")

if etudiants.exists():
    for e in etudiants:
        print(f"\nMatricule: {e.matricule}")
        print(f"Nom: {e.nom}")
        print(f"Prénom: {e.prenom}")
        print(f"Liste: {e.liste.annee_universitaire if e.liste else 'AUCUNE'}")
        print(f"Utilisateur lié: {'OUI' if e.utilisateur else 'NON'}")
        break  # Ne montrer que le premier pour le test
else:
    print("❌ AUCUN ÉTUDIANT ACTIF AVEC LISTE ACTIVE!")
