from apps.utilisateurs.models_formation import ProgressionEtudiant
from apps.utilisateurs.models import Utilisateur

# Compter les progressions pour les étudiants Med6
etudiants_med6 = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
count = ProgressionEtudiant.objects.filter(etudiant__in=etudiants_med6).count()
print(f"Progressions existantes pour Med6: {count}")
print(f"Attendu: {etudiants_med6.count() * 2} (étudiants × 2 cours)")
