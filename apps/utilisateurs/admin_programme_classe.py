# apps/utilisateurs/admin_programme_classe.py
"""
Admin personnalisé pour afficher la structure complète du programme par classe
Compétences → Jalons → Cours → Leçons
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models_formation import Classe, Competence, CompetenceJalon, Cours, Lecon


class LeconInline(admin.TabularInline):
    """Inline pour afficher les leçons d'un cours"""
    model = Lecon
    extra = 0
    fields = ('numero', 'titre', 'duree_heures', 'ordre', 'actif')
    readonly_fields = ('numero', 'titre', 'duree_heures', 'ordre')
    can_delete = False
    show_change_link = True
    
    def has_add_permission(self, request, obj=None):
        return False


class CoursInline(admin.TabularInline):
    """Inline pour afficher les cours liés à un jalon"""
    model = Cours.jalons_competence.through
    extra = 0
    verbose_name = "Cours"
    verbose_name_plural = "Cours associés"
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('cours')


class CompetenceJalonInline(admin.TabularInline):
    """Inline pour afficher les jalons d'une compétence"""
    model = CompetenceJalon
    extra = 0
    fields = ('titre', 'classe', 'ordre', 'actif')
    readonly_fields = ('titre', 'classe', 'ordre')
    can_delete = False
    show_change_link = True
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Classe)
class ClasseProgrammeAdmin(admin.ModelAdmin):
    """Admin pour afficher la structure complète du programme par classe"""
    list_display = ('code', 'nom', 'formation', 'annee', 'get_programme_summary', 'actif')
    list_filter = ('formation', 'annee', 'actif')
    search_fields = ('code', 'nom', 'formation__nom')
    readonly_fields = (
        'get_programme_complet',
        'get_statistiques',
    )
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('formation', 'nom', 'code', 'annee', 'description', 'date_debut', 'date_fin', 'effectif_max', 'responsable', 'actif')
        }),
        ('Structure du programme', {
            'fields': ('get_programme_complet',),
            'classes': ('wide',),
        }),
        ('Statistiques', {
            'fields': ('get_statistiques',),
            'classes': ('collapse',),
        }),
    )
    
    def get_programme_summary(self, obj):
        """Affiche un résumé du programme dans la liste"""
        competences_count = Competence.objects.filter(
            jalons_competence__classe=obj
        ).distinct().count()
        jalons_count = CompetenceJalon.objects.filter(classe=obj).count()
        cours_count = Cours.objects.filter(classe=obj).count()
        lecons_count = Lecon.objects.filter(cours__classe=obj).count()
        
        return format_html(
            '<strong>{} compétences</strong> · {} jalons · {} cours · {} leçons',
            competences_count, jalons_count, cours_count, lecons_count
        )
    get_programme_summary.short_description = 'Programme'
    
    def get_statistiques(self, obj):
        """Affiche les statistiques détaillées"""
        competences = Competence.objects.filter(
            jalons_competence__classe=obj
        ).distinct()
        jalons = CompetenceJalon.objects.filter(classe=obj)
        cours = Cours.objects.filter(classe=obj)
        lecons = Lecon.objects.filter(cours__classe=obj)
        
        total_heures = sum(c.duree_heures or 0 for c in cours)
        total_heures_lecons = sum(l.duree_heures or 0 for l in lecons)
        
        html = f"""
        <div style="padding: 10px;">
            <h3>Statistiques du programme</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;"><strong>Compétences :</strong></td>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;">{competences.count()}</td>
                </tr>
                <tr>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;"><strong>Jalons :</strong></td>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;">{jalons.count()}</td>
                </tr>
                <tr>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;"><strong>Cours :</strong></td>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;">{cours.count()}</td>
                </tr>
                <tr>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;"><strong>Leçons :</strong></td>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;">{lecons.count()}</td>
                </tr>
                <tr>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;"><strong>Volume horaire (cours) :</strong></td>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;">{total_heures} heures</td>
                </tr>
                <tr>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;"><strong>Volume horaire (leçons) :</strong></td>
                    <td style="padding: 5px; border-bottom: 1px solid #ddd;">{total_heures_lecons} heures</td>
                </tr>
            </table>
        </div>
        """
        return mark_safe(html)
    get_statistiques.short_description = 'Statistiques'
    
    def get_programme_complet(self, obj):
        """Affiche la structure complète du programme : Compétences → Jalons → Cours → Leçons"""
        if not obj:
            return "Sélectionnez une classe pour voir le programme"
        
        # Récupérer toutes les compétences avec leurs jalons pour cette classe
        competences = Competence.objects.filter(
            jalons_competence__classe=obj
        ).distinct().order_by('libelle')
        
        if not competences.exists():
            return format_html(
                '<div style="padding: 20px; background-color: #f0f0f0; border-radius: 5px;">'
                '<p style="color: #666;">Aucune compétence définie pour cette classe.</p>'
                '<p>Créez des jalons de compétence pour cette classe pour voir la structure du programme.</p>'
                '</div>'
            )
        
        html_parts = ['<div style="font-family: Arial, sans-serif;">']
        
        for comp in competences:
            # Jalons de cette compétence pour cette classe
            jalons = CompetenceJalon.objects.filter(
                competence=comp,
                classe=obj
            ).order_by('ordre', 'titre')
            
            if not jalons.exists():
                continue
            
            # En-tête de la compétence
            comp_url = reverse('admin:utilisateurs_competence_change', args=[comp.pk])
            html_parts.append(f'''
                <div style="margin: 20px 0; padding: 15px; background-color: #e3f2fd; border-left: 4px solid #2196F3; border-radius: 4px;">
                    <h2 style="margin: 0 0 10px 0; color: #1976D2;">
                        <a href="{comp_url}" style="text-decoration: none; color: #1976D2;">
                            📚 {comp.libelle}
                        </a>
                    </h2>
                    <p style="margin: 5px 0; color: #555; font-size: 0.9em;">{comp.description[:200]}...</p>
                </div>
            ''')
            
            # Jalons
            for jalon in jalons:
                jalon_url = reverse('admin:utilisateurs_competencejalon_change', args=[jalon.pk])
                html_parts.append(f'''
                    <div style="margin: 10px 0 10px 30px; padding: 12px; background-color: #f5f5f5; border-left: 3px solid #4CAF50; border-radius: 3px;">
                        <h3 style="margin: 0 0 8px 0; color: #2E7D32; font-size: 1.1em;">
                            <a href="{jalon_url}" style="text-decoration: none; color: #2E7D32;">
                                🎯 {jalon.titre}
                            </a>
                        </h3>
                        <p style="margin: 5px 0; color: #666; font-size: 0.85em;">{jalon.description[:150]}...</p>
                ''')
                
                # Cours liés à ce jalon
                cours = Cours.objects.filter(
                    classe=obj,
                    jalons_competence=jalon
                ).distinct().order_by('ordre', 'titre')
                
                if cours.exists():
                    html_parts.append('<div style="margin: 10px 0 0 20px;">')
                    for cours_obj in cours:
                        cours_url = reverse('admin:utilisateurs_cours_change', args=[cours_obj.pk])
                        html_parts.append(f'''
                            <div style="margin: 8px 0; padding: 10px; background-color: #fff; border-left: 2px solid #FF9800; border-radius: 2px;">
                                <h4 style="margin: 0 0 5px 0; color: #F57C00; font-size: 1em;">
                                    <a href="{cours_url}" style="text-decoration: none; color: #F57C00;">
                                        📖 {cours_obj.titre}
                                    </a>
                                    <span style="color: #999; font-size: 0.85em; font-weight: normal;">
                                        ({cours_obj.duree_heures or 0} heures)
                                    </span>
                                </h4>
                        ''')
                        
                        # Leçons de ce cours
                        lecons = Lecon.objects.filter(
                            cours=cours_obj
                        ).order_by('numero', 'ordre')
                        
                        if lecons.exists():
                            html_parts.append('<ul style="margin: 5px 0 0 0; padding-left: 20px; list-style-type: none;">')
                            for lecon in lecons:
                                lecon_url = reverse('admin:utilisateurs_lecon_change', args=[lecon.pk])
                                html_parts.append(f'''
                                    <li style="margin: 3px 0; color: #666; font-size: 0.9em;">
                                        <a href="{lecon_url}" style="text-decoration: none; color: #666;">
                                            📝 Leçon {lecon.numero}: {lecon.titre}
                                        </a>
                                        {f"({lecon.duree_heures}h)" if lecon.duree_heures else ""}
                                    </li>
                                ''')
                            html_parts.append('</ul>')
                        
                        html_parts.append('</div>')
                    html_parts.append('</div>')
                else:
                    html_parts.append('<p style="margin: 5px 0 0 20px; color: #999; font-style: italic; font-size: 0.85em;">Aucun cours associé</p>')
                
                html_parts.append('</div>')
        
        html_parts.append('</div>')
        
        return mark_safe(''.join(html_parts))
    get_programme_complet.short_description = 'Structure complète du programme'
    
    class Media:
        css = {
            'all': ('admin/css/programme_classe.css',)
        }

