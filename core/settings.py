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
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost,fmos-mfmc.onrender.com').split(',')

# CSRF et Proxy (important pour Render/production)
CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    'https://fmos-mfmc.onrender.com'
).split(',')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

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

# Configuration des bases de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Base de données
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    database_url = os.environ.get('DATABASE_URL')
    
    # Configuration via dj-database-url
    # Forcer SSL si c'est une connexion externe Render
    db_config = dj_database_url.config(
        default=database_url,
        conn_max_age=600,
        conn_health_checks=True,
    )
    
    # Si c'est Render, on ajuste les options SSL
    if 'render.com' in database_url and 'sslmode' not in database_url:
        if 'dpg-' in database_url:
            # Pour les URLs Render, on préfère sslmode=prefer pour la compatibilité
            db_config['OPTIONS'] = {'sslmode': 'prefer'}
    
    # Forcer l'utilisation de SQLite en développement local si souhaité
    USE_SQLITE = os.getenv('USE_SQLITE', 'False') == 'True'
    
    if not USE_SQLITE:
        DATABASES = {'default': db_config}

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
# En développement, utiliser la console par défaut, sauf si EMAIL_BACKEND est spécifié
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend')

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
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