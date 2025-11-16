# ⚙️ Étape 4 : Configurer les variables d'environnement sur Railway

## ✅ Base de données créée !

Maintenant que votre base PostgreSQL est créée, Railway a automatiquement créé la variable `DATABASE_URL`. Vérifions que tout est bien configuré.

---

## 📋 Configuration des variables d'environnement

### 1. Accéder aux variables

1. Dans Railway Dashboard, cliquez sur votre **service web Django** (pas la base de données)
2. Allez dans l'onglet **"Variables"** ou **"Environment Variables"**

### 2. Vérifier DATABASE_URL

Railway devrait avoir automatiquement créé `DATABASE_URL`. Vérifiez qu'elle existe dans la liste des variables.

**Si elle n'existe pas :**
- Cliquez sur votre service PostgreSQL
- Allez dans l'onglet **"Variables"**
- Copiez la valeur de `DATABASE_URL`
- Retournez dans votre service Django > Variables
- Ajoutez-la manuellement

### 3. Ajouter les variables obligatoires

Cliquez sur **"New Variable"** pour chaque variable suivante :

#### Variable 1 : SECRET_KEY

```
Nom: SECRET_KEY
Valeur: gutp!g9gqbuhq9)514-r*tkds6v3p0r(myo0rvgmgc0svu&0-i
```

#### Variable 2 : DEBUG

```
Nom: DEBUG
Valeur: False
```

⚠️ **Important** : Mettez bien `False` (avec F majuscule), pas `false` ou `FALSE`.

#### Variable 3 : ALLOWED_HOSTS

```
Nom: ALLOWED_HOSTS
Valeur: votre-projet.railway.app
```

**Comment trouver votre URL Railway :**
1. Allez dans votre service Django > **Settings**
2. Faites défiler jusqu'à **"Domains"**
3. Vous verrez une URL comme `fmos-mfmc-production.up.railway.app`
4. **Copiez cette URL exacte** et utilisez-la pour `ALLOWED_HOSTS`

**Exemple** : Si votre URL est `fmos-mfmc-production.up.railway.app`, alors :
```
ALLOWED_HOSTS = fmos-mfmc-production.up.railway.app
```

---

## 🔄 Redéploiement automatique

Dès que vous ajoutez une variable, Railway redéploie automatiquement votre application. Cela peut prendre 2-5 minutes.

### Vérifier le déploiement

1. Allez dans l'onglet **"Deployments"**
2. Attendez que le statut soit **"Success"** (icône verte)
3. Si vous voyez une erreur, cliquez sur le déploiement pour voir les logs

---

## 📧 Variables optionnelles (pour les emails)

Si vous voulez configurer l'envoi d'emails plus tard, vous pouvez ajouter :

```
EMAIL_HOST = smtp.gmail.com
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = votre_email@gmail.com
EMAIL_HOST_PASSWORD = votre_mot_de_passe_app_gmail
DEFAULT_FROM_EMAIL = noreply@fmos-mfmc.ml
```

**Note** : Pour Gmail, vous devez créer un "Mot de passe d'application" dans les paramètres de sécurité de votre compte Google.

---

## ✅ Checklist des variables

Vérifiez que vous avez bien :

- [ ] `DATABASE_URL` (créée automatiquement par Railway)
- [ ] `SECRET_KEY` (la clé que je vous ai donnée)
- [ ] `DEBUG` (False)
- [ ] `ALLOWED_HOSTS` (votre URL Railway)

---

## 🎯 Prochaine étape

Une fois les variables configurées et le déploiement réussi, vous devrez :

1. **Appliquer les migrations** (créer les tables dans la base de données)
2. **Collecter les fichiers statiques**
3. **Créer un superutilisateur** (pour accéder à l'admin Django)

Je vous guiderai pour cela dans l'étape suivante !

---

**Dites-moi quand vous avez ajouté toutes les variables et que le déploiement est réussi !**

