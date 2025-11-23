from django.db import models
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import ProgressionEtudiant

with open('verify_result.txt', 'w', encoding='utf-8') as f:
    f.write("=== Recherche des étudiants de Médecine 6 ===\n")

    # 1. Chercher la classe exacte
    classes = Utilisateur.objects.filter(type_utilisateur='etudiant').values_list('classe', flat=True).distinct()
    f.write(f"Classes trouvées en base : {list(classes)}\n")

    # 2. Filtrer les étudiants
    students = Utilisateur.objects.filter(
        type_utilisateur='etudiant', 
        classe__icontains='6'
    ).filter(
        models.Q(classe__icontains='Med') | models.Q(classe__icontains='Méd')
    )

    if not students.exists():
        f.write("Aucun étudiant trouvé pour 'Médecine 6' (recherche large).\n")
        f.write("Exemple d'étudiants :\n")
        for s in Utilisateur.objects.filter(type_utilisateur='etudiant')[:10]:
            f.write(f"- {s.username} ({s.classe})\n")
    else:
        f.write(f"{students.count()} étudiants trouvés.\n")
        for student in students:
            f.write(f"\nÉtudiant : {student.last_name} {student.first_name}\n")
            f.write(f"Matricule (Username) : {student.username}\n")
            f.write(f"Classe : {student.classe}\n")
            
            # 3. Vérifier les cours
            progressions = ProgressionEtudiant.objects.filter(etudiant=student)
            if progressions.exists():
                f.write(f"  Accès aux cours ({progressions.count()}) :\n")
                for prog in progressions:
                    f.write(f"  - {prog.cours.titre} (Statut: {prog.get_statut_display()})\n")
            else:
                f.write("  Aucun cours associé.\n")
