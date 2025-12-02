# core/urls.py
"""
URLs principales - Organisation modulaire
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views, views_setup

# Importer les fichiers d'URLs organisés
from . import urls_public, urls_auth, urls_etudiant, urls_enseignant, urls_administration, urls_modules

urlpatterns = [
    # Admin Django
    path('admin/', admin.site.urls),
    
    # Pages publiques
    *urls_public.urlpatterns,
    
    # Authentification
    *urls_auth.urlpatterns,
    
    # Espace étudiant
    *urls_etudiant.urlpatterns,
    
    # Espace enseignant
    *urls_enseignant.urlpatterns,
    
    # Administration
    *urls_administration.urlpatterns,
    
    # Modules (apps et fonctionnalités spécialisées)
    *urls_modules.urlpatterns,
    
    # ⚠️ VUES TEMPORAIRES POUR CONFIGURATION RENDER - À SUPPRIMER APRÈS CONFIGURATION
    path('setup/', views_setup.setup_dashboard, name='setup_dashboard'),
    path('setup/migrate/', views_setup.setup_migrate, name='setup_migrate'),
    path('setup/create-superuser/', views_setup.setup_create_superuser, name='setup_create_superuser'),
    path('setup/init-programme/', views_setup.setup_init_programme, name='setup_init_programme'),
    path('setup/status/', views_setup.setup_status, name='setup_status'),
]

# Ajouter les vues de formation pour éviter les erreurs Reverse
formation_vues = [
    'desmfmc', 'sante_communautaire', 'recherche', 'echographie_base',
    'pedagogie_sante', 'autres_programmes',
    'logiciels_analyse_certif', 'logiciels_analyse_noncertif',
    'base_pedagogie', 'cours_med6', 'habilites_cliniques'
]

for vue in formation_vues:
    if hasattr(views, vue):
        urlpatterns.append(path(f'formations/{vue}/', getattr(views, vue), name=vue))

# Servir les fichiers statiques et media en debug
if settings.DEBUG:
    # En développement, servir depuis STATICFILES_DIRS (dossier static)
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Handlers d'erreurs
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
