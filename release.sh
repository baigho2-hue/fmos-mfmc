#!/bin/bash
# Script exécuté par Railway avant le démarrage de l'application
# Applique les migrations et collecte les fichiers statiques

echo "🚀 Démarrage du script de release..."
echo "📦 Application des migrations..."
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "✅ Script de release terminé !"

