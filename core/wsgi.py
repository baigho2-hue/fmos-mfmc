import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Désactivé pour économiser la mémoire sur le plan gratuit Render
# Les migrations sont appliquées dans le buildCommand de render.yaml
# Utilisez l'interface /setup/ pour l'initialisation manuelle
# try:
#     from core.startup import run_startup_tasks
#     run_startup_tasks()
# except Exception as e:
#     print(f"⚠️  Erreur lors des tâches de démarrage : {e}")

application = get_wsgi_application()
