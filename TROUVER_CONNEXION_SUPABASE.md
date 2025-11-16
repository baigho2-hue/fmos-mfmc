# 🔍 Comment trouver les informations de connexion Supabase

## 📍 Où chercher dans Supabase

L'interface Supabase peut varier. Voici tous les endroits possibles :

---

## Méthode 1 : Settings > Database > Connection Info

1. Dans votre projet Supabase, cliquez sur l'icône **⚙️ Settings** (en bas à gauche de l'écran)
2. Dans le menu de gauche, cliquez sur **"Database"**
3. Cherchez une section appelée :
   - **"Connection Info"**
   - **"Connection parameters"**
   - **"Database settings"**
   - **"Connection pooling"**

Vous devriez voir des informations comme :
- **Host** : `db.xxxxx.supabase.co`
- **Database name** : `postgres`
- **Port** : `5432` ou `6543`
- **User** : `postgres`
- **Password** : (masqué, mais vous pouvez le réinitialiser)

---

## Méthode 2 : Settings > Database > Connection Pooling

1. Allez dans **Settings** > **Database**
2. Cherchez l'onglet **"Connection Pooling"**
3. Vous verrez une URL de connexion avec le port **6543**

---

## Méthode 3 : API Settings

1. Allez dans **Settings** > **API**
2. Cherchez la section **"Database"** ou **"Connection"**
3. Les informations peuvent être là

---

## Méthode 4 : Table Editor (indirect)

1. Allez dans **Table Editor** (menu de gauche)
2. Si vous voyez déjà des tables, cela signifie que la connexion fonctionne
3. Les informations sont dans Settings > Database

---

## Méthode 5 : Utiliser les informations séparées

Si vous ne trouvez pas l'URL complète, utilisez les informations séparées :

### Étape 1 : Trouver le Host

1. Allez dans **Settings** > **Database**
2. Cherchez **"Host"** ou **"Connection string"**
3. Vous devriez voir quelque chose comme : `db.abcdefghijklmnop.supabase.co`

### Étape 2 : Construire l'URL manuellement

Une fois que vous avez toutes les informations, construisez l'URL :

```
postgresql://postgres:VOTRE_MOT_DE_PASSE@HOST:5432/postgres
```

**Exemple** :
```
postgresql://postgres:MonMotDePasse123@db.abcdefghijklmnop.supabase.co:5432/postgres
```

---

## Méthode 6 : Réinitialiser le mot de passe

Si vous ne vous souvenez plus du mot de passe :

1. Allez dans **Settings** > **Database**
2. Cherchez **"Database password"** ou **"Reset database password"**
3. Cliquez sur **"Reset password"** ou **"Generate new password"**
4. **Notez le nouveau mot de passe** (vous ne le reverrez plus !)

---

## 📸 À quoi ressemble l'interface Supabase

L'interface Supabase ressemble généralement à ceci :

```
┌─────────────────────────────────────┐
│  Supabase Logo                      │
├─────────────────────────────────────┤
│  [Table Editor] [SQL Editor]        │
│  [Authentication] [Storage]          │
│  [Settings] ⚙️  ← Cliquez ici !    │
└─────────────────────────────────────┘
```

Dans Settings, vous verrez :
```
┌─────────────────────────────────────┐
│  Settings                            │
├─────────────────────────────────────┤
│  [General]                           │
│  [API]                                │
│  [Database] ← Cliquez ici !          │
│  [Auth]                               │
│  [Storage]                            │
└─────────────────────────────────────┘
```

Dans Database, vous devriez voir :
```
┌─────────────────────────────────────┐
│  Database Settings                   │
├─────────────────────────────────────┤
│  Connection Info                     │
│  Host: db.xxxxx.supabase.co         │
│  Database: postgres                  │
│  Port: 5432                          │
│  User: postgres                      │
│                                      │
│  Connection Pooling                  │
│  [Onglet avec URL]                   │
└─────────────────────────────────────┘
```

---

## 🆘 Si vous ne trouvez toujours pas

### Option A : Utiliser l'API Supabase

1. Allez dans **Settings** > **API**
2. Cherchez **"Project URL"** ou **"Project API keys"**
3. L'URL de l'API contient souvent le même domaine que la base de données

**Exemple** :
- Si votre API URL est : `https://abcdefghijklmnop.supabase.co`
- Alors votre DB Host est probablement : `db.abcdefghijklmnop.supabase.co`

### Option B : Contacter le support Supabase

1. Allez sur https://supabase.com/dashboard/support
2. Créez un ticket de support
3. Demandez les informations de connexion PostgreSQL

### Option C : Vérifier les emails Supabase

Quand vous avez créé le projet, Supabase vous a peut-être envoyé un email avec les informations de connexion.

---

## 💡 Astuce : Utiliser Supabase CLI

Si vous avez Node.js installé :

```bash
# Installer Supabase CLI
npm install -g supabase

# Se connecter
supabase login

# Lier votre projet
supabase link --project-ref votre-project-ref

# Obtenir les informations de connexion
supabase db connection-string
```

---

## 🎯 Informations dont vous avez besoin

Pour configurer Django, vous avez besoin de :

1. **Host** : `db.xxxxx.supabase.co`
2. **Database name** : `postgres` (généralement)
3. **Port** : `5432` (ou `6543` pour pooling)
4. **User** : `postgres` (généralement)
5. **Password** : Le mot de passe que vous avez créé lors de la création du projet

Une fois que vous avez ces informations, construisez l'URL :

```
postgresql://postgres:VOTRE_MOT_DE_PASSE@HOST:5432/postgres
```

---

## 🆘 Besoin d'aide supplémentaire ?

Dites-moi :
1. **Que voyez-vous exactement** dans Settings > Database ?
2. **Y a-t-il des onglets** dans la section Database ?
3. **Voyez-vous des informations** comme Host, Port, Database name ?

Je pourrai vous guider plus précisément avec ces informations !

