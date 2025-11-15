from django.apps import AppConfig

class ExtrasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.extras"

    def ready(self):
        # Import local signals ici si besoin, mais PAS les modèles
        pass
 