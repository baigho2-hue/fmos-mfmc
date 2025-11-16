#!/usr/bin/env python
"""
Script de test des fichiers statiques de l'application Django FMOS-MFMC
"""
import os
import sys
import django
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from django.contrib.staticfiles.finders import find

print("=" * 80)
print("TEST DES FICHIERS STATIQUES - FMOS-MFMC")
print("=" * 80)
print()

# Compteurs
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
# 1. CONFIGURATION DES FICHIERS STATIQUES
# ============================================================================
test_titre("1. CONFIGURATION DES FICHIERS STATIQUES")

try:
    static_url = settings.STATIC_URL
    static_root = settings.STATIC_ROOT
    staticfiles_dirs = settings.STATICFILES_DIRS
    
    test_resultat("Configuration STATIC_URL", static_url == '/static/', 
                  f"STATIC_URL: {static_url}")
    test_resultat("Configuration STATIC_ROOT", static_root is not None,
                  f"STATIC_ROOT: {static_root}")
    test_resultat("Configuration STATICFILES_DIRS", len(staticfiles_dirs) > 0,
                  f"STATICFILES_DIRS: {staticfiles_dirs}")
except Exception as e:
    test_resultat("Configuration fichiers statiques", False, f"Erreur: {str(e)}")

# ============================================================================
# 2. VÉRIFICATION DES DOSSIERS STATIQUES
# ============================================================================
test_titre("2. VÉRIFICATION DES DOSSIERS STATIQUES")

# Vérifier le dossier static source
static_dir = Path(settings.BASE_DIR) / 'static'
test_resultat("Dossier static source existe", static_dir.exists(),
              f"Chemin: {static_dir}")

# Vérifier le dossier staticfiles (pour production)
staticfiles_dir = Path(settings.STATIC_ROOT)
if staticfiles_dir:
    test_resultat("Dossier staticfiles existe", staticfiles_dir.exists(),
                  f"Chemin: {staticfiles_dir}")
else:
    test_resultat("Dossier staticfiles existe", False, "STATIC_ROOT non configuré")

# ============================================================================
# 3. VÉRIFICATION DES FICHIERS STATIQUES PRINCIPAUX
# ============================================================================
test_titre("3. FICHIERS STATIQUES PRINCIPAUX")

# Liste des fichiers statiques à vérifier
fichiers_importants = [
    'css/style.css',
    'js/menu.js',
    'js/news-ticker.js',
    'images/favicon.ico',
    'images/logo USTTB.png',
    'images/logo_fmos.png',
]

for fichier in fichiers_importants:
    try:
        chemin_trouve = find(fichier)
        if chemin_trouve:
            taille = os.path.getsize(chemin_trouve) if os.path.exists(chemin_trouve) else 0
            test_resultat(f"Fichier {fichier}", True, 
                         f"Trouvé: {chemin_trouve} ({taille} octets)")
        else:
            test_resultat(f"Fichier {fichier}", False, "Fichier non trouvé")
    except Exception as e:
        test_resultat(f"Fichier {fichier}", False, f"Erreur: {str(e)}")

# ============================================================================
# 4. LISTE COMPLÈTE DES FICHIERS STATIQUES
# ============================================================================
test_titre("4. LISTE COMPLÈTE DES FICHIERS STATIQUES")

try:
    fichiers_css = list((static_dir / 'css').glob('*.css')) if (static_dir / 'css').exists() else []
    fichiers_js = list((static_dir / 'js').glob('*.js')) if (static_dir / 'js').exists() else []
    fichiers_images = list((static_dir / 'images').glob('*')) if (static_dir / 'images').exists() else []
    
    print(f"\n[CSS] Fichiers CSS trouvés: {len(fichiers_css)}")
    for f in fichiers_css:
        taille = f.stat().st_size
        print(f"     - {f.name} ({taille} octets)")
    
    print(f"\n[JS] Fichiers JavaScript trouvés: {len(fichiers_js)}")
    for f in fichiers_js:
        taille = f.stat().st_size
        print(f"     - {f.name} ({taille} octets)")
    
    print(f"\n[IMAGES] Fichiers images trouvés: {len(fichiers_images)}")
    for f in fichiers_images:
        taille = f.stat().st_size
        print(f"     - {f.name} ({taille} octets)")
    
    total_fichiers = len(fichiers_css) + len(fichiers_js) + len(fichiers_images)
    test_resultat("Liste des fichiers statiques", True,
                  f"Total: {total_fichiers} fichiers")
except Exception as e:
    test_resultat("Liste des fichiers statiques", False, f"Erreur: {str(e)}")

# ============================================================================
# 5. VÉRIFICATION WHITENOISE
# ============================================================================
test_titre("5. CONFIGURATION WHITENOISE")

try:
    storage = settings.STATICFILES_STORAGE
    whitenoise_configure = 'whitenoise' in storage.lower()
    test_resultat("WhiteNoise configuré", whitenoise_configure,
                  f"Storage: {storage}")
    
    # Vérifier que WhiteNoise est dans MIDDLEWARE
    middleware = settings.MIDDLEWARE
    whitenoise_middleware = any('whitenoise' in m.lower() for m in middleware)
    test_resultat("WhiteNoise dans MIDDLEWARE", whitenoise_middleware,
                  "Middleware configuré pour servir les fichiers statiques")
except Exception as e:
    test_resultat("Configuration WhiteNoise", False, f"Erreur: {str(e)}")

# ============================================================================
# 6. VÉRIFICATION DES FICHIERS MÉDIAS
# ============================================================================
test_titre("6. CONFIGURATION DES FICHIERS MÉDIAS")

try:
    media_url = settings.MEDIA_URL
    media_root = settings.MEDIA_ROOT
    
    test_resultat("Configuration MEDIA_URL", media_url == '/media/',
                  f"MEDIA_URL: {media_url}")
    test_resultat("Configuration MEDIA_ROOT", media_root is not None,
                  f"MEDIA_ROOT: {media_root}")
    
    # Vérifier si le dossier media existe
    media_dir = Path(media_root)
    if media_dir.exists():
        fichiers_media = list(media_dir.rglob('*'))
        test_resultat("Dossier media existe", True,
                     f"Contient {len(fichiers_media)} fichiers")
    else:
        test_resultat("Dossier media existe", False,
                     "Le dossier sera créé automatiquement lors du premier upload")
except Exception as e:
    test_resultat("Configuration fichiers médias", False, f"Erreur: {str(e)}")

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

