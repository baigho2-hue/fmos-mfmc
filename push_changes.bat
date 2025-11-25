@echo off
chcp 65001 >nul
echo ========================================
echo PUSH VERS GIT
echo ========================================
echo.

echo Ajout des fichiers...
git add apps/utilisateurs/admin.py
git add scripts/verifier_noms_etudiants.py
git add scripts/corriger_email_dicko.py
git add scripts/push_to_git.py

echo.
echo Verification de l'etat...
git status --short

echo.
echo Creation du commit...
git commit -m "fix(admin): improve name display for DESMFMC students"

echo.
echo Push vers le depot distant...
git push origin main

echo.
echo ========================================
echo TERMINE
echo ========================================
pause

