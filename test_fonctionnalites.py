#!/usr/bin/env python
"""
Script de test des fonctionnalités principales de l'application Django FMOS-MFMC
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist

# Import des modèles
from apps.utilisateurs.models import Utilisateur
from apps.utilisateurs.models_formation import Formation, Classe, Cours, Lecon
from apps.utilisateurs.models_programme_desmfmc import (
    CSComUCentre, StageRotationDES, StagePremiereAnnee
)
from apps.utilisateurs.models_carnet_stage import CarnetStage, EvaluationStage
# Autres modèles (optionnels pour les tests de base)
try:
    from apps.evaluations.models import Evaluation, EvaluationPratique
    EVALUATIONS_AVAILABLE = True
except ImportError:
    EVALUATIONS_AVAILABLE = False

try:
    from apps.admissions.models import Inscription, DossierCandidature
    ADMISSIONS_AVAILABLE = True
except ImportError:
    ADMISSIONS_AVAILABLE = False

print("=" * 80)
print("TEST DES FONCTIONNALITÉS PRINCIPALES - FMOS-MFMC")
print("=" * 80)
print()

# Compteurs de tests
tests_passes = 0
tests_echoues = 0
erreurs = []

def test_titre(titre):
    """Affiche un titre de section"""
    print(f"\n{'='*80}")
    print(f"  {titre}")
    print(f"{'='*80}")

def test_resultat(nom_test, resultat, details=""):
    """Affiche le résultat d'un test"""
    global tests_passes, tests_echoues
    if resultat:
        print(f"[OK] {nom_test}")
        if details:
            print(f"     {details}")
        tests_passes += 1
    else:
        print(f"[ERREUR] {nom_test}")
        if details:
            print(f"     {details}")
        tests_echoues += 1
        erreurs.append(f"{nom_test}: {details}")

# ============================================================================
# 1. TEST DE LA CONNEXION À LA BASE DE DONNÉES
# ============================================================================
test_titre("1. CONNEXION À LA BASE DE DONNÉES")

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        resultat = cursor.fetchone()
        test_resultat("Connexion PostgreSQL", resultat[0] == 1, "Connexion réussie à Supabase")
except Exception as e:
    test_resultat("Connexion PostgreSQL", False, f"Erreur: {str(e)}")

# ============================================================================
# 2. TEST DES MODÈLES PRINCIPAUX
# ============================================================================
test_titre("2. MODÈLES PRINCIPAUX")

# Test Utilisateur
try:
    total_utilisateurs = Utilisateur.objects.count()
    total_etudiants = Utilisateur.objects.filter(type_utilisateur='etudiant').count()
    total_enseignants = Utilisateur.objects.filter(type_utilisateur='enseignant').count()
    total_coordination = Utilisateur.objects.filter(est_membre_coordination=True).count()
    
    test_resultat("Modèle Utilisateur", True, 
                  f"Total: {total_utilisateurs} | Étudiants: {total_etudiants} | "
                  f"Enseignants: {total_enseignants} | Coordination: {total_coordination}")
except Exception as e:
    test_resultat("Modèle Utilisateur", False, f"Erreur: {str(e)}")

# Test Formation
try:
    total_formations = Formation.objects.count()
    formation_desmfmc = Formation.objects.filter(code='DESMFMC').first()
    test_resultat("Modèle Formation", True, 
                  f"Total: {total_formations} | DESMFMC: {'Trouvé' if formation_desmfmc else 'Non trouvé'}")
except Exception as e:
    test_resultat("Modèle Formation", False, f"Erreur: {str(e)}")

# Test Classe
try:
    total_classes = Classe.objects.count()
    classes_desmfmc = Classe.objects.filter(formation__code='DESMFMC').count()
    test_resultat("Modèle Classe", True, 
                  f"Total: {total_classes} | DESMFMC: {classes_desmfmc}")
except Exception as e:
    test_resultat("Modèle Classe", False, f"Erreur: {str(e)}")

# Test Cours
try:
    total_cours = Cours.objects.count()
    cours_actifs = Cours.objects.filter(actif=True).count()
    test_resultat("Modèle Cours", True, 
                  f"Total: {total_cours} | Actifs: {cours_actifs}")
except Exception as e:
    test_resultat("Modèle Cours", False, f"Erreur: {str(e)}")

# Test Leçon
try:
    total_lecons = Lecon.objects.count()
    lecons_actives = Lecon.objects.filter(actif=True).count()
    test_resultat("Modèle Leçon", True, 
                  f"Total: {total_lecons} | Actives: {lecons_actives}")
except Exception as e:
    test_resultat("Modèle Leçon", False, f"Erreur: {str(e)}")

# Test CSCom-U
try:
    total_cscom = CSComUCentre.objects.count()
    cscom_actifs = CSComUCentre.objects.filter(actif=True).count()
    test_resultat("Modèle CSCom-U", True, 
                  f"Total: {total_cscom} | Actifs: {cscom_actifs}")
except Exception as e:
    test_resultat("Modèle CSCom-U", False, f"Erreur: {str(e)}")

# Test Stage
try:
    total_stages_rotation = StageRotationDES.objects.count()
    total_stages_premiere = StagePremiereAnnee.objects.count()
    test_resultat("Modèle Stage", True, 
                  f"Rotation DES: {total_stages_rotation} | Première année: {total_stages_premiere}")
except Exception as e:
    test_resultat("Modèle Stage", False, f"Erreur: {str(e)}")

# ============================================================================
# 3. TEST DES RELATIONS ENTRE MODÈLES
# ============================================================================
test_titre("3. RELATIONS ENTRE MODÈLES")

# Test Classe -> Cours
try:
    classe_test = Classe.objects.first()
    if classe_test:
        cours_classe = classe_test.cours_set.count()
        test_resultat("Relation Classe -> Cours", True, 
                      f"Classe '{classe_test.nom}' a {cours_classe} cours")
    else:
        test_resultat("Relation Classe -> Cours", False, "Aucune classe trouvée")
except Exception as e:
    test_resultat("Relation Classe -> Cours", False, f"Erreur: {str(e)}")

# Test Cours -> Leçons
try:
    cours_test = Cours.objects.first()
    if cours_test:
        lecons_cours = cours_test.lecon_set.count()
        test_resultat("Relation Cours -> Leçons", True, 
                      f"Cours '{cours_test.titre}' a {lecons_cours} leçons")
    else:
        test_resultat("Relation Cours -> Leçons", False, "Aucun cours trouvé")
except Exception as e:
    test_resultat("Relation Cours -> Leçons", False, f"Erreur: {str(e)}")

# Test Utilisateur -> Classe
try:
    etudiant_test = Utilisateur.objects.filter(type_utilisateur='etudiant').first()
    if etudiant_test:
        classe_etudiant = etudiant_test.classe
        test_resultat("Relation Utilisateur -> Classe", True, 
                      f"Étudiant '{etudiant_test.username}' dans classe: {classe_etudiant or 'Aucune'}")
    else:
        test_resultat("Relation Utilisateur -> Classe", False, "Aucun étudiant trouvé")
except Exception as e:
    test_resultat("Relation Utilisateur -> Classe", False, f"Erreur: {str(e)}")

# ============================================================================
# 4. TEST DES DONNÉES CRITIQUES
# ============================================================================
test_titre("4. DONNÉES CRITIQUES")

# Test Superutilisateur
try:
    admin = Utilisateur.objects.filter(username='admin', is_superuser=True).first()
    test_resultat("Superutilisateur admin", admin is not None, 
                  f"Admin trouvé: {admin is not None}")
except Exception as e:
    test_resultat("Superutilisateur admin", False, f"Erreur: {str(e)}")

# Test Formation DESMFMC
try:
    desmfmc = Formation.objects.filter(code='DESMFMC').first()
    if desmfmc:
        classes_desmfmc = desmfmc.classe_set.count()
        test_resultat("Formation DESMFMC", True, 
                      f"Formation trouvée avec {classes_desmfmc} classes")
    else:
        test_resultat("Formation DESMFMC", False, "Formation DESMFMC non trouvée")
except Exception as e:
    test_resultat("Formation DESMFMC", False, f"Erreur: {str(e)}")

# Test CSCom-U avec superviseurs
try:
    cscom_avec_superviseur = CSComUCentre.objects.exclude(
        cec_superviseur_principal=''
    ).exclude(cec_superviseur_principal__isnull=True).count()
    test_resultat("CSCom-U avec superviseurs", True, 
                  f"{cscom_avec_superviseur} CSCom-U ont un superviseur")
except Exception as e:
    test_resultat("CSCom-U avec superviseurs", False, f"Erreur: {str(e)}")

# ============================================================================
# 5. TEST DES FONCTIONNALITÉS ADMIN
# ============================================================================
test_titre("5. FONCTIONNALITÉS ADMIN")

# Test accès admin
try:
    from django.contrib import admin
    models_registres = len(admin.site._registry)
    test_resultat("Modèles enregistrés dans Admin", True, 
                  f"{models_registres} modèles enregistrés")
except Exception as e:
    test_resultat("Modèles enregistrés dans Admin", False, f"Erreur: {str(e)}")

# ============================================================================
# 6. TEST DES MÉTHODES PERSONNALISÉES
# ============================================================================
test_titre("6. MÉTHODES PERSONNALISÉES")

# Test méthode nombre_superviseurs sur CSComUCentre
try:
    cscom_test = CSComUCentre.objects.first()
    if cscom_test:
        nb_superviseurs = cscom_test.nombre_superviseurs()
        test_resultat("Méthode nombre_superviseurs", True, 
                      f"CSCom '{cscom_test.nom}' a {nb_superviseurs} superviseurs")
    else:
        test_resultat("Méthode nombre_superviseurs", False, "Aucun CSCom trouvé")
except Exception as e:
    test_resultat("Méthode nombre_superviseurs", False, f"Erreur: {str(e)}")

# Test méthode nombre_stages sur CSComUCentre
try:
    cscom_test = CSComUCentre.objects.first()
    if cscom_test:
        nb_stages = cscom_test.nombre_stages()
        test_resultat("Méthode nombre_stages", True, 
                      f"CSCom '{cscom_test.nom}' a {nb_stages} stages")
    else:
        test_resultat("Méthode nombre_stages", False, "Aucun CSCom trouvé")
except Exception as e:
    test_resultat("Méthode nombre_stages", False, f"Erreur: {str(e)}")

# ============================================================================
# 7. TEST DES STATISTIQUES GLOBALES
# ============================================================================
test_titre("7. STATISTIQUES GLOBALES")

try:
    stats = {
        'utilisateurs': Utilisateur.objects.count(),
        'etudiants': Utilisateur.objects.filter(type_utilisateur='etudiant').count(),
        'enseignants': Utilisateur.objects.filter(type_utilisateur='enseignant').count(),
        'formations': Formation.objects.count(),
        'classes': Classe.objects.count(),
        'cours': Cours.objects.count(),
        'lecons': Lecon.objects.count(),
        'cscom': CSComUCentre.objects.count(),
        'stages_rotation': StageRotationDES.objects.count(),
        'stages_premiere': StagePremiereAnnee.objects.count(),
        'carnets_stage': CarnetStage.objects.count(),
        'evaluations_stage': EvaluationStage.objects.count(),
    }
    
    print("\n[STATISTIQUES] Statistiques de l'application:")
    for key, value in stats.items():
        print(f"   {key.capitalize()}: {value}")
    
    test_resultat("Statistiques globales", True, "Statistiques calculées avec succès")
except Exception as e:
    test_resultat("Statistiques globales", False, f"Erreur: {str(e)}")

# ============================================================================
# RÉSUMÉ DES TESTS
# ============================================================================
test_titre("RÉSUMÉ DES TESTS")

total_tests = tests_passes + tests_echoues
pourcentage_reussite = (tests_passes / total_tests * 100) if total_tests > 0 else 0

print(f"\n[RESULTATS] Résultats:")
print(f"   Tests réussis: {tests_passes}/{total_tests} ({pourcentage_reussite:.1f}%)")
print(f"   Tests échoués: {tests_echoues}/{total_tests}")

if erreurs:
    print(f"\n[ERREURS] Erreurs rencontrées:")
    for i, erreur in enumerate(erreurs, 1):
        print(f"   {i}. {erreur}")

if tests_echoues == 0:
    print("\n[SUCCES] Tous les tests sont passes avec succes!")
else:
    print(f"\n[ATTENTION] {tests_echoues} test(s) ont echoue. Verifiez les erreurs ci-dessus.")

print("\n" + "=" * 80)

