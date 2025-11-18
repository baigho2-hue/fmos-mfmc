# 🖥️ Accéder au Terminal Railway

## 📍 Où trouver le terminal dans Railway

### Méthode 1 : Via l'onglet "Deployments"

1. Dans Railway, cliquez sur votre service Django (celui marqué "WEB")
2. Allez dans l'onglet **"Deployments"** (en haut)
3. Cliquez sur le **dernier déploiement** (celui qui est actif, généralement en haut de la liste)
4. Vous verrez plusieurs onglets : **"Logs"**, **"Metrics"**, **"Shell"** ou **"Terminal"**
5. Cliquez sur **"Shell"** ou **"Terminal"** pour ouvrir le terminal

### Méthode 2 : Via l'onglet "Settings"

1. Dans votre service Django, allez dans **"Settings"** (icône ⚙️)
2. Cherchez une section **"Shell"** ou **"Terminal"**
3. Cliquez dessus pour ouvrir le terminal

### Méthode 3 : Via le menu du service

1. Cliquez sur votre service Django
2. Cherchez un bouton **"Open Shell"** ou **"Terminal"** quelque part dans l'interface
3. Cliquez dessus

---

## 🔍 Si vous ne trouvez pas le terminal

### Vérification 1 : Le service est-il actif ?

- Assurez-vous que votre service Django est **"Active"** ou **"Deployed"**
- Si le statut est "No active deployment", vous devez d'abord déployer

### Vérification 2 : Interface Railway

L'interface Railway peut varier. Cherchez :
- Un bouton **"Shell"**
- Un bouton **"Terminal"**
- Un onglet **"Shell"**
- Un onglet **"Terminal"**
- Un bouton **"Open Shell"**

---

## 🗄️ Gérer la Base de Données

### Option A : Recréer PostgreSQL dans Railway (Recommandé)

1. Dans votre projet Railway, cliquez sur **"New"** (bouton vert)
2. Sélectionnez **"Database"** > **"Add PostgreSQL"**
3. Railway va créer une nouvelle base PostgreSQL
4. Copiez l'URL de connexion depuis les Variables du service PostgreSQL
5. Mettez à jour `DATABASE_URL` dans votre service Django

### Option B : Utiliser Supabase

Si vous préférez utiliser Supabase :

1. Allez dans votre service Django > **"Variables"**
2. Ajoutez ou modifiez `DATABASE_URL` avec votre URL Supabase
3. **Important** : Réinitialisez le mot de passe Supabase car il a été exposé dans Git

---

## 📝 Une fois le terminal ouvert

Dans le terminal Railway, vous pouvez exécuter :

```bash
# Vérifier que vous êtes dans le bon répertoire
pwd

# Lister les fichiers
ls

# Lancer les migrations (si base de données configurée)
python manage.py migrate --noinput

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer un superutilisateur
python manage.py createsuperuser
```

---

## 🆘 Si vous ne trouvez toujours pas le terminal

Dites-moi :
1. **Quel est le statut** de votre service Django ? (Active, Deployed, Error, etc.)
2. **Quels onglets voyez-vous** dans votre service Django ? (Deployments, Settings, Variables, etc.)
3. **Y a-t-il un bouton** "Shell", "Terminal", ou similaire quelque part ?

Je pourrai vous guider plus précisément avec ces informations !

