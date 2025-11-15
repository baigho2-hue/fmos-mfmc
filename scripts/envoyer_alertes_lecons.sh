#!/bin/bash
# Script pour envoyer les alertes de leçons quotidiennement
# Usage: Ajouter ce script au crontab pour exécution quotidienne

# Aller dans le répertoire du projet
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_DIR"

# Activer l'environnement virtuel (si présent)
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

# Exécuter la commande Django
python manage.py envoyer_alertes_lecons

# Désactiver l'environnement virtuel
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi

# Log de l'exécution
LOG_DIR="$PROJECT_DIR/logs"
mkdir -p "$LOG_DIR"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Commande envoyer_alertes_lecons executee" >> "$LOG_DIR/alertes_lecons.log"

