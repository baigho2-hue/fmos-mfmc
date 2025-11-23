from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant

print("=== CRÉATION PROGRESSIONS MANQUANTES (OPTIMISÉ) ===\n")

# Récupérer la classe et les cours
classe = Classe.objects.get(nom='Médecine 6')
cours_med6 = Cours.objects.filter(classe=classe, actif=True)
print(f"Cours actifs: {cours_med6.count()}")
for c in cours_med6:
    print(f"  - {c.titre}")

# Récupérer les étudiants Med6
etudiants_med6 = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
print(f"\nÉtudiants Med6: {etudiants_med6.count()}")

# Récupérer les progressions existantes
existing = set(
    ProgressionEtudiant.objects.filter(
        etudiant__in=etudiants_med6,
        cours__in=cours_med6
    ).values_list('etudiant_id', 'cours_id')
)
print(f"Progressions existantes: {len(existing)}")

# Créer les progressions manquantes
progressions_to_create = []
for etudiant in etudiants_med6:
    for cours in cours_med6:
        if (etudiant.id, cours.id) not in existing:
            progressions_to_create.append(
                ProgressionEtudiant(
                    etudiant=etudiant,
                    cours=cours,
                    statut='non_commence'
                )
            )

print(f"Progressions à créer: {len(progressions_to_create)}")

if progressions_to_create:
    # Créer par lots de 500
    batch_size = 500
    total = len(progressions_to_create)
    for i in range(0, total, batch_size):
        batch = progressions_to_create[i:i+batch_size]
        ProgressionEtudiant.objects.bulk_create(batch, batch_size=batch_size)
        print(f"  Créées: {min(i+batch_size, total)}/{total}")
    
    print(f"\n✓ Total créé: {len(progressions_to_create)}")
else:
    print("Toutes les progressions existent déjà")

# Vérification finale
total_progressions = ProgressionEtudiant.objects.filter(cours__in=cours_med6).count()
attendu = etudiants_med6.count() * cours_med6.count()

print(f"\n=== RÉSUMÉ ===")
print(f"Total progressions: {total_progressions}")
print(f"Attendu: {attendu}")
print(f"Statut: {'✓ OK' if total_progressions == attendu else '✗ INCOMPLET'}")
