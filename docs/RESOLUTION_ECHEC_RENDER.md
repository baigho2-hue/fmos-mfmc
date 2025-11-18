# 🔧 Résolution : Déploiement Échoué sur Render (Exit Status 1)

## 🔍 Diagnostic Immédiat

Le déploiement a échoué avec **"Exit Status 1"**. Voici comment identifier et résoudre le problème.

---

## 📋 ÉTAPE 1 : Vérifier les Logs de Build

1. Dans Render, allez dans votre **Web Service**
2. Cliquez sur l'onglet **"Logs"** ou **"Events"**
3. **Lisez les erreurs** affichées dans les logs

### Erreurs courantes à chercher :

#### ❌ Erreur 1 : "ModuleNotFoundError"
```
ModuleNotFoundError: No module named 'xxx'
```
**Solution** : Le package manque dans `requirements.txt`

#### ❌ Erreur 2 : "Could not connect to database"
```
django.db.utils.OperationalError: could not connect
```
**Solution** : `DATABASE_URL` n'est pas configurée ou incorrecte

#### ❌ Erreur 3 : "SECRET_KEY not set"
```
ImproperlyConfigured: The SECRET_KEY setting must not be empty
```
**Solution** : Ajoutez `SECRET_KEY` dans les variables d'environnement

#### ❌ Erreur 4 : "ALLOWED_HOSTS"
```
DisallowedHost at /
```
**Solution** : Ajoutez votre domaine Render dans `ALLOWED_HOSTS`

#### ❌ Erreur 5 : "gunicorn: command not found"
```
gunicorn: command not found
```
**Solution** : Vérifiez que `gunicorn` est dans `requirements.txt`

---

## ✅ ÉTAPE 2 : Vérifier les Variables d'Environnement

Dans Render > Web Service > **Environment** :

Vérifiez que vous avez **TOUTES** ces variables :

### Variable 1 : SECRET_KEY
- **Key** : `SECRET_KEY`
- **Value** : Une clé secrète Django (générez-en une nouvelle si besoin)

### Variable 2 : DEBUG
- **Key** : `DEBUG`
- **Value** : `False` (en production)

### Variable 3 : ALLOWED_HOSTS
- **Key** : `ALLOWED_HOSTS`
- **Value** : `votre-app.onrender.com` (remplacez par votre URL Render)

### Variable 4 : DATABASE_URL
- **Key** : `DATABASE_URL`
- **Value** : L'URL complète de votre base PostgreSQL

**Si une variable manque, ajoutez-la immédiatement !**

---

## 🔧 ÉTAPE 3 : Vérifier la Configuration du Build

Dans Render > Web Service > **Settings** :

### Build Command :
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

### Start Command :
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

**Note** : Render définit automatiquement `$PORT`, vous n'avez pas besoin de le définir manuellement.

**Vérifiez que ces commandes sont exactement comme ci-dessus !**

---

## 🗄️ ÉTAPE 4 : Vérifier la Base de Données

### Option A : Utiliser PostgreSQL de Render

1. Dans Render, créez une **PostgreSQL** (si pas encore fait)
2. Copiez l'**Internal Database URL**
3. Ajoutez-la dans les variables d'environnement comme `DATABASE_URL`

### Option B : Utiliser Supabase

1. Vérifiez que votre URL Supabase est correcte
2. **Encodez le mot de passe** si nécessaire (ex: `@` devient `%40`)
3. Ajoutez-la dans `DATABASE_URL`

---

## 🔄 ÉTAPE 5 : Vérifier requirements.txt

Votre `requirements.txt` doit contenir **au minimum** :

```
Django>=4.2,<5.0
psycopg2-binary>=2.9
python-dotenv>=1.0
gunicorn>=21.2.0
whitenoise>=6.6.0
dj-database-url>=2.1.0
xhtml2pdf>=0.2.0
reportlab>=4.0
```

**Vérifiez que tous les packages sont présents !**

---

## 🚀 ÉTAPE 6 : Redéployer

Une fois les corrections faites :

1. Dans Render, allez dans votre Web Service
2. Cliquez sur **"Manual Deploy"** > **"Deploy latest commit"**
3. Surveillez les logs pour voir si ça fonctionne

---

## 🆘 Solutions Spécifiques par Erreur

### Erreur : "No module named 'dj_database_url'"

**Solution** :
1. Vérifiez que `dj-database-url>=2.1.0` est dans `requirements.txt`
2. Redéployez

### Erreur : "Could not translate host name"

**Solution** :
1. Vérifiez que `DATABASE_URL` est correcte
2. Si vous utilisez Supabase, utilisez l'URL de **Connection Pooling** (port 6543)

### Erreur : "password authentication failed"

**Solution** :
1. Réinitialisez le mot de passe de votre base de données
2. Mettez à jour `DATABASE_URL` avec le nouveau mot de passe
3. **Encodez les caractères spéciaux** dans le mot de passe (ex: `@` → `%40`)

### Erreur : "collectstatic failed"

**Solution** :
1. Vérifiez que `whitenoise` est dans `requirements.txt`
2. Vérifiez que WhiteNoise est configuré dans `settings.py`
3. Le Build Command devrait inclure `collectstatic`

---

## 📝 Checklist de Vérification

Avant de redéployer, vérifiez :

- [ ] **4 variables d'environnement** sont configurées (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DATABASE_URL)
- [ ] **Build Command** est correct
- [ ] **Start Command** est correct
- [ ] **requirements.txt** contient tous les packages nécessaires
- [ ] **Base de données** est créée et accessible
- [ ] **ALLOWED_HOSTS** contient votre domaine Render (ex: `votre-app.onrender.com`)

---

## 💡 Astuce : Activer DEBUG Temporairement

Pour voir les erreurs détaillées :

1. Dans Render > Environment, changez `DEBUG` à `True`
2. Redéployez
3. Visitez votre site - vous verrez les erreurs détaillées
4. **Important** : Remettez `DEBUG=False` après avoir résolu le problème !

---

## 🎯 Prochaines Actions

1. **Lisez les logs** dans Render pour identifier l'erreur exacte
2. **Vérifiez les 4 variables** d'environnement
3. **Corrigez le problème** identifié
4. **Redéployez**

---

## 📞 Dites-moi

1. **Quelle erreur voyez-vous** dans les logs Render ?
2. **Les 4 variables** sont-elles toutes configurées ?
3. **Avez-vous créé** une base PostgreSQL dans Render ?

Avec ces informations, je pourrai vous aider à résoudre le problème précisément ! 🔧

