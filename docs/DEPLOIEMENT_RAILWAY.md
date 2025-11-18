# 🚀 Guide de Déploiement sur Railway - Étape par Étape

## 📋 Étape 1 : Préparer votre projet localement

### 1.1 Vérifier que tout fonctionne localement

```bash
# Activer votre environnement virtuel (si vous en avez un)
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Vérifier que les migrations sont à jour
python manage.py migrate

# Tester que le serveur démarre
python manage.py runserver
```

### 1.2 Créer un fichier .env.example (pour référence)

Créez un fichier `.env.example` à la racine avec :

```env
SECRET_KEY=votre-clé-secrète-très-longue
DEBUG=False
ALLOWED_HOSTS=votre-domaine.railway.app
DB_NAME=fmos_mfmc
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app
DEFAULT_FROM_EMAIL=noreply@fmos-mfmc.ml
```

**⚠️ Important :** Ne commitez JAMAIS le fichier `.env` réel !

### 1.3 Vérifier que votre code est sur GitHub

```bash
# Vérifier le statut Git
git status

# Si vous avez des modifications non commitées
git add .
git commit -m "Préparation pour déploiement Railway"

# Vérifier que vous avez un repository distant
git remote -v

# Si vous n'avez pas de repository GitHub, créez-en un sur github.com
# Puis ajoutez-le :
# git remote add origin https://github.com/votre-username/fmos-mfmc.git
# git push -u origin main
```

---

## 🌐 Étape 2 : Créer un compte Railway

1. Allez sur **https://railway.app**
2. Cliquez sur **"Start a New Project"** ou **"Login"**
3. Connectez-vous avec votre compte GitHub (recommandé)

---

## 🏗️ Étape 3 : Créer un nouveau projet sur Railway

1. Dans Railway Dashboard, cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Autorisez Railway à accéder à vos repositories GitHub si demandé
4. Sélectionnez votre repository `fmos-mfmc`
5. Railway va automatiquement détecter Django et commencer le déploiement

---

## 🗄️ Étape 4 : Créer une base de données PostgreSQL

1. Dans votre projet Railway, cliquez sur **"+ New"**
2. Sélectionnez **"Database"** > **"Add PostgreSQL"**
3. Railway créera automatiquement une base de données PostgreSQL
4. Notez les informations de connexion qui apparaissent

---

## ⚙️ Étape 5 : Configurer les variables d'environnement

1. Dans votre projet Railway, cliquez sur votre service web (celui avec Django)
2. Allez dans l'onglet **"Variables"**
3. Ajoutez les variables suivantes une par une :

### Variables essentielles :

```
SECRET_KEY = gutp!g9gqbuhq9)514-r*tkds6v3p0r(myo0rvgmgc0svu&0-i
DEBUG = False
```

### Variables de base de données (depuis PostgreSQL) :

Railway génère automatiquement une variable `DATABASE_URL`. Vous devez créer ces variables séparées :

```
DB_NAME = (valeur depuis DATABASE_URL ou votre nom de DB)
DB_USER = (valeur depuis DATABASE_URL)
DB_PASSWORD = (valeur depuis DATABASE_URL)
DB_HOST = (valeur depuis DATABASE_URL)
DB_PORT = 5432
```

**Astuce :** Pour obtenir les valeurs depuis `DATABASE_URL`, Railway l'affiche dans les variables. Le format est :
`postgresql://user:password@host:port/dbname`

### Variables de domaine :

```
ALLOWED_HOSTS = votre-projet.railway.app
```

Railway vous donnera une URL comme `votre-projet.railway.app`. Utilisez-la ici.

### Variables d'email (optionnel pour l'instant) :

```
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = votre_email@gmail.com
EMAIL_HOST_PASSWORD = votre_mot_de_passe_app_gmail
DEFAULT_FROM_EMAIL = noreply@fmos-mfmc.ml
```

**Note :** Pour Gmail, vous devez créer un "Mot de passe d'application" dans les paramètres de sécurité de votre compte Google.

---

## 🔄 Étape 6 : Configurer la connexion à la base de données

Railway utilise `DATABASE_URL` par défaut. Vous devez modifier `core/settings.py` pour utiliser cette variable si elle existe.

Ajoutez ceci dans `core/settings.py` après la ligne `load_dotenv()` :

```python
# Configuration base de données pour Railway
import dj_database_url

# Si DATABASE_URL existe (Railway), l'utiliser
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    # Sinon, utiliser la configuration normale
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
```

Et ajoutez `dj-database-url` à `requirements.txt` :

```
dj-database-url>=2.1.0
```

---

## 🚀 Étape 7 : Déployer

1. Railway déploie automatiquement à chaque push sur votre branche principale
2. Si vous avez fait des modifications, poussez-les :
   ```bash
   git add .
   git commit -m "Configuration pour Railway"
   git push origin main
   ```
3. Railway va automatiquement détecter le push et redéployer

---

## ✅ Étape 8 : Appliquer les migrations

1. Dans Railway Dashboard, cliquez sur votre service web
2. Allez dans l'onglet **"Deployments"**
3. Cliquez sur le dernier déploiement
4. Cliquez sur **"View Logs"**
5. Ouvrez un terminal Railway en cliquant sur l'icône terminal
6. Exécutez :

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

---

## 🌍 Étape 9 : Accéder à votre site

1. Dans Railway Dashboard, cliquez sur votre service web
2. Cliquez sur l'onglet **"Settings"**
3. Sous **"Domains"**, vous verrez votre URL Railway (ex: `votre-projet.railway.app`)
4. Cliquez sur cette URL pour accéder à votre site !

---

## 🔧 Étape 10 : Configurer un domaine personnalisé (optionnel)

1. Dans Railway Dashboard > Settings > Domains
2. Cliquez sur **"Custom Domain"**
3. Entrez votre domaine (ex: `fmos-mfmc.ml`)
4. Suivez les instructions pour configurer les DNS

---

## 🐛 Dépannage

### Le site affiche une erreur 500

1. Vérifiez les logs dans Railway Dashboard > Deployments > View Logs
2. Vérifiez que toutes les variables d'environnement sont correctes
3. Vérifiez que `DEBUG=False` et que `SECRET_KEY` est définie

### Les fichiers statiques ne se chargent pas

1. Vérifiez que `collectstatic` a été exécuté
2. Vérifiez que WhiteNoise est dans le middleware (déjà fait)
3. Vérifiez les logs pour les erreurs

### Erreur de base de données

1. Vérifiez que la base PostgreSQL est créée et connectée
2. Vérifiez que les migrations sont appliquées
3. Vérifiez les variables `DATABASE_URL` ou `DB_*`

### Le déploiement échoue

1. Vérifiez les logs de build dans Railway
2. Vérifiez que `requirements.txt` est correct
3. Vérifiez que `Procfile` existe et est correct

---

## 📝 Checklist finale

- [ ] Code poussé sur GitHub
- [ ] Projet créé sur Railway
- [ ] Base PostgreSQL créée
- [ ] Variables d'environnement configurées
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Site accessible via l'URL Railway
- [ ] Fichiers statiques chargés correctement
- [ ] Admin Django accessible

---

## 🎉 Félicitations !

Votre site est maintenant déployé sur Railway ! 

**Prochaines étapes :**
- Configurer un domaine personnalisé
- Configurer les emails pour la production
- Mettre en place des sauvegardes automatiques
- Configurer un monitoring

