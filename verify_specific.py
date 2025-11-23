from apps.utilisateurs.models import Utilisateur

matricule = "ML20181242752ML"
try:
    u = Utilisateur.objects.get(username=matricule)
    print(f"User found: {u.username}")
    print(f"Name: {u.last_name} {u.first_name}")
    print(f"Class: '{u.classe}'")
    print(f"Active: {u.is_active}")
except Utilisateur.DoesNotExist:
    print(f"User {matricule} not found.")
except Exception as e:
    print(f"Error: {e}")
