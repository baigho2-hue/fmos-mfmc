#!/usr/bin/env python
"""
Script de vérification avant déploiement
"""
import os
from pathlib import Path

print("=" * 80)
print("VERIFICATION PRE-DEPLOIEMENT - FMOS-MFMC")
print("=" * 80)
print()

erreurs = []
avertissements = []

# Vérifier les fichiers nécessaires
fichiers_requis = [
    'Procfile',
    'runtime.txt',
    'requirements.txt',
    '.gitignore',
    'manage.py',
    'core/settings.py',
    'core/wsgi.py',
]

print("[1] Verification des fichiers requis...")
for fichier in fichiers_requis:
    if Path(fichier).exists():
        print(f"  [OK] {fichier}")
    else:
        print(f"  [ERREUR] {fichier} manquant")
        erreurs.append(f"Fichier manquant: {fichier}")

# Vérifier le Procfile
print("\n[2] Verification du Procfile...")
if Path('Procfile').exists():
    with open('Procfile', 'r') as f:
        contenu = f.read()
        if 'gunicorn' in contenu:
            print("  [OK] Procfile contient gunicorn")
        else:
            print("  [ERREUR] Procfile ne contient pas gunicorn")
            erreurs.append("Procfile invalide")
        if '$PORT' in contenu:
            print("  [OK] Procfile utilise $PORT")
        else:
            print("  [ATTENTION] Procfile n'utilise pas $PORT")
            avertissements.append("Procfile devrait utiliser $PORT")

# Vérifier runtime.txt
print("\n[3] Verification de runtime.txt...")
if Path('runtime.txt').exists():
    with open('runtime.txt', 'r') as f:
        version = f.read().strip()
        print(f"  [OK] Version Python: {version}")
        if not version.startswith('python-'):
            print("  [ATTENTION] Format devrait etre python-X.Y.Z")
            avertissements.append("Format runtime.txt")

# Vérifier requirements.txt
print("\n[4] Verification de requirements.txt...")
packages_requis = ['Django', 'gunicorn', 'whitenoise', 'psycopg2', 'dj-database-url']
if Path('requirements.txt').exists():
    with open('requirements.txt', 'r') as f:
        contenu = f.read()
        for package in packages_requis:
            if package.lower() in contenu.lower():
                print(f"  [OK] {package} present")
            else:
                print(f"  [ERREUR] {package} manquant")
                erreurs.append(f"Package manquant: {package}")

# Vérifier .gitignore
print("\n[5] Verification de .gitignore...")
if Path('.gitignore').exists():
    with open('.gitignore', 'r') as f:
        contenu = f.read()
        if '.env' in contenu:
            print("  [OK] .env dans .gitignore")
        else:
            print("  [ATTENTION] .env devrait etre dans .gitignore")
            avertissements.append(".env devrait etre ignore")
        if 'staticfiles' in contenu or 'staticfiles/' in contenu:
            print("  [OK] staticfiles dans .gitignore")
        else:
            print("  [ATTENTION] staticfiles devrait etre dans .gitignore")
            avertissements.append("staticfiles devrait etre ignore")

# Vérifier settings.py
print("\n[6] Verification de settings.py...")
if Path('core/settings.py').exists():
    with open('core/settings.py', 'r') as f:
        contenu = f.read()
        if 'DATABASE_URL' in contenu:
            print("  [OK] DATABASE_URL configure")
        else:
            print("  [ERREUR] DATABASE_URL non configure")
            erreurs.append("DATABASE_URL non configure dans settings.py")
        if 'whitenoise' in contenu.lower():
            print("  [OK] WhiteNoise configure")
        else:
            print("  [ERREUR] WhiteNoise non configure")
            erreurs.append("WhiteNoise non configure")
        if 'STATIC_ROOT' in contenu:
            print("  [OK] STATIC_ROOT configure")
        else:
            print("  [ATTENTION] STATIC_ROOT non configure")
            avertissements.append("STATIC_ROOT non configure")

# Résumé
print("\n" + "=" * 80)
print("RESUME")
print("=" * 80)

if erreurs:
    print(f"\n[ERREURS] {len(erreurs)} erreur(s) trouvee(s):")
    for i, erreur in enumerate(erreurs, 1):
        print(f"  {i}. {erreur}")
    print("\n[ATTENTION] Corrigez ces erreurs avant de deployer!")
else:
    print("\n[SUCCES] Aucune erreur critique trouvee!")

if avertissements:
    print(f"\n[AVERTISSEMENTS] {len(avertissements)} avertissement(s):")
    for i, avertissement in enumerate(avertissements, 1):
        print(f"  {i}. {avertissement}")
    print("\n[INFO] Ces avertissements ne bloquent pas le deploiement mais devraient etre corriges.")

if not erreurs:
    print("\n[PRET] Votre application est prete pour le deploiement!")
    print("\nProchaines etapes:")
    print("  1. Poussez votre code sur GitHub")
    print("  2. Suivez le guide GUIDE_DEPLOIEMENT_COMPLET.md")
    print("  3. Configurez les variables d'environnement sur votre plateforme")
    print("  4. Deployez!")

print("\n" + "=" * 80)

