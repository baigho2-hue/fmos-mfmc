#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test pour diagnostiquer les problèmes d'import
"""
import os
import sys

print("=== Diagnostic des imports ===\n")

# Afficher le répertoire actuel
print(f"1. Répertoire actuel: {os.getcwd()}")

# Afficher le chemin du script
script_path = os.path.abspath(__file__)
print(f"2. Chemin du script: {script_path}")

# Calculer le répertoire racine
project_root = os.path.dirname(os.path.dirname(script_path))
print(f"3. Répertoire racine calculé: {project_root}")

# Afficher le PYTHONPATH actuel
print(f"\n4. PYTHONPATH actuel:")
for path in sys.path:
    print(f"   - {path}")

# Configurer l'encodage pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ajouter le répertoire racine
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"\n5. [OK] Repertoire racine ajoute au PYTHONPATH")
else:
    print(f"\n5. [WARN] Repertoire racine deja dans PYTHONPATH")

# Vérifier si core existe
print(f"\n6. Verification de l'existence de 'core':")
core_path = os.path.join(project_root, 'core')
if os.path.exists(core_path):
    print(f"   [OK] Le dossier 'core' existe: {core_path}")
    if os.path.exists(os.path.join(core_path, '__init__.py')):
        print(f"   [OK] Le fichier 'core/__init__.py' existe")
    else:
        print(f"   [WARN] Le fichier 'core/__init__.py' n'existe pas")
    if os.path.exists(os.path.join(core_path, 'settings.py')):
        print(f"   [OK] Le fichier 'core/settings.py' existe")
    else:
        print(f"   [ERROR] Le fichier 'core/settings.py' n'existe pas")
else:
    print(f"   [ERROR] Le dossier 'core' n'existe pas: {core_path}")

# Essayer d'importer core
print(f"\n7. Tentative d'import de 'core':")
try:
    import core
    print(f"   [OK] Import de 'core' reussi")
    print(f"   [INFO] Emplacement: {core.__file__}")
except ImportError as e:
    print(f"   [ERROR] Erreur d'import: {e}")

# Essayer d'importer core.settings
print(f"\n8. Tentative d'import de 'core.settings':")
try:
    from core import settings
    print(f"   [OK] Import de 'core.settings' reussi")
except ImportError as e:
    print(f"   [ERROR] Erreur d'import: {e}")

# Configurer Django
print(f"\n9. Configuration de Django:")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
print(f"   [OK] DJANGO_SETTINGS_MODULE = {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# Essayer d'importer Django
print(f"\n10. Tentative d'import de Django:")
try:
    import django
    print(f"    [OK] Import de Django reussi (version: {django.get_version()})")
    django.setup()
    print(f"    [OK] django.setup() reussi")
except Exception as e:
    print(f"    [ERROR] Erreur: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Fin du diagnostic ===")

