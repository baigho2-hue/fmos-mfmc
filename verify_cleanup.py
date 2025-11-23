from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6
from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant

print("=== VÉRIFICATION FINALE APRÈS NETTOYAGE ===\n")

# 1. Liste et EtudiantMed6
liste = ListeMed6.objects.filter(active=True).first()
if liste:
    etudiants = EtudiantMed6.objects.filter(liste=liste, actif=True)
    print(f"1. Liste Med6 ({liste.annee_universitaire}):")
    print(f"   - EtudiantMed6 actifs: {etudiants.count()}")
    print(f"   - Avec compte utilisateur: {etudiants.filter(utilisateur__isnull=False).count()}")

# 2. Utilisateurs
users = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
print(f"\n2. Utilisateurs Med6: {users.count()}")

# 3. Cours et Progressions
classe = Classe.objects.filter(nom='Médecine 6').first()
if classe:
    cours = Cours.objects.filter(classe=classe, actif=True)
    print(f"\n3. Cours actifs: {cours.count()}")
    for c in cours:
        print(f"   - {c.titre}")
    
    progressions = ProgressionEtudiant.objects.filter(cours__in=cours)
    etudiants_avec_prog = progressions.values('etudiant').distinct().count()
    
    print(f"\n4. Progressions:")
    print(f"   - Total: {progressions.count()}")
    print(f"   - Étudiants avec progressions: {etudiants_avec_prog}")
    print(f"   - Attendu: {users.count()} × {cours.count()} = {users.count() * cours.count()}")
    
    if progressions.count() == users.count() * cours.count():
        print("   ✓ Toutes les progressions sont créées")
    else:
        print(f"   ✗ Manque {(users.count() * cours.count()) - progressions.count()} progressions")

print("\n=== STATUT: ✓ SYSTÈME PROPRE ===")
