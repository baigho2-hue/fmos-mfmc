# 🗄️ Configuration avec Supabase

## 📋 Vue d'ensemble

Supabase est une alternative à PostgreSQL hébergée. Vous pouvez :
- Utiliser Supabase comme base de données
- Déployer votre application Django sur une autre plateforme (Render, Vercel, ou un VPS)
- Ou continuer avec Railway mais utiliser Supabase au lieu de leur PostgreSQL

---

## 🚀 Étape 1 : Créer un compte Supabase

1. Allez sur **https://supabase.com**
2. Cliquez sur **"Start your project"** ou **"Sign up"**
3. Connectez-vous avec GitHub (recommandé)
4. Créez un nouveau projet

---

## 🏗️ Étape 2 : Créer un projet Supabase

1. Cliquez sur **"New Project"**
2. Remplissez les informations :
   - **Name** : `fmos-mfmc`
   - **Database Password** : Créez un mot de passe fort (notez-le !)
   - **Region** : Choisissez la région la plus proche (ex: Europe West)
   - **Pricing Plan** : Free (gratuit)
3. Cliquez sur **"Create new project"**
4. Attendez 2-3 minutes que Supabase crée votre projet

---

## 🔑 Étape 3 : Récupérer les informations de connexion

Une fois le projet créé :

1. Dans votre projet Supabase, allez dans **"Settings"** (icône d'engrenage)
2. Cliquez sur **"Database"** dans le menu de gauche
3. Faites défiler jusqu'à **"Connection string"**
4. Vous verrez plusieurs options. Choisissez **"URI"** ou **"Connection pooling"**

### Option 1 : URI (recommandé pour Django)

Vous verrez quelque chose comme :
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

**Remplacez `[YOUR-PASSWORD]`** par le mot de passe que vous avez créé.

### Option 2 : Informations séparées

Vous pouvez aussi utiliser les informations séparées :
- **Host** : `db.xxxxx.supabase.co`
- **Database name** : `postgres`
- **Port** : `5432`
- **User** : `postgres`
- **Password** : Le mot de passe que vous avez créé

---

## ⚙️ Étape 4 : Configurer Django pour Supabase

### Option A : Utiliser DATABASE_URL (recommandé)

Dans votre fichier `.env` local (pour tester) ou dans les variables d'environnement de votre plateforme de déploiement :

```env
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@db.xxxxx.supabase.co:5432/postgres
```

Django utilisera automatiquement cette variable grâce à `dj-database-url` que nous avons déjà configuré !

### Option B : Utiliser les variables séparées

Si vous préférez utiliser les variables séparées :

```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
```

---

## 🧪 Étape 5 : Tester la connexion localement

1. Créez un fichier `.env` à la racine de votre projet (s'il n'existe pas déjà)
2. Ajoutez la variable `DATABASE_URL` avec votre URL Supabase
3. Testez la connexion :

```powershell
python manage.py migrate
```

Si ça fonctionne, vous verrez les migrations s'appliquer !

---

## 🌐 Étape 6 : Déployer votre application

Maintenant que vous avez Supabase comme base de données, vous pouvez déployer votre application Django sur :

### Option 1 : Render (recommandé - similaire à Railway)

1. Allez sur **https://render.com**
2. Créez un compte
3. Créez un nouveau **Web Service**
4. Connectez votre repository GitHub
5. Configurez les variables d'environnement avec votre `DATABASE_URL` Supabase

### Option 2 : Vercel (pour applications Django simples)

Vercel supporte Django mais avec quelques limitations.

### Option 3 : VPS (contrôle total)

Déployez sur un VPS Ubuntu/Debian avec Nginx et Gunicorn.

### Option 4 : Continuer avec Railway mais utiliser Supabase

Vous pouvez garder Railway pour l'application mais utiliser Supabase comme base :
1. Dans Railway, supprimez le service PostgreSQL
2. Ajoutez la variable `DATABASE_URL` avec votre URL Supabase
3. Redéployez

---

## 📝 Variables d'environnement à configurer

Quelle que soit la plateforme choisie, configurez ces variables :

### Obligatoires :

```
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY=gutp!g9gqbuhq9)514-r*tkds6v3p0r(myo0rvgmgc0svu&0-i
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
```

### Optionnelles (emails) :

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app
DEFAULT_FROM_EMAIL=noreply@fmos-mfmc.ml
```

---

## ✅ Avantages de Supabase

- ✅ **Gratuit** jusqu'à 500 MB de base de données
- ✅ **Interface graphique** pour gérer votre base de données
- ✅ **Backups automatiques**
- ✅ **API REST automatique** (bonus si vous en avez besoin plus tard)
- ✅ **Table Editor** pour voir/modifier vos données facilement

---

## 🔒 Sécurité Supabase

1. **Ne partagez jamais** votre mot de passe Supabase publiquement
2. **Utilisez des variables d'environnement** pour stocker `DATABASE_URL`
3. **Activez Row Level Security** dans Supabase si nécessaire
4. **Limitez les connexions** depuis certaines IP si possible

---

## 🆘 Besoin d'aide ?

Dites-moi :
1. **Avez-vous créé votre projet Supabase ?**
2. **Quelle plateforme voulez-vous utiliser** pour déployer Django ? (Render, Vercel, VPS, ou autre)
3. **Avez-vous récupéré votre URL de connexion** Supabase ?

Je vous guiderai pour la suite !

