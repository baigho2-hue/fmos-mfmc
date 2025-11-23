from apps.utilisateurs.models import Utilisateur

count = Utilisateur.objects.filter(classe="Médecine 6").count()
print(f"Students in 'Médecine 6': {count}")
