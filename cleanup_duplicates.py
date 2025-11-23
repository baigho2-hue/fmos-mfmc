from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6
from apps.utilisateurs.models_formation import ProgressionEtudiant
import openpyxl

print("=== NETTOYAGE DES DOUBLONS ===\n")

# 1. Lire les matricules du fichier Excel
file_path = r"c:\Users\HP\Documents\fmos-mfmc\Liste Med6 2024-2025.xlsx"
wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
sheet = wb.active

matricules_excel = set()
for row in sheet.iter_rows(min_row=3, values_only=True):
    if row[1]:
        matricules_excel.add(str(row[1]).strip())

print(f"Matricules de référence (Excel): {len(matricules_excel)}")

# 2. Supprimer les EtudiantMed6 en trop
liste = ListeMed6.objects.filter(active=True).first()
if liste:
    etudiants_a_supprimer = EtudiantMed6.objects.filter(liste=liste).exclude(matricule__in=matricules_excel)
    count_etud = etudiants_a_supprimer.count()
    if count_etud > 0:
        etudiants_a_supprimer.delete()
        print(f"✓ Supprimé {count_etud} EtudiantMed6 en trop")
    
    # Mettre à jour le compteur
    liste.nombre_etudiants = EtudiantMed6.objects.filter(liste=liste).count()
    liste.save()
    print(f"  EtudiantMed6 restants: {liste.nombre_etudiants}")

# 3. Supprimer les Utilisateurs en trop
users_a_supprimer = Utilisateur.objects.filter(
    classe='Médecine 6',
    type_utilisateur='etudiant'
).exclude(username__in=matricules_excel)

count_users = users_a_supprimer.count()
if count_users > 0:
    # Les progressions seront supprimées en cascade
    users_a_supprimer.delete()
    print(f"✓ Supprimé {count_users} Utilisateurs en trop (et leurs progressions)")

# 4. Vérification finale
users_restants = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
etudiants_restants = EtudiantMed6.objects.filter(liste=liste) if liste else EtudiantMed6.objects.none()

print(f"\n=== RÉSULTAT FINAL ===")
print(f"EtudiantMed6: {etudiants_restants.count()}")
print(f"Utilisateurs: {users_restants.count()}")
print(f"Attendu: {len(matricules_excel)}")

# Vérifier les progressions
from apps.utilisateurs.models_formation import Classe, Cours
classe = Classe.objects.filter(nom='Médecine 6').first()
if classe:
    cours = Cours.objects.filter(classe=classe, actif=True)
    progressions = ProgressionEtudiant.objects.filter(cours__in=cours)
    print(f"Progressions: {progressions.count()}")
    print(f"Attendu: {users_restants.count()} × {cours.count()} = {users_restants.count() * cours.count()}")

print("\n✓ Nettoyage terminé")
