#!/bin/bash
# Script pour créer les tables PostgreSQL pour FMOS MFMC

echo "========================================"
echo "Création des tables PostgreSQL"
echo "========================================"
echo ""

# Activer l'environnement virtuel
echo "[1/5] Activation de l'environnement virtuel..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERREUR: Impossible d'activer l'environnement virtuel"
    echo "Assurez-vous que .venv existe et contient les scripts"
    exit 1
fi

# Installer les dépendances
echo "[2/5] Installation des dépendances..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERREUR: Échec de l'installation des dépendances"
    exit 1
fi

# Créer les migrations
echo "[3/5] Création des migrations..."
python manage.py makemigrations
if [ $? -ne 0 ]; then
    echo "ERREUR: Échec de la création des migrations"
    exit 1
fi

# Appliquer les migrations
echo "[4/5] Application des migrations (création des tables)..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERREUR: Échec de l'application des migrations"
    echo "Vérifiez que PostgreSQL est démarré et que la base de données existe"
    exit 1
fi

# Afficher l'état des migrations
echo "[5/5] État des migrations:"
python manage.py showmigrations

echo ""
echo "========================================"
echo "Tables créées avec succès!"
echo "========================================"
echo ""
echo "Prochaines étapes:"
echo "1. Créer un superutilisateur: python manage.py createsuperuser"
echo "2. Initialiser le programme DESMFMC: python manage.py init_programme_desmfmc_detaille"
echo ""

