from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6
from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant

print("=== CRÉATION COMPTES UTILISATEURS MANQUANTS ===\n")

# Récupérer la liste active
liste = ListeMed6.objects.filter(active=True).first()
if not liste:
    print("Aucune liste active trouvée!")
    exit(1)

# Récupérer les étudiants Med6 sans compte utilisateur
etudiants_sans_compte = EtudiantMed6.objects.filter(
    liste=liste,
    actif=True,
    utilisateur__isnull=True
)

print(f"Étudiants sans compte: {etudiants_sans_compte.count()}")

# Créer les comptes
count_created = 0
count_errors = 0

for etudiant in etudiants_sans_compte:
    try:
        # Créer l'utilisateur
        user = Utilisateur.objects.create_user(
            username=etudiant.matricule,
            email=f"{etudiant.matricule.lower()}@fmos.ml",
            password=etudiant.matricule,  # Mot de passe = matricule
            first_name=etudiant.prenom,
            last_name=etudiant.nom,
            type_utilisateur='etudiant',
            classe='Médecine 6',
            email_verifie=True,
            is_active=True
        )
        
        # Lier à EtudiantMed6
        etudiant.utilisateur = user
        etudiant.save()
        
        count_created += 1
        
        if count_created % 50 == 0:
            print(f"  Créés: {count_created}...")
            
    except Exception as e:
        count_errors += 1
        print(f"  Erreur {etudiant.matricule}: {e}")

print(f"\n✓ Comptes créés: {count_created}")
print(f"✗ Erreurs: {count_errors}")

# Créer les progressions pour les nouveaux utilisateurs
print("\n=== CRÉATION PROGRESSIONS ===")

classe = Classe.objects.get(nom='Médecine 6')
cours_med6 = Cours.objects.filter(classe=classe, actif=True)
nouveaux_utilisateurs = Utilisateur.objects.filter(
    etudiant_med6__liste=liste,
    etudiant_med6__actif=True
).exclude(
    progressions__cours__in=cours_med6
).distinct()

print(f"Utilisateurs sans progressions: {nouveaux_utilisateurs.count()}")

progressions_to_create = []
for user in nouveaux_utilisateurs:
    for cours in cours_med6:
        # Vérifier si la progression n'existe pas déjà
        if not ProgressionEtudiant.objects.filter(etudiant=user, cours=cours).exists():
            progressions_to_create.append(
                ProgressionEtudiant(
                    etudiant=user,
                    cours=cours,
                    statut='non_commence'
                )
            )

if progressions_to_create:
    ProgressionEtudiant.objects.bulk_create(progressions_to_create, batch_size=100)
    print(f"✓ Progressions créées: {len(progressions_to_create)}")
else:
    print("Toutes les progressions existent déjà")

# Vérification finale
total_users = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant').count()
total_progressions = ProgressionEtudiant.objects.filter(cours__in=cours_med6).count()

print(f"\n=== RÉSUMÉ FINAL ===")
print(f"Total utilisateurs Med6: {total_users}")
print(f"Total progressions: {total_progressions}")
print(f"Attendu: {total_users} × {cours_med6.count()} = {total_users * cours_med6.count()}")
