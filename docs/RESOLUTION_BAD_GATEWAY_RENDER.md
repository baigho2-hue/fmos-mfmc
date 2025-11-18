# 🔧 Résolution : Bad Gateway sur Render

## 🔍 Diagnostic

**"Bad Gateway"** signifie que Render ne peut pas communiquer avec votre application Django. Cela peut avoir plusieurs causes.

---

## 📋 Causes Courantes

### 1️⃣ Application ne démarre pas correctement
- Erreur dans `settings.py`
- Module manquant
- Erreur de connexion à la base de données

### 2️⃣ Gunicorn ne démarre pas
- Port incorrect
- Commande de démarrage incorrecte
- Erreur dans `wsgi.py`

### 3️⃣ Base de données inaccessible
- `DATABASE_URL` incorrecte
- Base de données non créée
- Problème de connexion réseau

---

## ✅ ÉTAPE 1 : Vérifier les Logs Render

**C'est la première chose à faire !**

1. Dans Render > Web Service
2. Allez dans l'onglet **"Logs"**
3. **Lisez les dernières erreurs**

### Erreurs à chercher :

#### ❌ "Could not connect to database"
```
django.db.utils.OperationalError: could not connect
```
**Solution** : Vérifiez `DATABASE_URL`

#### ❌ "SECRET_KEY not set"
```
ImproperlyConfigured: The SECRET_KEY setting must not be empty
```
**Solution** : Ajoutez `SECRET_KEY` dans Environment

#### ❌ "ModuleNotFoundError"
```
ModuleNotFoundError: No module named 'xxx'
```
**Solution** : Ajoutez le package dans `requirements.txt`

#### ❌ "Address already in use"
```
OSError: [Errno 98] Address already in use
```
**Solution** : Vérifiez la commande Start Command

---

## ✅ ÉTAPE 2 : Vérifier les Variables d'Environnement

Dans Render > Web Service > **Environment** :

Vérifiez que vous avez **TOUTES** ces variables :

| Variable | Valeur Exemple | Obligatoire |
|----------|----------------|-------------|
| `SECRET_KEY` | `django-insecure-abc123...` | ✅ Oui |
| `DEBUG` | `False` | ✅ Oui |
| `ALLOWED_HOSTS` | `votre-app.onrender.com` | ✅ Oui |
| `DATABASE_URL` | `postgresql://...` | ✅ Oui |

**Si une variable manque → Ajoutez-la !**

---

## ✅ ÉTAPE 3 : Vérifier la Commande de Démarrage

Dans Render > Web Service > **Settings** :

**Start Command** doit être :
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

**Vérifiez que c'est exactement comme ça !**

---

## ✅ ÉTAPE 4 : Vérifier la Base de Données

### Option A : PostgreSQL Render

1. Dans Render, vérifiez que vous avez créé une **PostgreSQL**
2. Allez dans PostgreSQL > **Connections**
3. Copiez l'**Internal Database URL**
4. Vérifiez qu'elle est dans `DATABASE_URL` de votre Web Service

### Option B : Supabase

1. Vérifiez que votre URL Supabase est correcte
2. **Encodez le mot de passe** si nécessaire (`@` → `%40`)
3. Vérifiez que `DATABASE_URL` est correcte

---

## 🔧 Solutions Spécifiques

### Solution 1 : Activer DEBUG Temporairement

Pour voir les erreurs détaillées :

1. Dans Render > Environment
2. Changez `DEBUG` à `True`
3. Redéployez
4. Visitez votre site - vous verrez les erreurs détaillées
5. **Important** : Remettez `DEBUG=False` après !

---

### Solution 2 : Vérifier les Migrations

Si l'application démarre mais échoue :

1. Dans Render > Web Service > **Shell**
2. Exécutez :
   ```bash
   python manage.py migrate --noinput
   ```

---

### Solution 3 : Vérifier la Connexion à la Base de Données

Dans Render > Web Service > **Shell** :

```bash
python manage.py dbshell
```

Si ça échoue → Problème de connexion à la base de données.

---

## 📝 Checklist de Vérification

Avant de redéployer :

- [ ] **Logs lus** - Erreur identifiée
- [ ] **4 variables** d'environnement configurées
- [ ] **Start Command** correct
- [ ] **Base de données** créée et accessible
- [ ] **DATABASE_URL** correcte
- [ ] **ALLOWED_HOSTS** contient votre domaine Render

---

## 🚀 Redéployer

Une fois les corrections faites :

1. Dans Render > Web Service
2. Cliquez sur **"Manual Deploy"** > **"Deploy latest commit"**
3. Surveillez les logs

---

## 💡 Astuce : Vérifier les Logs en Temps Réel

Dans Render > Web Service > **Logs** :

Vous pouvez voir les logs en temps réel. Cherchez :
- Messages de démarrage Gunicorn
- Erreurs de connexion
- Erreurs Django

---

## 📞 Dites-moi

1. **Quelle erreur voyez-vous** dans les logs Render ?
2. **Les 4 variables** sont-elles configurées ?
3. **Avez-vous créé** une base PostgreSQL dans Render ?

Avec ces informations, je pourrai vous aider à résoudre le problème précisément ! 🔧

