# 🔧 Résolution : Problème de connexion GitHub-Railway

## 🔍 Diagnostic du problème

Il peut y avoir plusieurs raisons pour lesquelles Railway ne peut pas se connecter à GitHub :

1. **Le repository GitHub n'existe pas ou n'est pas accessible**
2. **Le remote Git n'est pas correctement configuré**
3. **Railway n'a pas les permissions d'accès à votre repository**
4. **Le repository est privé et Railway n'y a pas accès**

---

## ✅ Solution 1 : Vérifier que le repository GitHub existe

1. Allez sur **https://github.com**
2. Connectez-vous à votre compte
3. Vérifiez que vous voyez le repository `fmos-mfmc` dans votre liste de repositories
4. Cliquez dessus pour vérifier qu'il contient bien vos fichiers

**Si le repository n'existe pas :**
- Créez-le maintenant sur GitHub
- Suivez les instructions dans `ETAPE_2_CONNEXION_GITHUB.md`

---

## ✅ Solution 2 : Vérifier la configuration Git locale

Ouvrez PowerShell dans votre projet et exécutez :

```powershell
git remote -v
```

Vous devriez voir quelque chose comme :
```
origin  https://github.com/VOTRE_USERNAME/fmos-mfmc.git (fetch)
origin  https://github.com/VOTRE_USERNAME/fmos-mfmc.git (push)
```

**Si vous voyez "VOTRE_USERNAME" au lieu de votre vrai nom d'utilisateur :**
- Le remote n'est pas correctement configuré
- Suivez la Solution 3 ci-dessous

---

## ✅ Solution 3 : Reconfigurer le remote Git

### Étape 1 : Trouver votre nom d'utilisateur GitHub

1. Allez sur https://github.com
2. Cliquez sur votre photo de profil (en haut à droite)
3. Votre nom d'utilisateur est affiché (ex: `john-doe`)

### Étape 2 : Supprimer l'ancien remote (si nécessaire)

```powershell
git remote remove origin
```

### Étape 3 : Ajouter le bon remote

**Remplacez `VOTRE_USERNAME` par votre vrai nom d'utilisateur GitHub :**

```powershell
git remote add origin https://github.com/VOTRE_USERNAME/fmos-mfmc.git
```

### Étape 4 : Vérifier

```powershell
git remote -v
```

Vous devriez maintenant voir votre vrai nom d'utilisateur.

### Étape 5 : Pousser le code

```powershell
git push -u origin main
```

Si GitHub vous demande de vous authentifier :
- Utilisez un **Personal Access Token** (recommandé)
- Ou votre mot de passe GitHub (si les tokens ne sont pas activés)

---

## ✅ Solution 4 : Créer un Personal Access Token GitHub

Si GitHub vous demande une authentification :

1. Allez sur GitHub > **Settings** (votre profil) > **Developer settings**
2. Cliquez sur **Personal access tokens** > **Tokens (classic)**
3. Cliquez sur **Generate new token** > **Generate new token (classic)**
4. Donnez un nom : `Railway Deployment`
5. Cochez la case **`repo`** (accès complet aux repositories)
6. Cliquez sur **Generate token**
7. **COPIEZ LE TOKEN** (vous ne le reverrez plus !)
8. Quand Git vous demande le mot de passe, utilisez ce token au lieu de votre mot de passe

---

## ✅ Solution 5 : Autoriser Railway à accéder à GitHub

### Méthode 1 : Via Railway Dashboard

1. Allez sur **https://railway.app**
2. Cliquez sur **"Login"** ou **"Start a New Project"**
3. Sélectionnez **"Login with GitHub"**
4. Autorisez Railway à accéder à vos repositories
5. Cochez la case pour autoriser l'accès à **tous vos repositories** ou seulement `fmos-mfmc`

### Méthode 2 : Vérifier les permissions GitHub

1. Allez sur GitHub > **Settings** > **Applications** > **Authorized OAuth Apps**
2. Cherchez **Railway**
3. Vérifiez que Railway a accès à vos repositories
4. Si nécessaire, cliquez sur Railway et modifiez les permissions

---

## ✅ Solution 6 : Vérifier que le code est bien sur GitHub

1. Allez sur `https://github.com/VOTRE_USERNAME/fmos-mfmc`
2. Vérifiez que vous voyez :
   - Le fichier `manage.py`
   - Le dossier `apps/`
   - Le dossier `core/`
   - Le fichier `requirements.txt`
   - Le fichier `Procfile`

**Si les fichiers ne sont pas là :**

```powershell
# Vérifier le statut
git status

# Si vous avez des modifications non commitées
git add .
git commit -m "Mise à jour avant déploiement"

# Pousser sur GitHub
git push origin main
```

---

## 🎯 Étapes à suivre maintenant

1. **Vérifiez que votre repository GitHub existe** et contient vos fichiers
2. **Vérifiez votre configuration Git locale** avec `git remote -v`
3. **Si nécessaire, reconfigurez le remote** avec votre vrai nom d'utilisateur
4. **Poussez le code** sur GitHub avec `git push origin main`
5. **Autorisez Railway** à accéder à GitHub lors de la connexion
6. **Essayez de créer le projet Railway** à nouveau

---

## 💡 Astuce : Utiliser l'URL SSH (alternative)

Si HTTPS ne fonctionne pas, vous pouvez utiliser SSH :

```powershell
# Supprimer l'ancien remote
git remote remove origin

# Ajouter avec SSH (remplacez VOTRE_USERNAME)
git remote add origin git@github.com:VOTRE_USERNAME/fmos-mfmc.git

# Pousser
git push -u origin main
```

**Note** : Pour SSH, vous devez avoir configuré une clé SSH sur GitHub.

---

## 🆘 Besoin d'aide supplémentaire ?

Dites-moi :
1. **Quel est votre nom d'utilisateur GitHub ?** (pour vérifier la configuration)
2. **Quel message d'erreur voyez-vous exactement ?** (dans Railway ou GitHub)
3. **À quelle étape êtes-vous bloqué ?** (connexion Railway, push Git, etc.)

Je pourrai vous aider plus précisément avec ces informations !

