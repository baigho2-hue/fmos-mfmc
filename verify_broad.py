from django.db import models
from apps.utilisateurs.models import Utilisateur

with open('verify_result_broad.txt', 'w', encoding='utf-8') as f:
    f.write("=== Recherche élargie ===\n")
    
    # Tous les étudiants
    all_students = Utilisateur.objects.filter(type_utilisateur='etudiant')
    f.write(f"Total étudiants: {all_students.count()}\n")
    
    for s in all_students:
        f.write(f"- [{s.username}] {s.last_name} {s.first_name} | Classe: '{s.classe}' | Actif: {s.is_active}\n")
        
    # Recherche de "6" n'importe où
    f.write("\n=== Recherche de '6' ===\n")
    students_6 = Utilisateur.objects.filter(
        models.Q(classe__icontains='6') | 
        models.Q(username__icontains='6')
    )
    for s in students_6:
        f.write(f"- [{s.username}] {s.last_name} {s.first_name} | Classe: '{s.classe}'\n")
