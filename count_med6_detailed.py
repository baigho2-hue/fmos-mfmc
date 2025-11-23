from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6
from apps.utilisateurs.models_formation import ProgressionEtudiant, Cours, Classe

print("=== COMPTAGE DÉTAILLÉ MED6 ===\n")

# 1. EtudiantMed6 dans la liste
liste = ListeMed6.objects.filter(active=True).first()
if liste:
    etudiants_med6_model = EtudiantMed6.objects.filter(liste=liste, actif=True)
    print(f"1. EtudiantMed6 (liste {liste.annee_universitaire}):")
    print(f"   - Actifs: {etudiants_med6_model.count()}")
    print(f"   - Total dans liste: {EtudiantMed6.objects.filter(liste=liste).count()}")

# 2. Utilisateurs avec classe "Médecine 6"
utilisateurs_med6 = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
print(f"\n2. Utilisateurs (classe='Médecine 6'):")
print(f"   - Total: {utilisateurs_med6.count()}")
print(f"   - Actifs: {utilisateurs_med6.filter(is_active=True).count()}")

# 3. Utilisateurs liés à EtudiantMed6
utilisateurs_lies = Utilisateur.objects.filter(
    etudiant_med6__isnull=False,
    etudiant_med6__actif=True
).distinct()
print(f"\n3. Utilisateurs liés à EtudiantMed6:")
print(f"   - Total: {utilisateurs_lies.count()}")

# 4. EtudiantMed6 sans utilisateur
sans_utilisateur = EtudiantMed6.objects.filter(
    liste=liste,
    actif=True,
    utilisateur__isnull=True
).count() if liste else 0
print(f"\n4. EtudiantMed6 sans compte Utilisateur: {sans_utilisateur}")

# 5. Progressions
classe = Classe.objects.filter(nom='Médecine 6').first()
if classe:
    cours = Cours.objects.filter(classe=classe, actif=True)
    progressions = ProgressionEtudiant.objects.filter(cours__in=cours)
    print(f"\n5. Progressions:")
    print(f"   - Total: {progressions.count()}")
    print(f"   - Étudiants uniques: {progressions.values('etudiant').distinct().count()}")
    print(f"   - Attendu: {utilisateurs_med6.count()} × {cours.count()} = {utilisateurs_med6.count() * cours.count()}")

print("\n=== FIN COMPTAGE ===")
