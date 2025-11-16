# 🗄️ Créer une base de données PostgreSQL sur Railway

## 📍 Où trouver l'option pour créer une base de données

L'interface Railway peut varier légèrement. Voici plusieurs façons de créer une base PostgreSQL :

---

## Méthode 1 : Via le menu "+ New" (interface classique)

1. Dans votre projet Railway, regardez en haut à droite
2. Cherchez un bouton **"+ New"** ou **"+ Add"** ou **"New Service"**
3. Cliquez dessus
4. Dans le menu déroulant, sélectionnez **"Database"**
5. Choisissez **"PostgreSQL"**

---

## Méthode 2 : Via le menu latéral (interface récente)

1. Dans votre projet Railway, regardez le menu de gauche
2. Cherchez une section **"Services"** ou **"Resources"**
3. Cliquez sur **"+ New"** à côté de cette section
4. Sélectionnez **"Database"** > **"PostgreSQL"**

---

## Méthode 3 : Via le template (recommandé)

1. Dans votre projet Railway, cliquez sur **"New"** (en haut)
2. Sélectionnez **"Template"** ou **"Add Service"**
3. Cherchez **"PostgreSQL"** dans les templates disponibles
4. Cliquez sur **"Deploy"** ou **"Add"**

---

## Méthode 4 : Depuis le service web Django

1. Cliquez sur votre service web Django (celui qui contient votre application)
2. Allez dans l'onglet **"Variables"**
3. Cherchez une section **"Add Database"** ou **"Connect Database"**
4. Cliquez dessus pour ajouter PostgreSQL

---

## Méthode 5 : Via le dashboard principal

1. Retournez au dashboard principal de Railway (cliquez sur le logo Railway en haut)
2. Cliquez sur votre projet `fmos-mfmc`
3. Dans la vue d'ensemble du projet, cherchez un bouton **"Add Service"** ou **"+ New"**
4. Sélectionnez **"Database"** > **"PostgreSQL"**

---

## ⚠️ Si vous ne voyez toujours pas l'option

### Vérification 1 : Vérifiez votre plan Railway

- Railway offre un plan gratuit avec des limites
- Assurez-vous que votre compte est actif
- Vérifiez que vous n'avez pas atteint la limite de services

### Vérification 2 : Interface différente

L'interface Railway peut avoir changé. Essayez :

1. **Actualisez la page** (F5 ou Ctrl+R)
2. **Déconnectez-vous et reconnectez-vous**
3. **Vérifiez que vous êtes bien dans le bon projet**

### Vérification 3 : Utiliser Railway CLI (alternative)

Si l'interface web ne fonctionne pas, vous pouvez utiliser la CLI :

```bash
# Installer Railway CLI
npm install -g @railway/cli

# Se connecter
railway login

# Aller dans votre projet
railway link

# Créer une base PostgreSQL
railway add postgresql
```

---

## 🎯 Ce que vous devriez voir après création

Une fois la base PostgreSQL créée, vous verrez :

1. **Un nouveau service** dans votre projet (à côté de votre service Django)
2. **Des variables automatiques** créées :
   - `DATABASE_URL` (celle-ci est importante !)
   - `PGHOST`
   - `PGPORT`
   - `PGUSER`
   - `PGPASSWORD`
   - `PGDATABASE`

---

## 💡 Astuce : Vérifier si la base existe déjà

Parfois Railway crée automatiquement une base de données. Vérifiez :

1. Dans votre projet Railway, regardez la liste des **services**
2. Cherchez un service nommé **"Postgres"** ou **"PostgreSQL"**
3. Si vous en voyez un, c'est que la base existe déjà !

---

## 📸 Description de l'interface Railway

L'interface Railway ressemble généralement à ceci :

```
┌─────────────────────────────────────┐
│  Railway Logo    [Projet] [+ New]   │
├─────────────────────────────────────┤
│                                     │
│  Services:                          │
│  ┌─────────────┐                   │
│  │ Django App  │  ← Votre app      │
│  └─────────────┘                   │
│                                     │
│  [+ New]  ← Cliquez ici !          │
│                                     │
└─────────────────────────────────────┘
```

---

## 🆘 Besoin d'aide supplémentaire ?

Dites-moi :
1. **Qu'est-ce que vous voyez exactement** dans votre interface Railway ?
2. **Y a-t-il déjà un service PostgreSQL** dans votre projet ?
3. **Quels boutons/menus voyez-vous** en haut de la page ?

Je pourrai vous guider plus précisément avec ces informations !

---

## ✅ Alternative : Utiliser une base externe

Si Railway ne vous permet pas de créer une base PostgreSQL (limite du plan gratuit), vous pouvez :

1. **Utiliser Supabase** (gratuit) : https://supabase.com
2. **Utiliser Neon** (gratuit) : https://neon.tech
3. **Utiliser ElephantSQL** (gratuit) : https://www.elephantsql.com

Ensuite, configurez simplement la variable `DATABASE_URL` dans Railway avec l'URL de connexion fournie.

