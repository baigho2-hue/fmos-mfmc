from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant

# Récupérer la classe Médecine 6
classe_med6 = Classe.objects.get(nom='Médecine 6')
print(f"Classe: {classe_med6}")

# Récupérer les cours
cours_med6 = Cours.objects.filter(classe=classe_med6, actif=True)
print(f"Nombre de cours actifs: {cours_med6.count()}")
for c in cours_med6:
    print(f"  - {c.titre}")

# Récupérer les étudiants Med6
etudiants_med6 = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
print(f"\nNombre d'étudiants Med6: {etudiants_med6.count()}")

# Créer les progressions
count_created = 0
count_existing = 0

for etudiant in etudiants_med6:
    for cours in cours_med6:
        progression, created = ProgressionEtudiant.objects.get_or_create(
            etudiant=etudiant,
            cours=cours,
            defaults={'statut': 'non_commence'}
        )
        if created:
            count_created += 1
        else:
            count_existing += 1

print(f"\nProgressions créées: {count_created}")
print(f"Progressions existantes: {count_existing}")
print(f"Total: {count_created + count_existing}")
