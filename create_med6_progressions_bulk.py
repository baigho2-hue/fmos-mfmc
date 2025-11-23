from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant

# Récupérer la classe Médecine 6
classe_med6 = Classe.objects.get(nom='Médecine 6')
print(f"Classe: {classe_med6}")

# Récupérer les cours
cours_med6 = Cours.objects.filter(classe=classe_med6, actif=True)
print(f"Nombre de cours actifs: {cours_med6.count()}")

# Récupérer les étudiants Med6
etudiants_med6 = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
print(f"Nombre d'étudiants Med6: {etudiants_med6.count()}")

# Récupérer les progressions existantes
existing_progressions = set(
    ProgressionEtudiant.objects.filter(
        etudiant__in=etudiants_med6,
        cours__in=cours_med6
    ).values_list('etudiant_id', 'cours_id')
)
print(f"Progressions existantes: {len(existing_progressions)}")

# Créer les progressions manquantes en bulk
progressions_to_create = []
for etudiant in etudiants_med6:
    for cours in cours_med6:
        if (etudiant.id, cours.id) not in existing_progressions:
            progressions_to_create.append(
                ProgressionEtudiant(
                    etudiant=etudiant,
                    cours=cours,
                    statut='non_commence'
                )
            )

if progressions_to_create:
    ProgressionEtudiant.objects.bulk_create(progressions_to_create, batch_size=100)
    print(f"Progressions créées: {len(progressions_to_create)}")
else:
    print("Toutes les progressions existent déjà")

# Vérification finale
total = ProgressionEtudiant.objects.filter(etudiant__in=etudiants_med6, cours__in=cours_med6).count()
print(f"Total progressions: {total}")
