# apps/utilisateurs/templatetags/dict_filters.py
"""
Filtres de template personnalisés pour accéder aux dictionnaires
"""
from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    """Récupère un élément d'un dictionnaire par sa clé"""
    if dictionary is None:
        return None
    return dictionary.get(key)

