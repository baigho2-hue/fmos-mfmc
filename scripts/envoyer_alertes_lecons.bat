@echo off
REM Script pour envoyer les alertes de leçons quotidiennement
REM Usage: Ce script doit être exécuté par le Planificateur de tâches Windows

cd /d "%~dp0.."
call venv\Scripts\activate.bat
python manage.py envoyer_alertes_lecons
deactivate

REM Log de l'exécution
echo [%date% %time%] Commande envoyer_alertes_lecons executee >> logs\alertes_lecons.log

