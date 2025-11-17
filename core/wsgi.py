import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Exécuter les tâches d'initialisation au démarrage
# (migrations automatiques, vérifications, etc.)
try:
    from core.startup import run_startup_tasks
    run_startup_tasks()
except Exception as e:
    # Ne pas bloquer le démarrage si les tâches échouent
    print(f"⚠️  Erreur lors des tâches de démarrage : {e}")

application = get_wsgi_application()
