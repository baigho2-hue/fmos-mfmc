@echo off
REM Script batch pour Windows - Envoi des alertes de leçons quotidiennement
REM À utiliser avec le Planificateur de tâches Windows

cd /d "%~dp0\.."
python manage.py envoyer_alertes_lecons

if %ERRORLEVEL% NEQ 0 (
    echo ERREUR lors de l'execution de la commande
    exit /b 1
)

echo Commande executee avec succes
exit /b 0

