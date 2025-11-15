# apps/utilisateurs/admin_widgets.py
"""
Widgets personnalisés pour l'admin Django
"""
from django import forms
from django.contrib.admin.widgets import AdminSelectWidget


class ClasseSelectWidget(forms.Select):
    """Widget personnalisé pour la sélection de classe avec affichage des cours"""
    template_name = 'admin/utilisateurs/widgets/classe_select.html'
    
    class Media:
        js = ('admin/js/classe_cours_filter.js',)


class CoursSelectWidget(forms.Select):
    """Widget personnalisé pour la sélection de cours filtré par classe"""
    template_name = 'admin/utilisateurs/widgets/cours_select.html'
    
    class Media:
        js = ('admin/js/classe_cours_filter.js',)

