from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6
from django.db.models import Count

print("=== VÉRIFICATION DOUBLONS ===\n")

# 1. Vérifier les doublons de matricule dans Utilisateur
doublons_username = Utilisateur.objects.filter(
    classe='Médecine 6',
    type_utilisateur='etudiant'
).values('username').annotate(count=Count('username')).filter(count__gt=1)

print(f"1. Doublons de matricule (username): {doublons_username.count()}")
if doublons_username.exists():
    for d in doublons_username[:5]:
        print(f"   - {d['username']}: {d['count']} occurrences")

# 2. Compter les utilisateurs uniques
users_med6 = Utilisateur.objects.filter(classe='Médecine 6', type_utilisateur='etudiant')
unique_usernames = users_med6.values('username').distinct().count()
print(f"\n2. Utilisateurs Med6:")
print(f"   - Total: {users_med6.count()}")
print(f"   - Usernames uniques: {unique_usernames}")

# 3. EtudiantMed6
liste = ListeMed6.objects.filter(active=True).first()
if liste:
    etudiants_med6 = EtudiantMed6.objects.filter(liste=liste, actif=True)
    print(f"\n3. EtudiantMed6 (liste {liste.annee_universitaire}):")
    print(f"   - Total actifs: {etudiants_med6.count()}")
    print(f"   - Avec compte utilisateur: {etudiants_med6.filter(utilisateur__isnull=False).count()}")
    print(f"   - Sans compte: {etudiants_med6.filter(utilisateur__isnull=True).count()}")

print("\n=== FIN VÉRIFICATION ===")
