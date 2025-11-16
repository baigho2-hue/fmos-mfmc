# 🎯 Guide Étape par Étape - Déploiement Gratuit sur Railway

## 📋 PRÉPARATION

### ✅ Vérification 1 : Votre code est-il sur GitHub ?

Vérifiez avec :
```bash
git remote -v
```

Si vous voyez `origin` avec une URL GitHub, c'est bon ✅
Sinon, vous devrez créer un dépôt GitHub d'abord.

---

## 🚀 ÉTAPE 1 : Préparer le code pour GitHub

### 1.1. Vérifier les fichiers à commiter

```bash
git status
```

### 1.2. Ajouter tous les fichiers (sauf ceux dans .gitignore)

```bash
git add .
```

### 1.3. Créer un commit

```bash
git commit -m "Application prête pour déploiement sur Railway"
```

### 1.4. Pousser sur GitHub

```bash
git push origin main
```

**Si vous avez une erreur**, dites-moi et je vous aiderai à la résoudre.

---

## 🚂 ÉTAPE 2 : Créer un compte Railway

### 2.1. Aller sur Railway

1. Ouvrez votre navigateur
2. Allez sur : **https://railway.app**
3. Cliquez sur **"Start a New Project"** ou **"Login"**

### 2.2. Se connecter avec GitHub

1. Cliquez sur **"Login with GitHub"**
2. Autorisez Railway à accéder à votre compte GitHub
3. Acceptez les permissions

### 2.3. Vérifier votre compte

Une fois connecté, vous devriez voir votre tableau de bord Railway.

**✅ Dites-moi quand vous êtes connecté à Railway !**

---

## 📦 ÉTAPE 3 : Créer un nouveau projet

### 3.1. Démarrer un nouveau projet

1. Dans Railway, cliquez sur **"New Project"** (bouton vert en haut à droite)
2. Vous verrez plusieurs options

### 3.2. Choisir "Deploy from GitHub repo"

1. Cliquez sur **"Deploy from GitHub repo"**
2. Railway va lister vos dépôts GitHub

### 3.3. Sélectionner votre dépôt

1. Cherchez **`fmos-mfmc`** dans la liste
2. Cliquez dessus
3. Railway va commencer à analyser votre projet

**✅ Dites-moi quand vous avez sélectionné le dépôt !**

---

## ⚙️ ÉTAPE 4 : Configurer les variables d'environnement

### 4.1. Accéder aux variables

Une fois le projet créé :
1. Cliquez sur votre projet dans Railway
2. Cliquez sur votre service Django (il devrait être créé automatiquement)
3. Allez dans l'onglet **"Variables"**

### 4.2. Ajouter les variables

Cliquez sur **"New Variable"** et ajoutez une par une :

#### Variable 1 : SECRET_KEY
- **Name** : `SECRET_KEY`
- **Value** : (générez-en une nouvelle, voir ci-dessous)

#### Variable 2 : DEBUG
- **Name** : `DEBUG`
- **Value** : `False`

#### Variable 3 : ALLOWED_HOSTS
- **Name** : `ALLOWED_HOSTS`
- **Value** : `*.railway.app`

#### Variable 4 : DATABASE_URL
- **Name** : `DATABASE_URL`
- **Value** : `postgresql://postgres.VOTRE_PROJECT_ID:VOTRE_MOT_DE_PASSE@aws-1-eu-north-1.pooler.supabase.com:5432/postgres`

### 4.3. Générer une SECRET_KEY

Exécutez cette commande dans votre terminal :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiez le résultat et utilisez-le comme valeur pour `SECRET_KEY`.

**✅ Dites-moi quand toutes les variables sont ajoutées !**

---

## 🔧 ÉTAPE 5 : Configurer le déploiement

### 5.1. Vérifier le Procfile

Railway devrait détecter automatiquement votre `Procfile`. Vérifiez dans **Settings** > **Deploy** que la commande de démarrage est :
```
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

### 5.2. Ajouter la commande post-déploiement

Dans **Settings** > **Deploy** > **Post Deploy Command**, ajoutez :

```
python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

Cela appliquera les migrations et collectera les fichiers statiques automatiquement.

**✅ Dites-moi quand c'est configuré !**

---

## 🚀 ÉTAPE 6 : Déployer

### 6.1. Lancer le déploiement

Railway devrait commencer à déployer automatiquement. Vous verrez les logs en temps réel.

### 6.2. Attendre la fin du déploiement

- Regardez les logs dans Railway
- Attendez que vous voyiez **"Build successful"** ou **"Deploy successful"**
- Cela peut prendre 2-5 minutes

**✅ Dites-moi quand le déploiement est terminé !**

---

## 🌐 ÉTAPE 7 : Obtenir votre URL

### 7.1. Générer un domaine

1. Dans votre service Django, allez dans l'onglet **"Settings"**
2. Cherchez la section **"Domains"**
3. Cliquez sur **"Generate Domain"**
4. Railway va créer une URL comme : `votre-app.railway.app`

### 7.2. Tester votre site

1. Cliquez sur l'URL générée
2. Votre site devrait s'afficher !
3. Testez `/admin` pour accéder à l'admin Django

**✅ Dites-moi si votre site fonctionne !**

---

## 👤 ÉTAPE 8 : Créer un superutilisateur

### 8.1. Ouvrir le terminal Railway

1. Dans votre service Django, allez dans l'onglet **"Deployments"**
2. Cliquez sur le dernier déploiement
3. Cliquez sur **"View Logs"**
4. Cliquez sur **"Open Terminal"** ou **"Shell"**

### 8.2. Créer le superutilisateur

Dans le terminal Railway, exécutez :

```bash
python manage.py createsuperuser
```

Entrez :
- **Username** : `admin`
- **Email** : `admin@fmos-mfmc.ml`
- **Password** : `Malifalifou_19Soul` (ou votre mot de passe)

**✅ Dites-moi quand le superutilisateur est créé !**

---

## ✅ ÉTAPE 9 : Vérifications finales

### 9.1. Tester l'application

- [ ] La page d'accueil s'affiche
- [ ] L'admin Django est accessible (`/admin`)
- [ ] Les fichiers statiques se chargent (CSS, images)
- [ ] La connexion fonctionne

### 9.2. Vérifier les logs

Dans Railway > **View Logs**, vérifiez qu'il n'y a pas d'erreurs.

---

## 🆘 EN CAS DE PROBLÈME

### Problème : Le déploiement échoue

**Solution** :
1. Regardez les logs dans Railway
2. Vérifiez que toutes les variables d'environnement sont définies
3. Vérifiez que `DATABASE_URL` est correcte

### Problème : Erreur 500

**Solution** :
1. Activez temporairement `DEBUG=True` pour voir les erreurs
2. Regardez les logs dans Railway
3. Vérifiez la connexion à Supabase

### Problème : Fichiers statiques ne se chargent pas

**Solution** :
1. Vérifiez que `collectstatic` a été exécuté (dans Post Deploy Command)
2. Vérifiez que WhiteNoise est configuré dans `settings.py`

---

## 🎉 FÉLICITATIONS !

Une fois toutes ces étapes terminées, votre site sera en ligne gratuitement sur Railway !

**Votre URL sera** : `https://votre-app.railway.app`

---

## 📝 RÉSUMÉ DES ÉTAPES

1. ✅ Pousser le code sur GitHub
2. ✅ Créer un compte Railway
3. ✅ Créer un nouveau projet
4. ✅ Configurer les variables d'environnement
5. ✅ Configurer le déploiement
6. ✅ Déployer
7. ✅ Obtenir votre URL
8. ✅ Créer un superutilisateur
9. ✅ Tester votre site

---

**Prêt à commencer ? Dites-moi à quelle étape vous êtes et je vous guiderai ! 🚀**

