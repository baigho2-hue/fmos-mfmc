# 🚀 Guide Complet : Déployer avec Supabase

## 📋 Plan d'action

1. ✅ Créer un compte et projet Supabase
2. ✅ Récupérer les informations de connexion
3. ✅ Tester la connexion localement
4. ✅ Choisir une plateforme de déploiement pour Django
5. ✅ Configurer et déployer

---

## 🗄️ Étape 1 : Créer votre projet Supabase

### 1.1 Créer un compte

1. Allez sur **https://supabase.com**
2. Cliquez sur **"Start your project"**
3. Connectez-vous avec **GitHub** (recommandé)
4. Autorisez Supabase à accéder à votre compte GitHub

### 1.2 Créer un nouveau projet

1. Cliquez sur **"New Project"**
2. Remplissez les informations :
   - **Name** : `fmos-mfmc`
   - **Database Password** : Créez un mot de passe fort (notez-le dans un endroit sûr !)
   - **Region** : Choisissez la région la plus proche (ex: `Europe West` pour l'Afrique de l'Ouest)
   - **Pricing Plan** : **Free** (gratuit)
3. Cliquez sur **"Create new project"**
4. ⏳ Attendez 2-3 minutes que Supabase crée votre projet

---

## 🔑 Étape 2 : Récupérer les informations de connexion

Une fois le projet créé :

1. Dans votre projet Supabase, cliquez sur l'icône **⚙️ Settings** (en bas à gauche)
2. Cliquez sur **"Database"** dans le menu de gauche
3. Faites défiler jusqu'à **"Connection string"**
4. Vous verrez plusieurs onglets : **URI**, **JDBC**, **Connection pooling**

### Option A : URI (Simple - pour débuter)

1. Cliquez sur l'onglet **"URI"**
2. Vous verrez quelque chose comme :
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
   ```
3. **Remplacez `[YOUR-PASSWORD]`** par le mot de passe que vous avez créé
4. **Copiez cette URL complète** - c'est votre `DATABASE_URL` !

**Exemple** :
```
postgresql://postgres:MonMotDePasse123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

### Option B : Connection Pooling (Recommandé pour production)

1. Cliquez sur l'onglet **"Connection pooling"**
2. Utilisez le port **6543** au lieu de 5432
3. URL ressemblera à :
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true
   ```

**Pour Django, utilisez l'Option A (URI) pour commencer.**

---

## 🧪 Étape 3 : Tester la connexion localement

### 3.1 Créer un fichier .env

Créez un fichier `.env` à la racine de votre projet avec :

```env
# Base de données Supabase
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@db.xxxxx.supabase.co:5432/postgres

# Sécurité
SECRET_KEY=gutp!g9gqbuhq9)514-r*tkds6v3p0r(myo0rvgmgc0svu&0-i
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

**Remplacez** :
- `VOTRE_MOT_DE_PASSE` par votre mot de passe Supabase
- `db.xxxxx.supabase.co` par votre host Supabase

### 3.2 Tester la connexion

```powershell
# Activer votre environnement virtuel si vous en avez un
# venv\Scripts\activate

# Tester la connexion
python manage.py migrate
```

Si ça fonctionne, vous verrez les migrations s'appliquer !

---

## 🌐 Étape 4 : Choisir une plateforme de déploiement

Maintenant que Supabase gère votre base de données, vous devez déployer votre application Django quelque part.

### Option 1 : Render (Recommandé - Simple et gratuit)

**Avantages** :
- ✅ Gratuit pour commencer
- ✅ Facile à configurer
- ✅ Support Django natif
- ✅ Déploiement automatique depuis GitHub

**Étapes** :
1. Allez sur **https://render.com**
2. Créez un compte (connectez-vous avec GitHub)
3. Cliquez sur **"New +"** > **"Web Service"**
4. Connectez votre repository GitHub `fmos-mfmc`
5. Render détectera automatiquement Django
6. Configurez les variables d'environnement (voir ci-dessous)

### Option 2 : VPS (Contrôle total)

Déployez sur un VPS Ubuntu/Debian avec Nginx et Gunicorn.
- Plus de contrôle
- Nécessite des connaissances Linux
- Guide disponible dans `GUIDE_DEPLOIEMENT.md`

### Option 3 : Railway (mais avec Supabase)

Vous pouvez continuer avec Railway mais utiliser Supabase :
1. Gardez votre service Django sur Railway
2. Supprimez le service PostgreSQL Railway
3. Ajoutez la variable `DATABASE_URL` avec votre URL Supabase

---

## ⚙️ Étape 5 : Configurer les variables d'environnement

Quelle que soit la plateforme choisie, configurez ces variables :

### Variables OBLIGATOIRES :

```
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY=gutp!g9gqbuhq9)514-r*tkds6v3p0r(myo0rvgmgc0svu&0-i
DEBUG=False
ALLOWED_HOSTS=votre-domaine.render.com
```

**Pour Render** : Votre URL sera quelque chose comme `fmos-mfmc.onrender.com`

### Variables OPTIONNELLES (emails) :

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app_gmail
DEFAULT_FROM_EMAIL=noreply@fmos-mfmc.ml
```

---

## 🚀 Étape 6 : Déployer sur Render (Exemple détaillé)

### 6.1 Créer le service web

1. Allez sur **https://render.com**
2. Cliquez sur **"New +"** > **"Web Service"**
3. Connectez votre repository GitHub si ce n'est pas déjà fait
4. Sélectionnez `baigho2-hue/fmos-mfmc`
5. Remplissez les informations :
   - **Name** : `fmos-mfmc`
   - **Region** : Choisissez la plus proche
   - **Branch** : `main`
   - **Root Directory** : (laissez vide)
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command** : `gunicorn core.wsgi:application`

### 6.2 Configurer les variables

Dans la section **"Environment Variables"**, ajoutez :
- `DATABASE_URL` (votre URL Supabase)
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=votre-app.onrender.com`

### 6.3 Déployer

1. Cliquez sur **"Create Web Service"**
2. Render va commencer le déploiement (5-10 minutes)
3. Une fois terminé, votre site sera accessible !

### 6.4 Appliquer les migrations

1. Dans Render Dashboard, allez dans votre service
2. Cliquez sur **"Shell"** (terminal)
3. Exécutez :
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

---

## ✅ Avantages de Supabase

- ✅ **Gratuit** jusqu'à 500 MB de base de données
- ✅ **Interface graphique** pour voir/modifier vos données
- ✅ **Backups automatiques**
- ✅ **Table Editor** intégré
- ✅ **API REST automatique** (bonus)
- ✅ **Authentification intégrée** (si vous en avez besoin plus tard)

---

## 🔒 Sécurité

1. **Ne partagez jamais** votre mot de passe Supabase publiquement
2. **Utilisez toujours** des variables d'environnement pour `DATABASE_URL`
3. **Ne commitez jamais** le fichier `.env` dans Git
4. **Activez Row Level Security** dans Supabase si nécessaire

---

## 📝 Checklist

- [ ] Compte Supabase créé
- [ ] Projet Supabase créé
- [ ] URL de connexion récupérée
- [ ] Connexion testée localement
- [ ] Plateforme de déploiement choisie
- [ ] Variables d'environnement configurées
- [ ] Application déployée
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Site accessible en ligne

---

## 🆘 Besoin d'aide ?

Dites-moi :
1. **Avez-vous créé votre projet Supabase ?**
2. **Avez-vous récupéré votre URL de connexion ?**
3. **Quelle plateforme voulez-vous utiliser** pour déployer Django ? (Render, VPS, autre)

Je vous guiderai pour la suite !

