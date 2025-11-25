#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour pousser les changements vers git.
"""
import subprocess
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)

def run_command(cmd):
    """Exécute une commande et retourne le résultat"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

print("=" * 70)
print("PUSH VERS GIT")
print("=" * 70)

# Vérifier l'état
print("\n1. Vérification de l'état du dépôt...")
code, stdout, stderr = run_command("git status --short")
print(stdout)
if stderr:
    print("Erreurs:", stderr)

# Ajouter les fichiers modifiés
print("\n2. Ajout des fichiers...")
files_to_add = [
    "apps/utilisateurs/admin.py",
    "scripts/verifier_noms_etudiants.py",
    "scripts/corriger_email_dicko.py"
]

for file in files_to_add:
    if os.path.exists(file):
        code, stdout, stderr = run_command(f'git add "{file}"')
        if stdout:
            print(f"  ✅ {file}")
        if stderr:
            print(f"  ⚠️  {file}: {stderr}")
    else:
        print(f"  ⚠️  {file} n'existe pas")

# Vérifier s'il y a des changements à committer
print("\n3. Vérification des changements à committer...")
code, stdout, stderr = run_command("git status --short")
if stdout.strip():
    print("Changements détectés:")
    print(stdout)
    
    # Commit
    print("\n4. Création du commit...")
    commit_msg = "fix(admin): improve name display for DESMFMC students"
    code, stdout, stderr = run_command(f'git commit -m "{commit_msg}"')
    print(stdout)
    if stderr:
        print("Erreurs:", stderr)
    
    if code == 0:
        print("✅ Commit créé avec succès")
        
        # Push
        print("\n5. Push vers le dépôt distant...")
        code, stdout, stderr = run_command("git push origin main")
        print(stdout)
        if stderr:
            print("Erreurs:", stderr)
        
        if code == 0:
            print("\n✅ Push réussi!")
        else:
            print("\n❌ Erreur lors du push")
    else:
        print("\n❌ Erreur lors du commit")
else:
    print("Aucun changement à committer")
    print("\n6. Vérification du dernier commit...")
    code, stdout, stderr = run_command("git log --oneline -1")
    print(stdout)

print("\n" + "=" * 70)

