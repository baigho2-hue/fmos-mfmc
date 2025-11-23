from apps.utilisateurs.models_formation import Classe, Cours

# Vérifier si la classe Médecine 6 existe
classe_med6 = Classe.objects.filter(nom__icontains='Médecine 6').first()
print(f"Classe Médecine 6: {classe_med6}")

if classe_med6:
    # Vérifier les cours associés
    cours = Cours.objects.filter(classe=classe_med6)
    print(f"Nombre de cours: {cours.count()}")
    for c in cours:
        print(f"  - {c.titre} (actif: {c.actif})")
else:
    print("Classe Médecine 6 n'existe pas!")
