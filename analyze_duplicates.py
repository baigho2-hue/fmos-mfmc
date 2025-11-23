from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6
from apps.utilisateurs.models_formation import ProgressionEtudiant
import openpyxl

print("=== ANALYSE DES DOUBLONS ===\n")

# 1. Lire les matricules du fichier Excel (source de vérité)
file_path = r"c:\Users\HP\Documents\fmos-mfmc\Liste Med6 2024-2025.xlsx"
wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
sheet = wb.active

matricules_excel = set()
for row in sheet.iter_rows(min_row=3, values_only=True):
    if row[1]:
        matricules_excel.add(str(row[1]).strip())

print(f"1. Matricules dans Excel: {len(matricules_excel)}")

# 2. Trouver les EtudiantMed6 à garder et à supprimer
liste = ListeMed6.objects.filter(active=True).first()
if liste:
    etudiants_med6 = EtudiantMed6.objects.filter(liste=liste)
    print(f"\n2. EtudiantMed6 dans la liste:")
    print(f"   - Total: {etudiants_med6.count()}")
    
    # Garder uniquement ceux dans Excel
    a_garder = etudiants_med6.filter(matricule__in=matricules_excel)
    a_supprimer = etudiants_med6.exclude(matricule__in=matricules_excel)
    
    print(f"   - À garder: {a_garder.count()}")
    print(f"   - À supprimer: {a_supprimer.count()}")

# 3. Trouver les Utilisateurs à garder et à supprimer
users_med6 = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
print(f"\n3. Utilisateurs Med6:")
print(f"   - Total: {users_med6.count()}")

users_a_garder = users_med6.filter(username__in=matricules_excel)
users_a_supprimer = users_med6.exclude(username__in=matricules_excel)

print(f"   - À garder (matricule dans Excel): {users_a_garder.count()}")
print(f"   - À supprimer (matricule pas dans Excel): {users_a_supprimer.count()}")

# 4. Vérifier les progressions liées
if users_a_supprimer.exists():
    progressions_a_supprimer = ProgressionEtudiant.objects.filter(etudiant__in=users_a_supprimer)
    print(f"\n4. Progressions à supprimer: {progressions_a_supprimer.count()}")

print("\n=== PLAN DE NETTOYAGE ===")
print(f"1. Supprimer {a_supprimer.count()} EtudiantMed6 en trop")
print(f"2. Supprimer {users_a_supprimer.count()} Utilisateurs en trop")
print(f"3. Supprimer {progressions_a_supprimer.count()} Progressions liées")
print(f"\nRésultat attendu:")
print(f"  - EtudiantMed6: {a_garder.count()}")
print(f"  - Utilisateurs: {users_a_garder.count()}")
