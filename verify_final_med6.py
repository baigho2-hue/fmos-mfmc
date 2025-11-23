from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6
from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant

print("=== VÉRIFICATION FINALE MED6 ===\n")

# 1. Liste Med6
liste = ListeMed6.objects.filter(active=True).first()
print(f"1. Liste Med6 active: {liste}")
print(f"   - Année: {liste.annee_universitaire if liste else 'N/A'}")
print(f"   - Nombre d'étudiants: {liste.nombre_etudiants if liste else 0}")

# 2. EtudiantMed6
etudiants_med6_model = EtudiantMed6.objects.filter(liste=liste, actif=True).count() if liste else 0
print(f"\n2. EtudiantMed6 actifs: {etudiants_med6_model}")

# 3. Utilisateurs Med6
utilisateurs_med6 = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
print(f"\n3. Utilisateurs Med6: {utilisateurs_med6.count()}")

# 4. Classe Med6
classe = Classe.objects.filter(nom='Médecine 6').first()
print(f"\n4. Classe Med6: {classe}")

# 5. Cours Med6
if classe:
    cours = Cours.objects.filter(classe=classe, actif=True)
    print(f"\n5. Cours Med6 actifs: {cours.count()}")
    for c in cours:
        print(f"   - {c.titre} ({c.code})")
        
    # 6. Progressions
    progressions = ProgressionEtudiant.objects.filter(cours__in=cours)
    print(f"\n6. Progressions totales: {progressions.count()}")
    
    # Vérifier un étudiant spécifique
    if utilisateurs_med6.exists():
        etudiant_test = utilisateurs_med6.first()
        prog_etudiant = ProgressionEtudiant.objects.filter(etudiant=etudiant_test, cours__in=cours)
        print(f"\n7. Test étudiant: {etudiant_test.username}")
        print(f"   - Progressions: {prog_etudiant.count()}")
        for p in prog_etudiant:
            print(f"     • {p.cours.titre}: {p.statut}")

print("\n=== FIN VÉRIFICATION ===")
