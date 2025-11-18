# 🔧 Configurer le fichier .env avec Supabase

## 📍 Où mettre l'URL de connexion Supabase

Vous avez **2 options** pour configurer votre URL Supabase :

---

## ✅ Option 1 : Utiliser DATABASE_URL (Recommandé)

C'est la méthode la plus simple et celle que votre projet utilise déjà !

### Étape 1 : Créer le fichier .env

Créez un fichier `.env` à la racine de votre projet (à côté de `manage.py`).

### Étape 2 : Ajouter l'URL Supabase

Ouvrez le fichier `.env` et ajoutez :

```env
DATABASE_URL=postgresql://postgres:VOTRE_MOT_DE_PASSE@db.xxxxx.supabase.co:5432/postgres
```

**Remplacez** :
- `VOTRE_MOT_DE_PASSE` par votre mot de passe Supabase
- `db.xxxxx.supabase.co` par votre host Supabase
- `5432` par le port (généralement 5432 pour Direct connection)

**Exemple** :
```env
DATABASE_URL=postgresql://postgres:MonMotDePasse123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

### Étape 3 : Vérifier que ça fonctionne

Testez la connexion :

```bash
python manage.py check --database default
```

Si tout est OK, vous verrez :
```
System check identified no issues (0 silenced).
```

---

## ✅ Option 2 : Utiliser les variables séparées

Si vous préférez utiliser des variables séparées au lieu de DATABASE_URL :

### Étape 1 : Créer le fichier .env

Créez un fichier `.env` à la racine de votre projet.

### Étape 2 : Ajouter les variables

```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=VOTRE_MOT_DE_PASSE
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432
```

**Remplacez** :
- `VOTRE_MOT_DE_PASSE` par votre mot de passe Supabase
- `db.xxxxx.supabase.co` par votre host Supabase

**Exemple** :
```env
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=MonMotDePasse123
DB_HOST=db.abcdefghijklmnop.supabase.co
DB_PORT=5432
```

---

## 🔒 Sécurité importante

⚠️ **Le fichier `.env` est déjà dans `.gitignore`**, donc il ne sera **PAS** envoyé sur GitHub. C'est parfait pour la sécurité !

---

## 📝 Structure du fichier .env complet

Voici un exemple complet de fichier `.env` :

```env
# Clé secrète Django
SECRET_KEY=votre-cle-secrete-django-tres-longue-et-aleatoire

# Mode debug
DEBUG=True

# Hôtes autorisés
ALLOWED_HOSTS=127.0.0.1,localhost

# URL de connexion Supabase
DATABASE_URL=postgresql://postgres:MonMotDePasse123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

---

## 🧪 Tester la connexion

Une fois que vous avez créé le fichier `.env` avec votre URL Supabase :

### Test 1 : Vérifier la configuration

```bash
python manage.py check --database default
```

### Test 2 : Créer les migrations (si nécessaire)

```bash
python manage.py makemigrations
```

### Test 3 : Appliquer les migrations

```bash
python manage.py migrate
```

Si tout fonctionne, vous verrez les migrations s'appliquer à votre base Supabase !

---

## 🆘 Problèmes courants

### Erreur : "could not connect to server"

**Solution** :
1. Vérifiez que votre URL est correcte
2. Vérifiez que vous avez utilisé le bon mot de passe
3. Vérifiez que vous avez choisi "Direct connection" (port 5432) dans Supabase

### Erreur : "password authentication failed"

**Solution** :
1. Réinitialisez votre mot de passe dans Supabase (Settings > Database > Reset database password)
2. Mettez à jour votre `.env` avec le nouveau mot de passe

### Erreur : "module 'dj_database_url' has no attribute 'parse'"

**Solution** :
```bash
pip install dj-database-url
```

---

## ✅ Prochaines étapes

Une fois que votre `.env` est configuré :

1. ✅ Testez la connexion
2. ✅ Appliquez les migrations : `python manage.py migrate`
3. ✅ Créez un superutilisateur : `python manage.py createsuperuser`
4. ✅ Lancez le serveur : `python manage.py runserver`

---

## 💡 Pour le déploiement

Quand vous déploierez votre site (sur Railway, Render, etc.), vous devrez configurer la variable d'environnement `DATABASE_URL` directement dans l'interface de la plateforme, pas dans un fichier `.env`.

Le fichier `.env` est uniquement pour le développement local !

