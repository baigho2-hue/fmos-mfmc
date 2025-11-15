@echo off
REM Script pour créer les tables PostgreSQL pour FMOS MFMC

echo ========================================
echo Creation des tables PostgreSQL
echo ========================================
echo.

REM Activer l'environnement virtuel
echo [1/5] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERREUR: Impossible d'activer l'environnement virtuel
    echo Assurez-vous que .venv existe et contient les scripts
    pause
    exit /b 1
)

REM Installer les dependances
echo [2/5] Installation des dependances...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERREUR: Echec de l'installation des dependances
    pause
    exit /b 1
)

REM Creer les migrations
echo [3/5] Creation des migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo ERREUR: Echec de la creation des migrations
    pause
    exit /b 1
)

REM Appliquer les migrations
echo [4/5] Application des migrations (creation des tables)...
python manage.py migrate
if errorlevel 1 (
    echo ERREUR: Echec de l'application des migrations
    echo Verifiez que PostgreSQL est demarre et que la base de donnees existe
    pause
    exit /b 1
)

REM Afficher l'etat des migrations
echo [5/5] Etat des migrations:
python manage.py showmigrations

echo.
echo ========================================
echo Tables creees avec succes!
echo ========================================
echo.
echo Prochaines etapes:
echo 1. Creer un superutilisateur: python manage.py createsuperuser
echo 2. Initialiser le programme DESMFMC: python manage.py init_programme_desmfmc_detaille
echo.
pause

