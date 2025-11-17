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

# Auth user personnalisé
AUTH_USER_MODEL = 'utilisateurs.Utilisateur'

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
    database_url = os.environ.get('DATABASE_URL')
    
    # Pour Render PostgreSQL, s'assurer que SSL est activé dans l'URL
    # Si l'URL ne contient pas déjà sslmode, l'ajouter
    if 'render.com' in database_url and 'sslmode' not in database_url:
        # Ajouter sslmode=require à l'URL si elle se termine par le nom de la base
        if '?' not in database_url:
            database_url += '?sslmode=require'
        else:
            database_url += '&sslmode=require'
    
    # Parser l'URL avec dj-database-url
    db_config = dj_database_url.parse(database_url)
    
    # Configuration SSL supplémentaire pour Render PostgreSQL
    # Render nécessite SSL pour les connexions
    if 'render.com' in db_config.get('HOST', ''):
        # Options SSL pour psycopg2
        db_config['OPTIONS'] = {
            'sslmode': 'require',
            'connect_timeout': 10,
        }
        # Réutiliser les connexions pour éviter les fermetures inattendues
        db_config['CONN_MAX_AGE'] = 600
    
    DATABASES = {
        'default': db_config
    }
else:
    # Sinon, utiliser la configuration normale avec variables d'environnement
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'fmos-mfmc'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'Yiriba_19'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
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
STATICFILES_DIRS = [BASE_DIR / 'static']  # ton dossier static à la racine
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