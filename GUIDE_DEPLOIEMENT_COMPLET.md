# 🚀 Guide de Déploiement Complet - FMOS-MFMC

## 📋 Prérequis

Avant de déployer, assurez-vous que :
- ✅ Votre code est sur GitHub
- ✅ Supabase est configuré avec votre base de données
- ✅ Tous les fichiers de configuration sont présents (`Procfile`, `runtime.txt`, `requirements.txt`)

---

## 🎯 Options de Déploiement

### Option 1 : Railway (Recommandé - Simple et gratuit)
### Option 2 : Render (Alternative gratuite)
### Option 3 : Heroku (Payant après essai gratuit)

---

## 🚂 DÉPLOIEMENT SUR RAILWAY

### Étape 1 : Créer un compte Railway

1. Allez sur https://railway.app
2. Cliquez sur **"Start a New Project"**
3. Connectez-vous avec GitHub

### Étape 2 : Créer un nouveau projet

1. Cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Choisissez votre dépôt `fmos-mfmc`
4. Railway va détecter automatiquement que c'est un projet Django

### Étape 3 : Configurer les variables d'environnement

Dans Railway, allez dans **Variables** et ajoutez :

```
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire-generee
DEBUG=False
ALLOWED_HOSTS=votre-app.railway.app,*.railway.app
DATABASE_URL=postgresql://postgres.VOTRE_PROJECT_ID:VOTRE_MOT_DE_PASSE@aws-1-eu-north-1.pooler.supabase.com:5432/postgres
```

**Important** :
- Générez une nouvelle `SECRET_KEY` pour la production (voir ci-dessous)
- Remplacez `votre-app.railway.app` par votre domaine Railway réel
- Utilisez votre URL Supabase complète

### Étape 4 : Générer une SECRET_KEY pour la production

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Étape 5 : Configurer le build

Railway détecte automatiquement Django, mais vous pouvez vérifier :

1. Allez dans **Settings** > **Build Command**
2. Assurez-vous que c'est vide (Railway le fait automatiquement)

### Étape 6 : Configurer la commande de démarrage

1. Allez dans **Settings** > **Start Command**
2. Railway devrait détecter automatiquement le `Procfile`
3. Sinon, ajoutez : `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`

### Étape 7 : Ajouter la commande de migration

1. Allez dans **Settings** > **Deploy**
2. Ajoutez dans **Post Deploy Command** :
   ```
   python manage.py migrate --noinput && python manage.py collectstatic --noinput
   ```

### Étape 8 : Déployer

1. Railway va automatiquement déployer votre application
2. Attendez que le déploiement soit terminé
3. Cliquez sur votre service pour obtenir l'URL

### Étape 9 : Créer un superutilisateur

Une fois déployé, créez un superutilisateur via le terminal Railway :

```bash
python manage.py createsuperuser
```

---

## 🎨 DÉPLOIEMENT SUR RENDER

### Étape 1 : Créer un compte Render

1. Allez sur https://render.com
2. Créez un compte gratuit
3. Connectez votre compte GitHub

### Étape 2 : Créer un nouveau Web Service

1. Cliquez sur **"New +"** > **"Web Service"**
2. Sélectionnez votre dépôt `fmos-mfmc`
3. Configurez :
   - **Name** : `fmos-mfmc`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command** : `gunicorn core.wsgi:application`

### Étape 3 : Configurer les variables d'environnement

Dans **Environment Variables**, ajoutez :

```
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
DEBUG=False
ALLOWED_HOSTS=votre-app.onrender.com
DATABASE_URL=postgresql://postgres.VOTRE_PROJECT_ID:VOTRE_MOT_DE_PASSE@aws-1-eu-north-1.pooler.supabase.com:5432/postgres
```

### Étape 4 : Configurer les migrations

Dans **Advanced** > **Post Deploy Command** :
```
python manage.py migrate --noinput
```

### Étape 5 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Render va déployer votre application
3. Attendez la fin du déploiement

---

## 🔧 CONFIGURATION AVANT DÉPLOIEMENT

### 1. Vérifier le Procfile

Votre `Procfile` doit contenir :
```
web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

### 2. Vérifier runtime.txt

Votre `runtime.txt` doit contenir :
```
python-3.11.0
```

### 3. Vérifier requirements.txt

Tous les packages nécessaires doivent être présents.

### 4. Mettre à jour settings.py pour la production

Assurez-vous que `settings.py` gère correctement `DATABASE_URL` :

```python
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
```

### 5. Générer une SECRET_KEY sécurisée

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## ✅ CHECKLIST DE DÉPLOIEMENT

Avant de déployer, vérifiez :

- [ ] Code poussé sur GitHub
- [ ] `Procfile` présent et correct
- [ ] `runtime.txt` présent avec la bonne version Python
- [ ] `requirements.txt` à jour
- [ ] `SECRET_KEY` générée pour la production
- [ ] `DEBUG=False` en production
- [ ] `ALLOWED_HOSTS` configuré avec votre domaine
- [ ] `DATABASE_URL` configurée avec Supabase
- [ ] WhiteNoise configuré dans `settings.py`
- [ ] Migrations prêtes à être appliquées

---

## 🧪 APRÈS LE DÉPLOIEMENT

### 1. Tester l'application

1. Visitez votre URL de déploiement
2. Vérifiez que la page d'accueil s'affiche
3. Testez l'accès à `/admin`

### 2. Créer un superutilisateur

Via le terminal de votre plateforme :
```bash
python manage.py createsuperuser
```

### 3. Vérifier les migrations

```bash
python manage.py showmigrations
```

### 4. Vérifier les fichiers statiques

Les fichiers statiques doivent être servis correctement via WhiteNoise.

---

## 🆘 RÉSOLUTION DE PROBLÈMES

### Problème : Application ne démarre pas

**Solution** :
1. Vérifiez les logs de déploiement
2. Vérifiez que `DATABASE_URL` est correcte
3. Vérifiez que `SECRET_KEY` est définie
4. Vérifiez que `ALLOWED_HOSTS` contient votre domaine

### Problème : Erreur 500

**Solution** :
1. Activez temporairement `DEBUG=True` pour voir les erreurs
2. Vérifiez les logs de l'application
3. Vérifiez la connexion à la base de données

### Problème : Fichiers statiques non chargés

**Solution** :
1. Vérifiez que `collectstatic` a été exécuté
2. Vérifiez que WhiteNoise est dans `MIDDLEWARE`
3. Vérifiez que `STATICFILES_STORAGE` est configuré

### Problème : Erreur de connexion à la base de données

**Solution** :
1. Vérifiez que `DATABASE_URL` est correcte
2. Vérifiez que Supabase accepte les connexions depuis votre plateforme
3. Vérifiez les restrictions IP dans Supabase

---

## 📝 NOTES IMPORTANTES

1. **Sécurité** : Ne commitez jamais votre `SECRET_KEY` ou votre `DATABASE_URL` dans Git
2. **Performance** : WhiteNoise compresse automatiquement les fichiers statiques
3. **Base de données** : Supabase a des limites sur le plan gratuit, surveillez votre utilisation
4. **Logs** : Consultez régulièrement les logs pour détecter les problèmes

---

## 🎯 PROCHAINES ÉTAPES

Une fois déployé :

1. Configurez un nom de domaine personnalisé (optionnel)
2. Configurez HTTPS (automatique sur Railway/Render)
3. Configurez les sauvegardes de base de données
4. Configurez le monitoring et les alertes

---

**Bon déploiement ! 🚀**

