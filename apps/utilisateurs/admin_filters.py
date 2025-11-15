# apps/utilisateurs/admin_filters.py
"""
Filtres personnalisés pour l'admin Django
"""
from django.contrib import admin
from django.db.models import Count, Q
from apps.utilisateurs.models_formation import Classe


class ClasseFilter(admin.SimpleListFilter):
    """Filtre personnalisé pour filtrer les cours par classe avec affichage amélioré"""
    title = 'Classe'
    parameter_name = 'classe_filter'
    
    def lookups(self, request, model_admin):
        """Retourne la liste des classes disponibles avec leur formation"""
        classes = Classe.objects.filter(actif=True).select_related('formation').order_by('formation__nom', 'nom')
        lookups = []
        for classe in classes:
            label = f"{classe.nom} ({classe.formation.nom})" if classe.formation else classe.nom
            lookups.append((str(classe.id), label))
        return lookups
    
    def queryset(self, request, queryset):
        """Filtre le queryset selon la classe sélectionnée"""
        if self.value():
            try:
                return queryset.filter(classe_id=self.value())
            except ValueError:
                pass
        return queryset


class ClasseWithCoursFilter(admin.SimpleListFilter):
    """Filtre amélioré qui affiche aussi le nombre de cours par classe"""
    title = 'Classe'
    parameter_name = 'classe_cours'
    
    def lookups(self, request, model_admin):
        """Retourne la liste des classes avec le nombre de cours"""
        try:
            classes = Classe.objects.filter(actif=True).annotate(
                nombre_cours=Count('cours', filter=Q(cours__actif=True))
            ).select_related('formation').order_by('formation__nom', 'nom')
            
            lookups = []
            for classe in classes:
                formation_nom = classe.formation.nom if classe.formation else "Sans formation"
                label = f"{classe.nom} ({formation_nom}) - {classe.nombre_cours} cours"
                lookups.append((str(classe.id), label))
            return lookups
        except Exception:
            # En cas d'erreur, retourner une liste vide
            return []
    
    def queryset(self, request, queryset):
        """Filtre le queryset selon la classe sélectionnée"""
        if self.value():
            try:
                classe_id = int(self.value())
                return queryset.filter(classe_id=classe_id)
            except (ValueError, TypeError):
                pass
        return queryset

