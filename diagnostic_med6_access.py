#!/usr/bin/env python
"""
Script de diagnostic pour le flux d'authentification Med6
Ce script teste le flux complet pour identifier où l'accès échoue
"""
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
django.setup()

from apps.utilisateurs.models_med6 import EtudiantMed6, ListeMed6
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Classe, Cours, ProgressionEtudiant
from core.views_med6 import est_etudiant_med6, a_acces_gratuit_med6

print("="*70)
print("DIAGNOSTIC MED6 - TEST DU FLUX D'AUTHENTIFICATION ET D'ACCÈS AUX COURS")
print("="*70)

# 1. Vérifier la base de données Med6
print("\n1. VÉRIFICATION DE LA BASE DE DONNÉES MED6")
print("-" * 70)

listes = ListeMed6.objects.all()
print(f"Listes Med6 totales: {listes.count()}")
for liste in listes:
    print(f"  - {liste.annee_universitaire}: {liste.etudiants.count()} étudiants, Active={liste.active}")

etudiants_actifs = EtudiantMed6.objects.filter(actif=True)
print(f"\nÉtudiants Med6 actifs: {etudiants_actifs.count()}")

etudiant_test = etudiants_actifs.first()
if etudiant_test:
    print(f"Étudiant de test: {etudiant_test.matricule} - {etudiant_test.nom_complet()}")
    print(f"  - Liste: {etudiant_test.liste.annee_universitaire if etudiant_test.liste else 'AUCUNE'}")
    print(f"  - Liste active: {etudiant_test.liste.active if etudiant_test.liste else False}")
    print(f"  - Utilisateur lié: {'OUI' if etudiant_test.utilisateur else 'NON'}")
    
    if etudiant_test.utilisateur:
        user = etudiant_test.utilisateur
        print(f"  - Username: {user.username}")
        print(f"  - Classe: {user.classe}")
        print(f"  - Type: {user.type_utilisateur}")
        print(f"  - Actif: {user.is_active}")
    else:
        print("\n⚠️  Utilisateur non lié. Il sera créé lors de la première connexion.")

# 2. Vérifier les cours Med6 disponibles
print("\n2. VÉRIFICATION DES COURS MED6")
print("-" * 70)

classe_med6 = Classe.objects.filter(nom__icontains='Médecine 6').first()
if classe_med6:
    print(f"Classe Med6 trouvée: {classe_med6.nom}")
    cours_med6 = Cours.objects.filter(classe=classe_med6, actif=True)
    print(f"Cours actifs pour Med6: {cours_med6.count()}")
    
    if cours_med6.exists():
        print("\nListe des cours:")
        for i, cours in enumerate(cours_med6[:5], 1):
            print(f"  {i}. {cours.titre}")
        if cours_med6.count() > 5:
            print(f"  ... et {cours_med6.count() - 5} autres")
    else:
        print("⚠️  AUCUN COURS ACTIF TROUVÉ POUR MED6!")
else:
    print("❌ AUCUNE CLASSE 'MÉDECINE 6' TROUVÉE!")

# 3. Tester les fonctions de vérification d'accès
print("\n3. TEST DES FONCTIONS DE VÉRIFICATION D'ACCÈS")
print("-" * 70)

if etudiant_test and etudiant_test.utilisateur:
    user = etudiant_test.utilisateur
    print(f"Test avec l'utilisateur: {user.username}")
    
    # Test est_etudiant_med6
    resultat_est_etudiant = est_etudiant_med6(user)
    print(f"  - est_etudiant_med6(user): {resultat_est_etudiant}")
    
    # Test a_acces_gratuit_med6
    resultat_acces_gratuit = a_acces_gratuit_med6(user)
    print(f"  - a_acces_gratuit_med6(user): {resultat_acces_gratuit}")
    
    # Vérifier la relation etudiant_med6
    try:
        etudiant_lie = user.etudiant_med6
        print(f"  - Relation user.etudiant_med6: OK")
        print(f"    → Matricule: {etudiant_lie.matricule}")
        print(f"    → Actif: {etudiant_lie.actif}")
        print(f"    → Liste: {etudiant_lie.liste.annee_universitaire if etudiant_lie.liste else 'AUCUNE'}")
        print(f"    → Liste active: {etudiant_lie.liste.active if etudiant_lie.liste else False}")
    except AttributeError as e:
        print(f"  ❌ Erreur d'accès à user.etudiant_med6: {e}")
    
    # Vérifier les progressions
    progressions = ProgressionEtudiant.objects.filter(etudiant=user)
    print(f"\n  - Progressions créées: {progressions.count()}")
    if progressions.exists():
        print(f"    Cours associés:")
        for prog in progressions[:5]:
            print(f"      - {prog.cours.titre} ({prog.statut})")
        if progressions.count() > 5:
            print(f"      ... et {progressions.count() - 5} autres")
    else:
        print("⚠️  AUCUNE PROGRESSION CRÉÉE!")
        
elif etudiant_test:
    print("⚠️  L'étudiant test n'a pas d'utilisateur lié. Impossible de tester les fonctions d'accès.")
else:
    print("❌ Aucun étudiant de test disponible!")

# 4. Simuler le flux de connexion
print("\n4. SIMULATION DU FLUX DE CONNEXION")
print("-" * 70)

if etudiant_test:
    print(f"Simulation de connexion pour: {etudiant_test.nom_complet()}")
    print(f"  Matricule: {etudiant_test.matricule}")
    print(f"  Nom: {etudiant_test.nom}")
    print(f"  Prénom: {etudiant_test.prenom}")
    
    # Vérifier la validation du formulaire
    from apps.utilisateurs.forms_med6 import LoginMed6Form
    form_data = {
        'matricule': etudiant_test.matricule,
        'nom': etudiant_test.nom,
        'prenom': etudiant_test.prenom
    }
    form = LoginMed6Form(data=form_data)
    
    if form.is_valid():
        print("✅ Formulaire valide!")
        etudiant_form = form.cleaned_data['etudiant']
        print(f"  - Étudiant validé: {etudiant_form.nom_complet()}")
        
        # Vérifier si l'utilisateur sera créé ou existe déjà
        if etudiant_form.utilisateur:
            print("  - Utilisateur existant sera connecté")
            user = etudiant_form.utilisateur
        else:
            print("  - Nouvel utilisateur sera créé lors de la connexion")
            user = None
    else:
        print("❌ Formulaire invalide!")
        for field, errors in form.errors.items():
            print(f"  - {field}: {', '.join(errors)}")

# 5. Recommandations
print("\n5. RECOMMANDATIONS")
print("-" * 70)

problemes = []
if not classe_med6:
    problemes.append("❌ Aucune classe 'Médecine 6' trouvée → Créer la classe")
elif not cours_med6 or cours_med6.count() == 0:
    problemes.append("❌ Aucun cours actif pour Med6 → Créer des cours ou activer les cours existants")

if etudiant_test and etudiant_test.utilisateur:
    if not a_acces_gratuit_med6(etudiant_test.utilisateur):
        problemes.append("❌ La fonction a_acces_gratuit_med6 retourne False → Déboguer la logique de vérification")
    
    if ProgressionEtudiant.objects.filter(etudiant=etudiant_test.utilisateur).count() == 0:
        problemes.append("⚠️  Aucune progression créée → Vérifier la création automatique lors de la connexion")

if problemes:
    print("Problèmes identifiés:")
    for prob in problemes:
        print(f"  {prob}")
else:
    print("✅ Aucun problème majeur identifié!")
    print("   Le flux d'authentification devrait fonctionner correctement.")

print("\n" + "="*70)
print("FIN DU DIAGNOSTIC")
print("="*70)
