from apps.utilisateurs.models_med6 import EtudiantMed6

count = EtudiantMed6.objects.count()
print(f"EtudiantMed6 count: {count}")
