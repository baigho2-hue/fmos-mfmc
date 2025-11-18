# 🎨 Déploiement Gratuit sur Render

## 🎯 Pourquoi Render ?

Votre compte Railway est limité aux bases de données uniquement. **Render** offre un plan gratuit qui permet de déployer des applications Django !

---

## ✅ Avantages de Render

- ✅ **Gratuit** : Plan gratuit permanent
- ✅ **Déploiement automatique** depuis GitHub
- ✅ **HTTPS** : Certificat SSL automatique
- ✅ **Base de données** : Peut créer PostgreSQL gratuitement
- ✅ **Simple** : Interface intuitive

---

## 📋 ÉTAPE 1 : Créer un compte Render

1. Allez sur **https://render.com**
2. Cliquez sur **"Get Started for Free"**
3. Connectez-vous avec **GitHub** (recommandé)
4. Autorisez Render à accéder à votre compte GitHub

---

## 📦 ÉTAPE 2 : Créer un nouveau Web Service

1. Dans Render, cliquez sur **"New +"** (en haut à droite)
2. Sélectionnez **"Web Service"**
3. Connectez votre dépôt GitHub :
   - Cliquez sur **"Connect account"** si nécessaire
   - Sélectionnez votre dépôt **`fmos-mfmc`**
   - Cliquez sur **"Connect"**

---

## ⚙️ ÉTAPE 3 : Configurer le Web Service

> **✅ Bonne nouvelle** : Votre projet est déjà prêt pour Render ! Les configurations nécessaires (WhiteNoise, dj-database-url, gunicorn) sont déjà dans `requirements.txt` et `core/settings.py`. Vous avez aussi un `Procfile` et un `runtime.txt` qui facilitent le déploiement.

Remplissez le formulaire :

### Informations de base :
- **Name** : `fmos-mfmc` (ou le nom que vous voulez)
- **Region** : Choisissez la région la plus proche (ex: `Frankfurt` pour l'Europe)
- **Branch** : `main` (ou `master`)

### Build & Start :
- **Build Command** : 
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Start Command** : 
  ```
  gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
  ```

### Plan :
- Sélectionnez **"Free"** (plan gratuit)

---

## 🗄️ ÉTAPE 4 : Créer une Base de Données PostgreSQL

1. Dans Render, cliquez sur **"New +"**
2. Sélectionnez **"PostgreSQL"**
3. Configurez :
   - **Name** : `fmos-mfmc-db`
   - **Database** : `fmos_mfmc`
   - **User** : `fmos_mfmc_user`
   - **Region** : Même région que votre web service
   - **Plan** : **"Free"**
4. Cliquez sur **"Create Database"**

### Obtenir l'URL de connexion :

1. Une fois la base créée, cliquez dessus
2. Dans **"Connections"**, vous verrez **"Internal Database URL"**
3. **Copiez cette URL** - elle ressemble à :
   ```
   postgresql://fmos_mfmc_user:motdepasse@dpg-xxxxx-a.frankfurt-postgres.render.com/fmos_mfmc
   ```

---

## 🔧 ÉTAPE 5 : Configurer les Variables d'Environnement

Dans votre **Web Service** > **Environment** :

1. Cliquez sur **"Add Environment Variable"**
2. Ajoutez ces variables une par une :

### Variable 1 : SECRET_KEY
- **Key** : `SECRET_KEY`
- **Value** : (générez-en une nouvelle, voir ci-dessous)

### Variable 2 : DEBUG
- **Key** : `DEBUG`
- **Value** : `False`

### Variable 3 : ALLOWED_HOSTS
- **Key** : `ALLOWED_HOSTS`
- **Value** : `votre-app.onrender.com`

### Variable 4 : DATABASE_URL
- **Key** : `DATABASE_URL`
- **Value** : (l'URL que vous avez copiée depuis PostgreSQL)

> **Note** : Le projet est déjà configuré pour utiliser automatiquement `DATABASE_URL` avec `dj-database-url`. Une fois cette variable définie, la connexion à la base de données sera automatiquement configurée.

### Exemple de configuration complète :

Voici un exemple de toutes les variables d'environnement à configurer :

```
ALLOWED_HOSTS=fmos-mfmc.onrender.com
DATABASE_URL=postgresql://fmos_mfmc_user:motdepasse@dpg-xxxxx-a.frankfurt-postgres.render.com/fmos_mfmc
DEBUG=False
SECRET_KEY=b3576260c5407de19fd66425c756f9f4
```

### Générer une SECRET_KEY :

Dans votre terminal local :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiez la clé générée et utilisez-la pour la variable `SECRET_KEY`.

---

## 🚀 ÉTAPE 6 : Déployer

1. Cliquez sur **"Create Web Service"**
2. Render va commencer à déployer votre application
3. Attendez que le déploiement soit terminé (2-5 minutes)
4. Vous verrez votre URL : `https://votre-app.onrender.com`

---

## 📝 ÉTAPE 7 : Configurer les Migrations (Post Deploy)

Dans Render, vous pouvez configurer une commande post-déploiement :

1. Allez dans votre Web Service > **"Settings"**
2. Cherchez **"Post Deploy Command"** ou **"Deploy Hook"**
3. Ajoutez :
   ```
   python manage.py migrate --noinput
   ```

**Si vous ne trouvez pas cette option**, pas de problème ! Vous pouvez lancer les migrations manuellement après le déploiement.

---

## 👤 ÉTAPE 8 : Créer un Superutilisateur

Une fois déployé :

1. Dans Render, allez dans votre Web Service
2. Cliquez sur **"Shell"** (en haut à droite)
3. Dans le terminal qui s'ouvre, exécutez :
   ```bash
   python manage.py createsuperuser
   ```
4. Entrez les informations du superutilisateur

---

## ⚙️ ÉTAPE 9 : Configuration Post-Déploiement

Maintenant que votre site est déployé sur `fmos-mfmc.onrender.com`, voici les étapes pour le configurer complètement :

### 📋 Vérifier les Variables d'Environnement

1. Dans Render, allez dans votre **Web Service** > **Environment**
2. Vérifiez que toutes ces variables sont définies :
   - ✅ `SECRET_KEY` : Une clé secrète générée
   - ✅ `DEBUG` : `False` (pour la production)
   - ✅ `ALLOWED_HOSTS` : `fmos-mfmc.onrender.com`
   - ✅ `DATABASE_URL` : L'URL de votre base PostgreSQL

### 🗄️ Appliquer les Migrations

1. Dans Render, allez dans votre **Web Service**
2. Cliquez sur **"Shell"** (en haut à droite)
3. Exécutez les migrations :
   ```bash
   python manage.py migrate
   ```
4. Vérifiez l'état des migrations :
   ```bash
   python manage.py showmigrations
   ```

### 👤 Créer un Superutilisateur

Dans le même Shell, créez votre compte administrateur :

```bash
python manage.py createsuperuser
```

Entrez :
- **Username** : (votre nom d'utilisateur admin)
- **Email** : (votre email)
- **Password** : (un mot de passe fort)

> **Note** : Vous pouvez aussi utiliser la commande personnalisée :
> ```bash
> python manage.py creer_superuser
> ```

### 📚 Initialiser le Programme DESMFMC

Pour initialiser la structure du programme de formation :

```bash
# Structure de base
python manage.py init_programme_desmfmc

# Structure détaillée (recommandé)
python manage.py init_programme_desmfmc_detaille
```

### ✅ Vérifier que Tout Fonctionne

1. **Accéder à l'admin Django** :
   - URL : `https://fmos-mfmc.onrender.com/admin/`
   - Connectez-vous avec votre superutilisateur

2. **Vérifier la base de données** :
   Dans le Shell Render :
   ```bash
   python manage.py shell
   ```
   Puis dans le shell Python :
   ```python
   from apps.utilisateurs.models import Utilisateur
   print(f"Nombre d'utilisateurs : {Utilisateur.objects.count()}")
   exit()
   ```

3. **Tester l'accès au site** :
   - Visitez `https://fmos-mfmc.onrender.com`
   - Vérifiez que la page se charge correctement

### 🔄 Commandes Utiles Post-Déploiement

Voici d'autres commandes que vous pourriez avoir besoin d'exécuter :

```bash
# Initialiser les coûts de formations
python manage.py init_couts_formations

# Créer des utilisateurs de test (si nécessaire)
python manage.py creer_utilisateurs_test

# Attribuer des classes DESMFMC
python manage.py attribuer_classes_desmfmc
```

### 📝 Notes Importantes

- **Shell Render** : Le Shell dans Render vous permet d'exécuter des commandes Django directement sur le serveur
- **Logs** : Consultez les logs dans Render > **Logs** pour voir les erreurs éventuelles
- **Redémarrage** : Après chaque modification de variables d'environnement, Render redémarre automatiquement l'application
- **Premier démarrage** : Si le site est en "spin down", le premier chargement peut prendre 30-60 secondes

---

## ⚠️ Limitations du Plan Gratuit Render

- **Spin down** : L'application s'endort après 15 minutes d'inactivité
- **Démarrage lent** : Premier chargement après inactivité peut prendre 30-60 secondes
- **512 MB RAM** : Suffisant pour Django
- **Domaine** : Sous-domaine `.onrender.com` gratuit

---

## ✅ Checklist de Déploiement

### Déploiement Initial
- [ ] Compte Render créé
- [ ] Web Service créé et configuré
- [ ] Base de données PostgreSQL créée
- [ ] Variables d'environnement configurées (4 variables)
- [ ] Déploiement lancé
- [ ] Site accessible sur `fmos-mfmc.onrender.com`

### Configuration Post-Déploiement
- [ ] Variables d'environnement vérifiées (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASE_URL)
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Superutilisateur créé (`python manage.py createsuperuser`)
- [ ] Programme DESMFMC initialisé (`python manage.py init_programme_desmfmc_detaille`)
- [ ] Accès à l'admin Django vérifié (`/admin/`)
- [ ] Site testé et fonctionnel

---

## 🆘 Résolution de Problèmes

### Problème : Le déploiement échoue

**Solution** :
1. Vérifiez les logs dans Render
2. Vérifiez que toutes les variables sont définies
3. Vérifiez que `DATABASE_URL` est correcte

### Problème : Erreur 500

**Solution** :
1. Activez temporairement `DEBUG=True` pour voir les erreurs
2. Vérifiez les logs dans Render
3. Vérifiez la connexion à la base de données

### Problème : Fichiers statiques ne se chargent pas

**Solution** :
1. Vérifiez que `collectstatic` est dans le Build Command
2. WhiteNoise est déjà configuré dans `core/settings.py` (ligne 41 et 113)
3. Vérifiez que `whitenoise>=6.6.0` est dans `requirements.txt` (déjà présent ✅)
4. Les fichiers statiques seront automatiquement servis par WhiteNoise en production

---

## 🎯 Prochaines Étapes

1. **Créez un compte Render**
2. **Créez un Web Service**
3. **Créez une base PostgreSQL**
4. **Configurez les variables**
5. **Déployez !**

---

**Render est parfait pour déployer votre application Django gratuitement ! 🚀**

