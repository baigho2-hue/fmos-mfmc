from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import ProgressionEtudiant, Cours, Classe

# Compter les utilisateurs Med6
users = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
print(f"Utilisateurs Med6: {users.count()}")

# Compter les progressions
classe = Classe.objects.get(nom='Médecine 6')
cours = Cours.objects.filter(classe=classe, actif=True)
progressions = ProgressionEtudiant.objects.filter(cours__in=cours)
print(f"Cours actifs: {cours.count()}")
print(f"Progressions totales: {progressions.count()}")
print(f"Attendu: {users.count()} × {cours.count()} = {users.count() * cours.count()}")
