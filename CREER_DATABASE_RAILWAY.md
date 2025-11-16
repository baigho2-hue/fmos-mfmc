# 🗄️ Créer une Base de Données PostgreSQL dans Railway

## 🎯 Option 1 : Créer une Base de Données PostgreSQL dans Railway (Recommandé)

### Étape 1 : Ajouter une base de données PostgreSQL

1. Dans Railway, allez dans votre **projet**
2. Cliquez sur **"New"** (bouton vert en haut à droite)
3. Sélectionnez **"Database"** > **"Add PostgreSQL"**
4. Railway va créer automatiquement une base de données PostgreSQL

### Étape 2 : Obtenir l'URL de connexion

Une fois la base de données créée :

1. Cliquez sur votre service **PostgreSQL**
2. Allez dans l'onglet **"Variables"**
3. Cherchez la variable **`DATABASE_URL`**
4. **Copiez cette URL** - elle ressemble à :
   ```
   postgresql://postgres:motdepasse@containers-us-west-xxx.railway.app:5432/railway
   ```

### Étape 3 : Configurer la variable DATABASE_URL dans votre service Django

1. Allez dans votre service **Django**
2. Allez dans l'onglet **"Variables"**
3. Cherchez la variable **`DATABASE_URL`**
4. **Remplacez** la valeur par l'URL que vous avez copiée depuis le service PostgreSQL
5. Ou **ajoutez** cette variable si elle n'existe pas

### Étape 4 : Redéployer votre service Django

1. Allez dans votre service Django
2. Cliquez sur **"Deployments"**
3. Cliquez sur **"Redeploy"** ou **"New Deployment"**
4. Railway va redéployer avec la nouvelle base de données

---

## 🎯 Option 2 : Utiliser Supabase (Déjà configuré)

Si vous préférez utiliser Supabase (que nous avons déjà configuré) :

### Vérifier la connexion Supabase

1. Dans Railway, allez dans votre service Django
2. Allez dans l'onglet **"Variables"**
3. Vérifiez que **`DATABASE_URL`** contient votre URL Supabase :
   ```
   postgresql://postgres.VOTRE_PROJECT_ID:VOTRE_MOT_DE_PASSE@aws-1-eu-north-1.pooler.supabase.com:5432/postgres
   ```

### Si la connexion Supabase ne fonctionne pas

Railway peut avoir des restrictions réseau. Dans ce cas, utilisez **Option 1** (créer une base PostgreSQL dans Railway).

---

## ✅ Recommandation

**Utilisez Option 1** (PostgreSQL dans Railway) car :
- ✅ Plus simple à configurer
- ✅ Pas de problèmes de réseau
- ✅ Gratuit sur Railway
- ✅ Intégré directement

---

## 📝 Après avoir créé la base de données

Une fois la base de données créée et configurée :

1. **Redéployez** votre service Django
2. **Ouvrez le terminal Railway** de votre service Django
3. **Lancez les migrations** :
   ```bash
   python manage.py migrate --noinput
   ```
4. **Collectez les fichiers statiques** :
   ```bash
   python manage.py collectstatic --noinput
   ```
5. **Créez un superutilisateur** :
   ```bash
   python manage.py createsuperuser
   ```

---

## 🆘 Si vous avez des problèmes

Dites-moi :
1. Avez-vous créé la base de données PostgreSQL dans Railway ?
2. Avez-vous copié l'URL de connexion ?
3. Avez-vous mis à jour la variable `DATABASE_URL` dans votre service Django ?
4. Voyez-vous des erreurs dans les logs ?

Je vous aiderai à résoudre le problème !
