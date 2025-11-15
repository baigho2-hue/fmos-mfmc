from django.apps import AppConfig


class UtilisateursConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.utilisateurs'

    def ready(self):
        """
        Corrige une incompatibilité entre Django 4.2 et Python 3.14.

        Python 3.14 modifie le comportement de copy.copy() appliqué aux objets
        super(), ce qui provoque l'exception :
        AttributeError: 'super' object has no attribute 'dicts'
        lors du rendu de l'admin.

        On remplace donc la méthode BaseContext.__copy__ par une version
        équivalente qui n'utilise plus copy(super()).
        """
        from django.template import context as django_context

        if getattr(django_context.BaseContext.__copy__, "_patched_for_py314", False):
            return

        def _basecontext_copy(self):
            duplicate = object.__new__(self.__class__)
            duplicate.__dict__ = self.__dict__.copy()
            duplicate.dicts = self.dicts[:]
            return duplicate

        _basecontext_copy._patched_for_py314 = True
        django_context.BaseContext.__copy__ = _basecontext_copy
