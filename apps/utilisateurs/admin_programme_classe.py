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
from .models import Utilisateur


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
    list_display = ('code', 'nom', 'formation', 'annee', 'get_etudiants_count', 'get_programme_summary', 'actif')
    list_filter = ('formation', 'annee', 'actif')
    search_fields = ('code', 'nom', 'formation__nom')
    readonly_fields = (
        'get_programme_complet',
        'get_statistiques',
        'get_etudiants_liste',
    )
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('formation', 'nom', 'code', 'annee', 'description', 'date_debut', 'date_fin', 'effectif_max', 'responsable', 'actif')
        }),
        ('Étudiants', {
            'fields': ('get_etudiants_liste',),
            'classes': ('wide',),
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
        if not obj:
            return "-"
        
        try:
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
        except Exception:
            return "-"
    get_programme_summary.short_description = 'Programme'
    
    def get_etudiants_count(self, obj):
        """Affiche le nombre d'étudiants dans la liste"""
        if not obj:
            return "-"
        
        try:
            count = Utilisateur.objects.filter(
                type_utilisateur='etudiant',
                classe__icontains=obj.nom,
                is_active=True
            ).count()
            
            if count == 0:
                return format_html('<span style="color: #dc3545;">0</span>')
            elif count >= obj.effectif_max:
                return format_html('<span style="color: #dc3545; font-weight: bold;">{}/{} ⚠️</span>', count, obj.effectif_max)
            else:
                return format_html('<span style="color: #28a745;">{}/{}</span>', count, obj.effectif_max)
        except Exception:
            return "-"
    get_etudiants_count.short_description = 'Étudiants'
    
    def get_etudiants_liste(self, obj):
        """Affiche la liste des étudiants de cette classe"""
        if not obj:
            return "Sélectionnez une classe pour voir les étudiants"
        
        try:
            # Récupérer les étudiants dont le champ classe contient le nom de cette classe
            etudiants = Utilisateur.objects.filter(
                type_utilisateur='etudiant',
                classe__icontains=obj.nom,
                is_active=True
            ).order_by('last_name', 'first_name', 'username')
            
            if not etudiants.exists():
                return format_html(
                    '<div style="padding: 20px; background-color: #fff3cd; border-radius: 5px; border: 1px solid #ffc107;">'
                    '<p style="margin: 0; color: #856404;"><strong>⚠️ Aucun étudiant trouvé pour cette classe.</strong></p>'
                    '<p style="margin: 10px 0 0 0; color: #856404;">'
                    'Les étudiants doivent avoir le nom de la classe ("{}") dans leur champ "Classe" pour apparaître ici.'
                    '</p>'
                    '<p style="margin: 10px 0 0 0; color: #856404;">'
                    'Vous pouvez modifier le champ "Classe" des étudiants dans <a href="{}">l\'administration des utilisateurs</a>.'
                    '</p>'
                    '</div>',
                    obj.nom,
                    reverse('admin:utilisateurs_utilisateur_changelist') + '?type_utilisateur__exact=etudiant'
                )
            
            html_parts = [
                '<div style="padding: 15px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 10px;">',
                f'<h3 style="margin: 0 0 15px 0; color: #005a9c;">📚 Étudiants ({etudiants.count()}/{obj.effectif_max})</h3>',
                '<table style="width: 100%; border-collapse: collapse; background: white;">',
                '<thead>',
                '<tr style="background-color: #005a9c; color: white;">',
                '<th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Nom</th>',
                '<th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Prénom</th>',
                '<th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Email</th>',
                '<th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Classe (champ)</th>',
                '<th style="padding: 10px; text-align: left; border: 1px solid #ddd;">Actions</th>',
                '</tr>',
                '</thead>',
                '<tbody>'
            ]
            
            for etudiant in etudiants:
                etudiant_url = reverse('admin:utilisateurs_utilisateur_change', args=[etudiant.pk])
                nom_complet = etudiant.get_full_name() or etudiant.username
                classe_etudiant = etudiant.classe or "(vide)"
                
                # Vérifier si le nom correspond exactement
                correspondance = "✅" if classe_etudiant == obj.nom else "⚠️"
                
                html_parts.append(f'''
                    <tr>
                        <td style="padding: 8px; border: 1px solid #ddd;">{etudiant.last_name or "-"}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{etudiant.first_name or "-"}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">{etudiant.email}</td>
                        <td style="padding: 8px; border: 1px solid #ddd;">
                            {correspondance} {classe_etudiant}
                        </td>
                        <td style="padding: 8px; border: 1px solid #ddd;">
                            <a href="{etudiant_url}" style="color: #005a9c; text-decoration: none;">✏️ Modifier</a>
                        </td>
                    </tr>
                ''')
            
            html_parts.extend([
                '</tbody>',
                '</table>',
                '</div>'
            ])
            
            return mark_safe(''.join(html_parts))
        except Exception as e:
            return format_html(
                '<div style="padding: 20px; background-color: #ffebee; border-radius: 5px; color: #c62828;">'
                f'<p>Erreur lors de la récupération des étudiants: {str(e)}</p>'
                '</div>'
            )
    get_etudiants_liste.short_description = 'Étudiants de la classe'
    
    def get_statistiques(self, obj):
        """Affiche les statistiques détaillées"""
        if not obj:
            return "Sélectionnez une classe pour voir les statistiques"
        
        try:
            competences = Competence.objects.filter(
                jalons_competence__classe=obj
            ).distinct()
            jalons = CompetenceJalon.objects.filter(classe=obj)
            cours = Cours.objects.filter(classe=obj)
            lecons = Lecon.objects.filter(cours__classe=obj)
            
            total_heures = sum(c.duree_heures or 0 for c in cours)
            total_heures_lecons = sum(l.duree_heures or 0 for l in lecons)
        except Exception as e:
            return f"Erreur lors du calcul des statistiques: {str(e)}"
        
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
        
        try:
            # Récupérer toutes les compétences avec leurs jalons pour cette classe
            competences = Competence.objects.filter(
                jalons_competence__classe=obj
            ).distinct().order_by('libelle')
        except Exception as e:
            return format_html(
                '<div style="padding: 20px; background-color: #ffebee; border-radius: 5px; color: #c62828;">'
                f'<p>Erreur lors de la récupération des compétences: {str(e)}</p>'
                '</div>'
            )
        
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
            try:
                comp_url = reverse('admin:utilisateurs_competence_change', args=[comp.pk])
            except Exception:
                comp_url = '#'
            
            comp_libelle = comp.libelle if comp.libelle else "Compétence sans libellé"
            comp_description = (comp.description[:200] + '...') if comp.description else "Aucune description"
            
            html_parts.append(f'''
                <div style="margin: 20px 0; padding: 15px; background-color: #e3f2fd; border-left: 4px solid #2196F3; border-radius: 4px;">
                    <h2 style="margin: 0 0 10px 0; color: #1976D2;">
                        <a href="{comp_url}" style="text-decoration: none; color: #1976D2;">
                            📚 {comp_libelle}
                        </a>
                    </h2>
                    <p style="margin: 5px 0; color: #555; font-size: 0.9em;">{comp_description}</p>
                </div>
            ''')
            
            # Jalons
            for jalon in jalons:
                try:
                    jalon_url = reverse('admin:utilisateurs_competencejalon_change', args=[jalon.pk])
                except Exception:
                    jalon_url = '#'
                
                jalon_titre = jalon.titre if jalon.titre else "Jalon sans titre"
                jalon_description = (jalon.description[:150] + '...') if jalon.description else "Aucune description"
                
                html_parts.append(f'''
                    <div style="margin: 10px 0 10px 30px; padding: 12px; background-color: #f5f5f5; border-left: 3px solid #4CAF50; border-radius: 3px;">
                        <h3 style="margin: 0 0 8px 0; color: #2E7D32; font-size: 1.1em;">
                            <a href="{jalon_url}" style="text-decoration: none; color: #2E7D32;">
                                🎯 {jalon_titre}
                            </a>
                        </h3>
                        <p style="margin: 5px 0; color: #666; font-size: 0.85em;">{jalon_description}</p>
                ''')
                
                # Cours liés à ce jalon
                cours = Cours.objects.filter(
                    classe=obj,
                    jalons_competence=jalon
                ).distinct().order_by('ordre', 'titre')
                
                if cours.exists():
                    html_parts.append('<div style="margin: 10px 0 0 20px;">')
                    for cours_obj in cours:
                        try:
                            cours_url = reverse('admin:utilisateurs_cours_change', args=[cours_obj.pk])
                        except Exception:
                            cours_url = '#'
                        
                        cours_titre = cours_obj.titre if cours_obj.titre else "Cours sans titre"
                        
                        html_parts.append(f'''
                            <div style="margin: 8px 0; padding: 10px; background-color: #fff; border-left: 2px solid #FF9800; border-radius: 2px;">
                                <h4 style="margin: 0 0 5px 0; color: #F57C00; font-size: 1em;">
                                    <a href="{cours_url}" style="text-decoration: none; color: #F57C00;">
                                        📖 {cours_titre}
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
                                try:
                                    lecon_url = reverse('admin:utilisateurs_lecon_change', args=[lecon.pk])
                                except Exception:
                                    lecon_url = '#'
                                
                                lecon_numero = lecon.numero if lecon.numero else "?"
                                lecon_titre = lecon.titre if lecon.titre else "Leçon sans titre"
                                
                                html_parts.append(f'''
                                    <li style="margin: 3px 0; color: #666; font-size: 0.9em;">
                                        <a href="{lecon_url}" style="text-decoration: none; color: #666;">
                                            📝 Leçon {lecon_numero}: {lecon_titre}
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

