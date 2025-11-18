#!/usr/bin/env python
"""
Script de vérification pour le déploiement Render
Vérifie que tous les fichiers et configurations nécessaires sont présents
"""

import os
import sys
from pathlib import Path

# Couleurs pour l'affichage
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    print(f"{RED}❌ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{RESET}")

def check_file_exists(filepath, description):
    """Vérifie si un fichier existe"""
    if Path(filepath).exists():
        print_success(f"{description} : {filepath}")
        return True
    else:
        print_error(f"{description} manquant : {filepath}")
        return False

def check_file_content(filepath, required_content, description):
    """Vérifie le contenu d'un fichier"""
    if not Path(filepath).exists():
        print_error(f"{description} : Fichier introuvable")
        return False
    
    content = Path(filepath).read_text()
    if required_content in content:
        print_success(f"{description} : Contenu correct")
        return True
    else:
        print_warning(f"{description} : Contenu à vérifier")
        return False

def check_requirements():
    """Vérifie les dépendances dans requirements.txt"""
    print("\n📦 Vérification des dépendances...")
    
    required_packages = [
        'Django',
        'gunicorn',
        'whitenoise',
        'psycopg2-binary',
        'dj-database-url',
    ]
    
    if not Path('requirements.txt').exists():
        print_error("requirements.txt introuvable")
        return False
    
    content = Path('requirements.txt').read_text()
    missing = []
    
    for package in required_packages:
        if package.lower() in content.lower():
            print_success(f"Package présent : {package}")
        else:
            print_error(f"Package manquant : {package}")
            missing.append(package)
    
    return len(missing) == 0

def check_settings():
    """Vérifie la configuration Django"""
    print("\n⚙️  Vérification de la configuration Django...")
    
    settings_path = Path('core/settings.py')
    if not settings_path.exists():
        print_error("core/settings.py introuvable")
        return False
    
    content = settings_path.read_text()
    
    checks = [
        ('DATABASE_URL' in content, "Configuration DATABASE_URL"),
        ('whitenoise' in content.lower(), "Configuration WhiteNoise"),
        ('STATIC_ROOT' in content, "Configuration STATIC_ROOT"),
        ('SECRET_KEY' in content, "Configuration SECRET_KEY"),
        ('ALLOWED_HOSTS' in content, "Configuration ALLOWED_HOSTS"),
    ]
    
    all_ok = True
    for check, description in checks:
        if check:
            print_success(description)
        else:
            print_error(f"{description} manquante")
            all_ok = False
    
    return all_ok

def check_render_config():
    """Vérifie la configuration Render"""
    print("\n🚀 Vérification de la configuration Render...")
    
    checks = [
        ('render.yaml', "Fichier render.yaml"),
        ('Procfile', "Fichier Procfile"),
        ('runtime.txt', "Fichier runtime.txt"),
    ]
    
    all_ok = True
    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    # Vérifier le contenu du Procfile
    if Path('Procfile').exists():
        procfile_content = Path('Procfile').read_text()
        if 'gunicorn' in procfile_content and 'core.wsgi' in procfile_content:
            print_success("Procfile : Commande gunicorn correcte")
        else:
            print_error("Procfile : Commande gunicorn incorrecte")
            all_ok = False
    
    return all_ok

def check_env_vars():
    """Vérifie les variables d'environnement nécessaires"""
    print("\n🔐 Vérification des variables d'environnement...")
    
    required_vars = [
        'SECRET_KEY',
        'DEBUG',
        'ALLOWED_HOSTS',
        'DATABASE_URL',
    ]
    
    print_warning("Variables d'environnement à configurer dans Render :")
    for var in required_vars:
        print(f"  - {var}")
    
    return True

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🔍 Vérification du déploiement Render")
    print("=" * 60)
    
    # Changer vers le répertoire du projet
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    results = []
    
    # Vérifications
    results.append(("Dépendances", check_requirements()))
    results.append(("Configuration Django", check_settings()))
    results.append(("Configuration Render", check_render_config()))
    results.append(("Variables d'environnement", check_env_vars()))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 Résumé des vérifications")
    print("=" * 60)
    
    all_ok = True
    for name, result in results:
        status = "✅ OK" if result else "❌ ÉCHEC"
        print(f"{name} : {status}")
        if not result:
            all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print_success("Toutes les vérifications sont passées !")
        print("Vous pouvez procéder au déploiement sur Render.")
        return 0
    else:
        print_error("Certaines vérifications ont échoué.")
        print("Veuillez corriger les erreurs avant de déployer.")
        return 1

if __name__ == '__main__':
    sys.exit(main())

