# 🔍 Trouver les informations de connexion Supabase (Méthode correcte)

## ✅ Méthode correcte selon l'interface Supabase actuelle

### Étape 1 : Accéder aux paramètres Database

1. Dans votre projet Supabase, cliquez sur l'icône **⚙️ Settings** (en bas à gauche)
2. Dans le menu de gauche, cliquez sur **"Database"**

### Étape 2 : Trouver "Connection Info"

1. Dans la page Database, cherchez une section appelée **"Connection Info"** ou **"Connection parameters"**
2. Vous devriez voir un bouton **"Connect"** ou **"Connection string"**
3. **Cliquez sur ce bouton**

### Étape 3 : Choisir le type de connexion

Quand vous cliquez sur "Connect", vous verrez plusieurs options :

#### Option 1 : Direct connection (Recommandé pour Django)
- **Port** : `5432`
- **Utilisation** : Serveurs persistants (comme Django)
- **URL ressemble à** : `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`

#### Option 2 : Pooler session mode
- **Port** : `5432` (via proxy)
- **Utilisation** : Environnements IPv4

#### Option 3 : Pooler transaction mode
- **Port** : `6543` (via proxy)
- **Utilisation** : Serverless/Edge functions

**Pour Django, utilisez l'Option 1 (Direct connection) !**

### Étape 4 : Récupérer l'URL

1. Vous verrez une URL avec `[YOUR-PASSWORD]`
2. **Remplacez `[YOUR-PASSWORD]`** par votre mot de passe Supabase
3. **Copiez l'URL complète**

**Exemple** :
```
postgresql://postgres:MonMotDePasse123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

---

## 🔑 Si vous ne connaissez pas votre mot de passe

1. Dans **Settings** > **Database**
2. Cherchez **"Database password"** ou **"Reset database password"**
3. Cliquez sur **"Reset database password"**
4. **Notez le nouveau mot de passe** (vous ne le reverrez plus !)
5. Utilisez ce nouveau mot de passe dans votre URL

---

## 📸 Description de l'interface

Dans Settings > Database, vous devriez voir quelque chose comme :

```
┌─────────────────────────────────────┐
│  Database Settings                   │
├─────────────────────────────────────┤
│                                      │
│  Connection Info                    │
│  ┌─────────────────────────────┐   │
│  │  [Connect] ← Cliquez ici !  │   │
│  └─────────────────────────────┘   │
│                                      │
│  Database password                  │
│  [Reset database password]          │
│                                      │
└─────────────────────────────────────┘
```

Quand vous cliquez sur "Connect", vous verrez :

```
┌─────────────────────────────────────┐
│  Connect to your database            │
├─────────────────────────────────────┤
│                                      │
│  Direct connection                  │
│  postgresql://postgres:[PASSWORD]@  │
│  db.xxxxx.supabase.co:5432/postgres │
│                                      │
│  Pooler session mode                 │
│  ...                                 │
│                                      │
│  Pooler transaction mode             │
│  ...                                 │
│                                      │
└─────────────────────────────────────┘
```

---

## 🎯 Informations à récupérer

Une fois que vous avez cliqué sur "Connect" et choisi "Direct connection", vous avez besoin de :

1. **L'URL complète** avec votre mot de passe
2. Ou les informations séparées :
   - **Host** : `db.xxxxx.supabase.co`
   - **Database** : `postgres`
   - **Port** : `5432`
   - **User** : `postgres`
   - **Password** : Votre mot de passe

---

## 💡 Alternative : Construire l'URL manuellement

Si vous voyez les informations séparées mais pas l'URL complète, construisez-la ainsi :

```
postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

**Exemple** :
```
postgresql://postgres:MonMotDePasse123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

---

## 🆘 Si vous ne voyez toujours pas "Connection Info"

Dites-moi :
1. **Que voyez-vous exactement** dans Settings > Database ?
2. **Y a-t-il des sections** comme "General", "Connection pooling", "Backups" ?
3. **Y a-t-il un bouton** "Connect" ou "Connection string" quelque part ?

Je pourrai vous guider plus précisément !

---

## ✅ Une fois que vous avez l'URL

Vous pourrez l'utiliser comme variable `DATABASE_URL` dans votre déploiement Django !

