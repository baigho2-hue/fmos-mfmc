# 🚀 Étape 3 : Déploiement sur Railway

## ✅ Prérequis vérifiés

- [x] Git initialisé
- [x] Code commité
- [x] Repository GitHub créé
- [x] Code poussé sur GitHub

---

## 📋 Étapes de déploiement sur Railway

### 1. Créer un compte Railway (2 minutes)

1. Allez sur **https://railway.app**
2. Cliquez sur **"Start a New Project"** ou **"Login"**
3. **Connectez-vous avec GitHub** (recommandé - plus simple)
   - Cliquez sur "Login with GitHub"
   - Autorisez Railway à accéder à vos repositories

### 2. Créer un nouveau projet (1 minute)

1. Dans Railway Dashboard, cliquez sur **"New Project"**
2. Sélectionnez **"Deploy from GitHub repo"**
3. Si c'est la première fois, autorisez Railway à accéder à vos repositories GitHub
4. **Sélectionnez votre repository** `fmos-mfmc`
5. Railway va automatiquement :
   - Détecter que c'est un projet Django
   - Commencer le déploiement
   - Créer un service web

### 3. Créer une base de données PostgreSQL (2 minutes)

1. Dans votre projet Railway, vous verrez votre service web Django
2. Cliquez sur **"+ New"** (en haut à droite ou dans le menu)
3. Sélectionnez **"Database"**
4. Choisissez **"Add PostgreSQL"**
5. Railway créera automatiquement une base PostgreSQL
6. **Note importante** : Railway créera automatiquement une variable `DATABASE_URL` - vous n'avez rien à faire de plus !

### 4. Configurer les variables d'environnement (5 minutes)

1. Cliquez sur votre **service web Django** (pas la base de données)
2. Allez dans l'onglet **"Variables"**
3. Cliquez sur **"New Variable"** pour chaque variable suivante :

#### Variables OBLIGATOIRES :

```
Nom: SECRET_KEY
Valeur: gutp!g9gqbuhq9)514-r*tkds6v3p0r(myo0rvgmgc0svu&0-i
```

```
Nom: DEBUG
Valeur: False
```

```
Nom: ALLOWED_HOSTS
Valeur: votre-projet.railway.app
```
**Note** : Railway vous donnera une URL comme `fmos-mfmc-production.up.railway.app`. Utilisez cette URL exacte.

#### Variables OPTIONNELLES (pour les emails) :

```
Nom: EMAIL_HOST
Valeur: smtp.gmail.com
```

```
Nom: EMAIL_PORT
Valeur: 587
```

```
Nom: EMAIL_USE_TLS
Valeur: True
```

```
Nom: EMAIL_HOST_USER
Valeur: votre_email@gmail.com
```

```
Nom: EMAIL_HOST_PASSWORD
Valeur: votre_mot_de_passe_app_gmail
```

```
Nom: DEFAULT_FROM_EMAIL
Valeur: noreply@fmos-mfmc.ml
```

**⚠️ Important** : Pour Gmail, vous devez créer un "Mot de passe d'application" dans les paramètres de sécurité de votre compte Google.

### 5. Vérifier le déploiement (2 minutes)

1. Railway va automatiquement redéployer quand vous ajoutez des variables
2. Allez dans l'onglet **"Deployments"**
3. Attendez que le statut soit **"Success"** (cela peut prendre 2-5 minutes)
4. Si vous voyez une erreur, cliquez sur le déploiement pour voir les logs

### 6. Appliquer les migrations (3 minutes)

Une fois le déploiement réussi :

1. Cliquez sur votre service web Django
2. Allez dans l'onglet **"Deployments"**
3. Cliquez sur le dernier déploiement (celui avec "Success")
4. Cliquez sur l'icône **Terminal** (ou "View Logs" puis "Open Shell")
5. Exécutez ces commandes une par une :

```bash
python manage.py migrate
```

```bash
python manage.py collectstatic --noinput
```

```bash
python manage.py createsuperuser
```
(Suivez les instructions pour créer votre compte admin)

### 7. Accéder à votre site (1 minute)

1. Dans Railway Dashboard, cliquez sur votre service web Django
2. Allez dans l'onglet **"Settings"**
3. Faites défiler jusqu'à **"Domains"**
4. Vous verrez votre URL Railway (ex: `fmos-mfmc-production.up.railway.app`)
5. **Cliquez sur cette URL** pour accéder à votre site !

---

## 🎉 Félicitations !

Votre site est maintenant en ligne !

### URLs importantes :

- **Site principal** : `https://votre-projet.railway.app`
- **Admin Django** : `https://votre-projet.railway.app/admin/`

---

## 🐛 Dépannage

### Le site affiche une erreur 500

1. Vérifiez les logs dans Railway > Deployments > View Logs
2. Vérifiez que `SECRET_KEY` est définie
3. Vérifiez que `DEBUG=False`
4. Vérifiez que `ALLOWED_HOSTS` contient votre URL Railway

### Les fichiers statiques ne se chargent pas

1. Vérifiez que `collectstatic` a été exécuté
2. Vérifiez les logs pour les erreurs
3. WhiteNoise est déjà configuré, cela devrait fonctionner automatiquement

### Erreur de base de données

1. Vérifiez que la base PostgreSQL est créée
2. Vérifiez que les migrations sont appliquées
3. Railway crée automatiquement `DATABASE_URL` - vérifiez qu'elle existe dans les variables

### Le déploiement échoue

1. Vérifiez les logs de build dans Railway
2. Vérifiez que `requirements.txt` est correct
3. Vérifiez que `Procfile` existe

---

## 📝 Checklist finale

- [ ] Compte Railway créé
- [ ] Projet créé et connecté à GitHub
- [ ] Base PostgreSQL créée
- [ ] Variables d'environnement configurées
- [ ] Déploiement réussi
- [ ] Migrations appliquées
- [ ] Fichiers statiques collectés
- [ ] Superutilisateur créé
- [ ] Site accessible
- [ ] Admin Django accessible

---

## 🎯 Prochaines étapes (optionnel)

1. **Configurer un domaine personnalisé** :
   - Railway > Settings > Domains > Custom Domain
   - Configurez les DNS de votre domaine

2. **Configurer les emails** :
   - Créez un mot de passe d'application Gmail
   - Ajoutez les variables d'email dans Railway

3. **Mettre en place des sauvegardes** :
   - Railway propose des sauvegardes automatiques pour PostgreSQL

4. **Monitoring** :
   - Railway fournit des métriques de base
   - Vous pouvez ajouter des services de monitoring externes

---

**Besoin d'aide ?** Consultez les logs dans Railway Dashboard ou le guide complet dans `DEPLOIEMENT_RAILWAY.md`

