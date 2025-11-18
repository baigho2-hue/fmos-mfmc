# Guide de Déploiement - Plateforme FMOS-MFMC

Ce guide vous explique comment déployer votre application Django sur différents services.

## 📋 Prérequis

- Python 3.8+
- Git installé
- Compte sur la plateforme de déploiement choisie
- Base de données PostgreSQL (locale ou cloud)

## 🔧 Préparation avant déploiement

### 1. Créer un fichier `.env` pour la production

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
# Sécurité
SECRET_KEY=votre-clé-secrète-très-longue-et-aléatoire
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# Base de données PostgreSQL
DB_NAME=fmos_mfmc
DB_USER=votre_utilisateur_db
DB_PASSWORD=votre_mot_de_passe_db
DB_HOST=localhost
DB_PORT=5432

# Email (pour la production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app
DEFAULT_FROM_EMAIL=noreply@fmos-mfmc.ml
```

**⚠️ Important :** Ne commitez JAMAIS le fichier `.env` dans Git ! Ajoutez-le au `.gitignore`.

### 2. Générer une SECRET_KEY sécurisée

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Mettre à jour requirements.txt

Assurez-vous que votre `requirements.txt` contient toutes les dépendances nécessaires :

```txt
Django>=4.2,<5.0
psycopg2-binary>=2.9
python-dotenv>=1.0
xhtml2pdf>=0.2.0
reportlab>=4.0
gunicorn>=21.2.0
whitenoise>=6.6.0
```

### 4. Créer un fichier `.gitignore`

Assurez-vous que votre `.gitignore` contient :

```
.env
*.pyc
__pycache__/
db.sqlite3
staticfiles/
media/
*.log
.DS_Store
venv/
env/
```

## 🚀 Option 1 : Déploiement sur Railway

Railway est une plateforme simple et rapide pour déployer des applications Django.

### Étapes :

1. **Créer un compte sur Railway** : https://railway.app

2. **Installer Railway CLI** (optionnel) :
```bash
npm install -g @railway/cli
railway login
```

3. **Créer un fichier `Procfile`** à la racine :
```
web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

4. **Créer un fichier `runtime.txt`** (si nécessaire) :
```
python-3.11.0
```

5. **Sur Railway Dashboard** :
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Connectez votre repository GitHub
   - Railway détectera automatiquement Django

6. **Configurer les variables d'environnement** :
   - Dans les settings du projet, ajoutez toutes les variables du fichier `.env`
   - Railway créera automatiquement une base de données PostgreSQL

7. **Déployer** :
   - Railway déploiera automatiquement à chaque push sur la branche principale
   - Votre site sera accessible via une URL Railway (ex: `votre-projet.railway.app`)

## 🌐 Option 2 : Déploiement sur Render

Render est une alternative populaire à Heroku.

### Étapes :

1. **Créer un compte sur Render** : https://render.com

2. **Créer un fichier `render.yaml`** à la racine :
```yaml
services:
  - type: web
    name: fmos-mfmc
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput
    startCommand: gunicorn core.wsgi:application
    envVars:
      - key: SECRET_KEY
        sync: false
      - key: DEBUG
        value: False
      - key: DATABASE_URL
        fromDatabase:
          name: fmos-mfmc-db
          property: connectionString
```

3. **Sur Render Dashboard** :
   - Cliquez sur "New +" > "Web Service"
   - Connectez votre repository GitHub
   - Render détectera automatiquement Django

4. **Créer une base de données PostgreSQL** :
   - Cliquez sur "New +" > "PostgreSQL"
   - Notez l'URL de connexion

5. **Configurer les variables d'environnement** dans les settings du service web

6. **Déployer** :
   - Render déploiera automatiquement
   - Votre site sera accessible via une URL Render

## 🖥️ Option 3 : Déploiement sur un VPS (Ubuntu/Debian)

Pour un contrôle total, vous pouvez déployer sur un VPS.

### Étapes :

1. **Préparer le serveur** :
```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Python et dépendances
sudo apt install python3-pip python3-venv postgresql nginx git -y

# Installer Gunicorn
pip3 install gunicorn
```

2. **Cloner le projet** :
```bash
cd /var/www
sudo git clone https://github.com/votre-username/fmos-mfmc.git
cd fmos-mfmc
```

3. **Créer un environnement virtuel** :
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Configurer PostgreSQL** :
```bash
sudo -u postgres psql
CREATE DATABASE fmos_mfmc;
CREATE USER fmos_user WITH PASSWORD 'votre_mot_de_passe';
ALTER ROLE fmos_user SET client_encoding TO 'utf8';
ALTER ROLE fmos_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE fmos_user SET timezone TO 'Africa/Bamako';
GRANT ALL PRIVILEGES ON DATABASE fmos_mfmc TO fmos_user;
\q
```

5. **Configurer Django** :
```bash
# Créer le fichier .env
nano .env
# Ajouter toutes les variables d'environnement

# Migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer un superutilisateur
python manage.py createsuperuser
```

6. **Configurer Gunicorn** :
```bash
# Créer le fichier de service systemd
sudo nano /etc/systemd/system/fmos-mfmc.service
```

Contenu du fichier :
```ini
[Unit]
Description=Gunicorn instance pour FMOS-MFMC
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/fmos-mfmc
Environment="PATH=/var/www/fmos-mfmc/venv/bin"
ExecStart=/var/www/fmos-mfmc/venv/bin/gunicorn --workers 3 --bind unix:/var/www/fmos-mfmc/fmos-mfmc.sock core.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Activer le service
sudo systemctl start fmos-mfmc
sudo systemctl enable fmos-mfmc
```

7. **Configurer Nginx** :
```bash
sudo nano /etc/nginx/sites-available/fmos-mfmc
```

Contenu :
```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;

    location /static/ {
        alias /var/www/fmos-mfmc/staticfiles/;
    }

    location /media/ {
        alias /var/www/fmos-mfmc/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/fmos-mfmc/fmos-mfmc.sock;
    }
}
```

```bash
# Activer le site
sudo ln -s /etc/nginx/sites-available/fmos-mfmc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

8. **Configurer SSL avec Let's Encrypt** :
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

## 📝 Checklist de déploiement

Avant de déployer, assurez-vous de :

- [ ] Avoir corrigé `manage.py` (DJANGO_SETTINGS_MODULE = 'core.settings')
- [ ] Avoir créé un fichier `.env` avec toutes les variables
- [ ] Avoir mis à jour `requirements.txt` avec `gunicorn` et `whitenoise`
- [ ] Avoir configuré `ALLOWED_HOSTS` dans les variables d'environnement
- [ ] Avoir mis `DEBUG=False` en production
- [ ] Avoir généré une `SECRET_KEY` sécurisée
- [ ] Avoir configuré la base de données PostgreSQL
- [ ] Avoir configuré l'envoi d'emails (SMTP)
- [ ] Avoir testé les migrations localement
- [ ] Avoir collecté les fichiers statiques

## 🔍 Vérifications post-déploiement

1. **Tester l'accès au site** : Vérifiez que le site est accessible
2. **Tester l'admin Django** : `/admin/`
3. **Vérifier les fichiers statiques** : CSS, JS, images
4. **Tester l'envoi d'emails** : Créer un compte utilisateur
5. **Vérifier les logs** : En cas d'erreur, consulter les logs

## 🐛 Dépannage

### Erreur 500
- Vérifier les logs du serveur
- Vérifier que `DEBUG=False` et que les variables d'environnement sont correctes
- Vérifier les permissions des fichiers

### Fichiers statiques non chargés
- Exécuter `python manage.py collectstatic --noinput`
- Vérifier la configuration de `STATIC_ROOT` et `STATIC_URL`
- Vérifier la configuration Nginx/serveur web

### Erreur de base de données
- Vérifier les variables d'environnement de la DB
- Vérifier que les migrations sont appliquées : `python manage.py migrate`
- Vérifier les permissions de l'utilisateur PostgreSQL

## 📚 Ressources supplémentaires

- [Documentation Django - Déploiement](https://docs.djangoproject.com/fr/4.2/howto/deployment/)
- [Documentation Gunicorn](https://docs.gunicorn.org/)
- [Documentation Nginx](https://nginx.org/en/docs/)

