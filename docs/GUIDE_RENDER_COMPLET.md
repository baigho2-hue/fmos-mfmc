# 🚀 Guide Complet de Déploiement sur Render

Ce guide vous accompagne étape par étape pour déployer votre application Django FMOS-MFMC sur Render.

---

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Méthode 1 : Déploiement Automatique avec render.yaml](#méthode-1--déploiement-automatique-avec-renderyaml)
3. [Méthode 2 : Déploiement Manuel](#méthode-2--déploiement-manuel)
4. [Configuration Post-Déploiement](#configuration-post-déploiement)
5. [Résolution de Problèmes](#résolution-de-problèmes)
6. [Optimisations](#optimisations)

---

## ✅ Prérequis

- Un compte GitHub avec votre projet `fmos-mfmc` poussé
- Un compte Render (gratuit) : [https://render.com](https://render.com)
- Les fichiers de configuration suivants présents dans votre projet :
  - ✅ `requirements.txt`
  - ✅ `Procfile`
  - ✅ `runtime.txt`
  - ✅ `render.yaml` (optionnel, pour déploiement automatique)

---

## 🎯 Méthode 1 : Déploiement Automatique avec render.yaml

Cette méthode est la plus simple et automatise tout le processus.

### Étape 1 : Vérifier le fichier render.yaml

Le fichier `render.yaml` à la racine de votre projet configure automatiquement :
- Le service web Django
- La base de données PostgreSQL
- Les variables d'environnement
- Les commandes de build et de démarrage

### Étape 2 : Connecter Render à GitHub

1. Allez sur [render.com](https://render.com)
2. Cliquez sur **"Get Started for Free"**
3. Connectez-vous avec votre compte **GitHub**
4. Autorisez Render à accéder à vos dépôts

### Étape 3 : Créer le Blueprint

1. Dans Render, cliquez sur **"New +"** > **"Blueprint"**
2. Sélectionnez votre dépôt **`fmos-mfmc`**
3. Render détectera automatiquement le fichier `render.yaml`
4. Cliquez sur **"Apply"**

Render va automatiquement :
- ✅ Créer le service web
- ✅ Créer la base de données PostgreSQL
- ✅ Configurer toutes les variables d'environnement
- ✅ Lancer le déploiement

### Étape 4 : Attendre le Déploiement

Le déploiement prend généralement 3-5 minutes. Vous pouvez suivre la progression dans les logs.

### Étape 5 : Configuration Post-Déploiement

Une fois le déploiement terminé, suivez la section [Configuration Post-Déploiement](#configuration-post-déploiement).

---

## 🔧 Méthode 2 : Déploiement Manuel

Si vous préférez configurer manuellement ou si le Blueprint ne fonctionne pas.

### Étape 1 : Créer la Base de Données PostgreSQL

1. Dans Render, cliquez sur **"New +"** > **"PostgreSQL"**
2. Configurez :
   - **Name** : `fmos-mfmc-db`
   - **Database** : `fmos_mfmc`
   - **User** : `fmos_mfmc_user`
   - **Region** : Choisissez la région la plus proche (ex: `Frankfurt`)
   - **Plan** : **Free**
3. Cliquez sur **"Create Database"**
4. **Copiez l'Internal Database URL** (vous en aurez besoin plus tard)

### Étape 2 : Créer le Web Service

1. Dans Render, cliquez sur **"New +"** > **"Web Service"**
2. Connectez votre dépôt GitHub :
   - Sélectionnez votre dépôt **`fmos-mfmc`**
   - Cliquez sur **"Connect"**

### Étape 3 : Configurer le Web Service

Remplissez le formulaire :

#### Informations de base :
- **Name** : `fmos-mfmc`
- **Region** : Même région que votre base de données
- **Branch** : `main` (ou `master`)

#### Build & Start :
- **Build Command** :
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Start Command** :
  ```bash
  gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
  ```

#### Plan :
- Sélectionnez **"Free"**

### Étape 4 : Configurer les Variables d'Environnement

Dans la section **Environment Variables**, ajoutez :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `SECRET_KEY` | (généré) | Clé secrète Django |
| `DEBUG` | `False` | Mode production |
| `ALLOWED_HOSTS` | `fmos-mfmc.onrender.com` | Domaine autorisé |
| `DATABASE_URL` | (URL de la base) | URL de connexion PostgreSQL |

#### Générer SECRET_KEY :

Dans votre terminal local :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiez la clé générée et utilisez-la pour `SECRET_KEY`.

### Étape 5 : Créer le Service

Cliquez sur **"Create Web Service"** et attendez le déploiement.

---

## ⚙️ Configuration Post-Déploiement

Une fois votre application déployée, vous devez configurer la base de données et créer un superutilisateur.

### 1. Ouvrir le Shell Render

1. Dans Render, allez dans votre **Web Service**
2. Cliquez sur **"Shell"** (en haut à droite)
3. Un terminal s'ouvrira

### 2. Appliquer les Migrations

Dans le Shell, exécutez :
```bash
python manage.py migrate
```

Vérifiez l'état des migrations :
```bash
python manage.py showmigrations
```

### 3. Créer un Superutilisateur

```bash
python manage.py createsuperuser
```

Entrez :
- **Username** : (votre choix)
- **Email** : (votre email)
- **Password** : (un mot de passe fort)

### 4. Initialiser le Programme DESMFMC

```bash
python manage.py init_programme_desmfmc_detaille
```

### 5. Vérifier le Déploiement

1. **Accéder à l'admin** : `https://fmos-mfmc.onrender.com/admin/`
2. **Tester le site** : `https://fmos-mfmc.onrender.com`
3. **Vérifier les logs** : Dans Render > Logs pour voir s'il y a des erreurs

---

## 🆘 Résolution de Problèmes

### Problème : Bad Gateway (502)

**Solutions** :
1. Vérifiez les **Logs** dans Render
2. Vérifiez que toutes les variables d'environnement sont définies
3. Vérifiez que `DATABASE_URL` est correcte
4. Vérifiez que `ALLOWED_HOSTS` contient votre domaine Render

### Problème : Erreur de Connexion à la Base de Données

**Solutions** :
1. Vérifiez que la base PostgreSQL est active dans Render
2. Vérifiez que `DATABASE_URL` utilise l'**Internal Database URL** (pas l'externe)
3. Vérifiez que la base et le service web sont dans la même région

### Problème : Fichiers Statiques ne se Chargent pas

**Solutions** :
1. Vérifiez que `collectstatic` est dans le Build Command
2. Vérifiez que WhiteNoise est configuré dans `core/settings.py`
3. Vérifiez que `whitenoise>=6.6.0` est dans `requirements.txt`

### Problème : Application en "Spin Down"

**Note** : Sur le plan gratuit, Render met l'application en veille après 15 minutes d'inactivité. Le premier chargement après veille peut prendre 30-60 secondes. C'est normal !

### Problème : Erreur SSL avec la Base de Données

**Solution** : Le projet est déjà configuré pour gérer automatiquement les URLs Render PostgreSQL. Si vous utilisez une URL interne (commençant par `dpg-`), SSL n'est pas nécessaire. Si vous utilisez une URL externe, SSL sera configuré automatiquement.

---

## 🚀 Optimisations

### 1. Configuration des Variables d'Environnement

Pour la production, assurez-vous que :
- `DEBUG=False`
- `SECRET_KEY` est une clé forte et unique
- `ALLOWED_HOSTS` contient votre domaine Render

### 2. Performance

- Les fichiers statiques sont servis par WhiteNoise (déjà configuré)
- La base de données utilise le pooling de connexions (CONN_MAX_AGE=600)
- Les fichiers statiques sont compressés automatiquement

### 3. Monitoring

- Consultez régulièrement les **Logs** dans Render
- Surveillez l'utilisation des ressources dans le dashboard Render
- Configurez des alertes si nécessaire (plan payant)

### 4. Sauvegarde de la Base de Données

Sur le plan gratuit, les sauvegardes automatiques ne sont pas disponibles. Pour sauvegarder votre base :

```bash
# Dans le Shell Render
pg_dump $DATABASE_URL > backup.sql
```

---

## 📝 Checklist de Déploiement

### Avant le Déploiement
- [ ] Compte Render créé
- [ ] Projet GitHub à jour
- [ ] Fichiers de configuration présents (`requirements.txt`, `Procfile`, `runtime.txt`)
- [ ] `render.yaml` créé (optionnel)

### Déploiement
- [ ] Base de données PostgreSQL créée
- [ ] Web Service créé
- [ ] Variables d'environnement configurées (4 variables)
- [ ] Déploiement réussi
- [ ] Site accessible sur `fmos-mfmc.onrender.com`

### Post-Déploiement
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Programme DESMFMC initialisé
- [ ] Accès à l'admin vérifié
- [ ] Site testé et fonctionnel

---

## 📚 Documentation Supplémentaire

Pour plus de détails sur des aspects spécifiques, consultez :

- **Déploiement Rapide** : `CONFIGURATION_RENDER_RAPIDE.md`
- **Résolution Bad Gateway** : `RESOLUTION_BAD_GATEWAY_RENDER.md`
- **Configuration SSL** : `RESOLUTION_ERREUR_SSL_RENDER.md`
- **Diagnostic** : `DIAGNOSTIC_RAPIDE_RENDER.md`

---

## 🎉 Félicitations !

Votre application Django est maintenant déployée sur Render ! 

Pour toute question ou problème, consultez les guides de résolution de problèmes ou les logs Render.

---

**Dernière mise à jour** : Novembre 2025

