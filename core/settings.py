# core/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

# Répertoire de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Sécurité et debug
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# CSRF trusted origins (important pour Render/production)
CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'https://fmos-mfmc.onrender.com'
).split(',')

# Auth user personnalisé
AUTH_USER_MODEL = 'utilisateurs.Utilisateur'

# Configuration de l'authentification
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Mes apps
    'apps.admissions',
    'apps.communications',
    'apps.evaluations',
    'apps.extras',
    'apps.procedurier',
    'apps.utilisateurs',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Pour servir les fichiers statiques en production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLs racines
ROOT_URLCONF = 'core.urls'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],  # ici Django cherchera index.html
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.navigation_menu',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'core.wsgi.application'

# Base de données PostgreSQL
# Si DATABASE_URL existe (Railway, Render, etc.), l'utiliser
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    
    # Récupérer l'URL de la base de données
    database_url = os.environ.get('DATABASE_URL', '')
    
    # Pour Render PostgreSQL, configuration SSL robuste
    if 'render.com' in database_url:
        # Les URLs internes Render (commencent par dpg-) n'ont PAS besoin de SSL
        # Les URLs externes nécessitent SSL
        
        # Détecter si c'est une URL interne (contient dpg-)
        is_internal = 'dpg-' in database_url
        
        if is_internal:
            # URL interne : Retirer sslmode de l'URL si présent (pas besoin de SSL)
            if 'sslmode' in database_url:
                import re
                database_url = re.sub(r'[?&]sslmode=[^&]*', '', database_url)
                # Nettoyer les ? ou & en double
                database_url = database_url.replace('??', '?').replace('&&', '&')
                if database_url.endswith('?') or database_url.endswith('&'):
                    database_url = database_url[:-1]
            
            # Parser l'URL
            db_config = dj_database_url.parse(database_url)
            
            # Pas d'options SSL pour les URLs internes
            db_config['OPTIONS'] = {
                'connect_timeout': 10,
            }
        else:
            # URL externe : Utiliser SSL avec mode prefer (plus flexible)
            if 'sslmode' not in database_url:
                if '?' not in database_url:
                    database_url += '?sslmode=prefer'
                else:
                    database_url += '&sslmode=prefer'
            
            db_config = dj_database_url.parse(database_url)
            db_config['OPTIONS'] = {
                'sslmode': 'prefer',  # Plus flexible que 'require'
                'connect_timeout': 10,
            }
        
        # Réutiliser les connexions pour éviter les fermetures inattendues
        db_config['CONN_MAX_AGE'] = 600
    else:
        # Pour les autres providers (Railway, etc.)
        db_config = dj_database_url.parse(database_url)
    
    # Forcer l'utilisation de SQLite en développement local si souhaité
    # ou si la connexion à Supabase échoue
    USE_SQLITE = os.getenv('USE_SQLITE', 'True') == 'True'
    
    if USE_SQLITE:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    else:
        DATABASES = {
            'default': db_config
        }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalisation
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Bamako'
USE_I18N = True
USE_TZ = True

# Fichiers statiques et médias
STATIC_URL = '/static/'
# Créer le dossier static s'il n'existe pas (pour éviter les erreurs de collectstatic)
static_dir = BASE_DIR / 'static'
if not static_dir.exists():
    static_dir.mkdir(parents=True, exist_ok=True)
STATICFILES_DIRS = [static_dir]  # ton dossier static à la racine
STATIC_ROOT = BASE_DIR / 'staticfiles'    # dossier pour collectstatic

# Configuration WhiteNoise pour servir les fichiers statiques en production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Messages
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuration Email
# En développement, utiliser la console pour les emails (affichage dans le terminal)
# En production, utiliser SMTP
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # Les emails seront affichés dans la console au lieu d'être envoyés
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@fmos-mfmc.ml')

# Email par défaut (utilisé même en mode console)
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@fmos-mfmc.ml')

# Configuration du logging - éviter de logger les données sensibles
# Note: Django ne log pas automatiquement les mots de passe dans les requêtes POST
# mais cette configuration limite le logging pour plus de sécurité
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',  # Ne logger que les erreurs, pas les requêtes normales
            'propagate': False,
        },
        # Désactiver le logging détaillé des requêtes qui pourraient contenir des mots de passe
        'django.server': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}