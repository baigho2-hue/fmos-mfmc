# core/startup.py
"""
Script d'initialisation automatique au démarrage de l'application
Exécute les migrations automatiquement si nécessaire
"""
import os
import sys
from django.core.management import call_command
from django.db import connection

def run_startup_tasks():
    """Exécute les tâches d'initialisation au démarrage"""
    # Vérifier si on doit ignorer les tâches de démarrage
    if os.environ.get('SKIP_STARTUP', 'False') == 'True':
        print("⏭️  Tâches de démarrage ignorées (SKIP_STARTUP=True)")
        return
    
    try:
        # Vérifier la connexion à la base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Connexion à la base de données OK")
        
        # Appliquer les migrations automatiquement
        print("🔄 Application des migrations...")
        call_command('migrate', '--noinput', verbosity=1)
        print("✅ Migrations appliquées")
        
        # Vérifier si un superutilisateur existe
        try:
            from apps.utilisateurs.models import Utilisateur
            superuser_count = Utilisateur.objects.filter(is_superuser=True).count()
            if superuser_count == 0:
                print("⚠️  Aucun superutilisateur trouvé.")
                print("   Créez-en un via l'interface setup : /setup/?token=VOTRE_TOKEN")
            else:
                print(f"✅ {superuser_count} superutilisateur(s) trouvé(s)")
        except Exception as e:
            print(f"⚠️  Impossible de vérifier les superutilisateurs : {e}")
        
        # Vérifier si le programme DESMFMC est initialisé
        try:
            from apps.utilisateurs.models_programme_desmfmc import JalonProgramme
            jalon_count = JalonProgramme.objects.count()
            if jalon_count == 0:
                print("⚠️  Programme DESMFMC non initialisé.")
                print("   Initialisez-le via l'interface setup : /setup/?token=VOTRE_TOKEN")
            else:
                print(f"✅ Programme DESMFMC initialisé ({jalon_count} jalons)")
        except Exception as e:
            print(f"⚠️  Impossible de vérifier le programme DESMFMC : {e}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        # Ne pas bloquer le démarrage de l'application
        import traceback
        traceback.print_exc()

