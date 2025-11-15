#!/bin/bash
# Script shell pour Linux/Mac - Envoi des alertes de leçons quotidiennement
# À utiliser avec cron

# Obtenir le répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Aller dans le répertoire du projet
cd "$PROJECT_DIR"

# Activer l'environnement virtuel si il existe
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Exécuter la commande Django
python manage.py envoyer_alertes_lecons

# Vérifier le code de retour
if [ $? -ne 0 ]; then
    echo "ERREUR lors de l'exécution de la commande"
    exit 1
fi

echo "Commande exécutée avec succès"
exit 0

