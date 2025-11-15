#!/usr/bin/env python
"""
Script pour envoyer les alertes de leçons quotidiennement
Peut être exécuté via cron (Linux/Mac) ou Task Scheduler (Windows)
"""
import os
import sys
import django

# Ajouter le répertoire du projet au path Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fmos_mfmc.settings')
django.setup()

# Maintenant on peut importer et exécuter la commande
from django.core.management import call_command
from django.conf import settings

if __name__ == '__main__':
    try:
        print(f"[{settings.DATABASES['default']['NAME']}] Exécution de la commande envoyer_alertes_lecons...")
        call_command('envoyer_alertes_lecons')
        print("Commande exécutée avec succès.")
    except Exception as e:
        print(f"ERREUR lors de l'exécution de la commande: {e}")
        sys.exit(1)

