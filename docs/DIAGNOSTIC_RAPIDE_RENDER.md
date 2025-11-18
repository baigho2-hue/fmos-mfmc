# ⚡ Diagnostic Rapide : Échec de Déploiement Render

## 🎯 Actions Immédiates (5 minutes)

### 1️⃣ Vérifier les Logs (2 min)

Dans Render > Web Service > **Logs** :

**Copiez la dernière erreur** que vous voyez. Elle ressemble à :
- `ModuleNotFoundError: No module named 'xxx'`
- `django.db.utils.OperationalError: ...`
- `ImproperlyConfigured: ...`

---

### 2️⃣ Vérifier les 4 Variables (2 min)

Dans Render > Web Service > **Environment** :

Vérifiez que vous avez **EXACTEMENT** ces 4 variables :

| Variable | Exemple de Valeur |
|----------|-------------------|
| `SECRET_KEY` | `django-insecure-abc123...` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `votre-app.onrender.com` |
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` |

**Si une variable manque → Ajoutez-la !**

---

### 3️⃣ Vérifier les Commandes (1 min)

Dans Render > Web Service > **Settings** :

**Build Command** :
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

**Start Command** :
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

**Si différent → Corrigez !**

---

## 🔍 Erreurs Courantes et Solutions

### ❌ "ModuleNotFoundError: No module named 'xxx'"

**Solution** :
1. Ouvrez `requirements.txt`
2. Ajoutez le package manquant
3. Commitez et poussez : `git add requirements.txt && git commit -m "Ajout package" && git push`
4. Redéployez dans Render

---

### ❌ "Could not connect to database"

**Solution** :
1. Vérifiez que `DATABASE_URL` est définie dans Environment
2. Vérifiez que l'URL est correcte (copiez depuis PostgreSQL)
3. Si vous utilisez Supabase, encodez le mot de passe (`@` → `%40`)

---

### ❌ "SECRET_KEY not set"

**Solution** :
1. Générez une clé :
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
2. Ajoutez-la dans Environment comme `SECRET_KEY`

---

### ❌ "DisallowedHost"

**Solution** :
1. Dans Environment, ajoutez/modifiez `ALLOWED_HOSTS`
2. Valeur : `votre-app.onrender.com` (remplacez par votre URL Render)

---

## ✅ Checklist Express

Avant de redéployer :

- [ ] Logs lus et erreur identifiée
- [ ] 4 variables d'environnement configurées
- [ ] Build Command correct
- [ ] Start Command correct
- [ ] `requirements.txt` à jour

---

## 🚀 Redéployer

1. Dans Render > Web Service
2. Cliquez sur **"Manual Deploy"** > **"Deploy latest commit"**
3. Surveillez les logs

---

## 📞 Besoin d'Aide ?

**Dites-moi** :
1. Quelle erreur voyez-vous dans les logs ?
2. Les 4 variables sont-elles configurées ?
3. Avez-vous créé une base PostgreSQL dans Render ?

Je vous aiderai à résoudre le problème précisément ! 🔧

