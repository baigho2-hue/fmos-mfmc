# 🔧 Corriger la configuration Git pour GitHub

## Problème détecté

Votre remote Git est configuré avec `VOTRE_USERNAME` au lieu de votre vrai nom d'utilisateur GitHub.

## Solution : Reconfigurer le remote

### Étape 1 : Trouver votre nom d'utilisateur GitHub

1. Allez sur **https://github.com**
2. Connectez-vous
3. Cliquez sur votre photo de profil (en haut à droite)
4. Votre nom d'utilisateur est affiché dans l'URL ou sous votre nom

**Exemple** : Si l'URL est `https://github.com/john-doe`, alors votre nom d'utilisateur est `john-doe`

### Étape 2 : Reconfigurer le remote

**Remplacez `VOTRE_VRAI_USERNAME` par votre nom d'utilisateur GitHub réel :**

```powershell
git remote add origin https://github.com/VOTRE_VRAI_USERNAME/fmos-mfmc.git
```

**Exemple** : Si votre nom d'utilisateur est `john-doe` :
```powershell
git remote add origin https://github.com/john-doe/fmos-mfmc.git
```

### Étape 3 : Vérifier

```powershell
git remote -v
```

Vous devriez maintenant voir votre vrai nom d'utilisateur.

### Étape 4 : Pousser le code sur GitHub

```powershell
git push -u origin main
```

**Si GitHub vous demande de vous authentifier :**

1. **Nom d'utilisateur** : Entrez votre nom d'utilisateur GitHub
2. **Mot de passe** : Utilisez un **Personal Access Token** (pas votre mot de passe)

#### Créer un Personal Access Token :

1. Allez sur GitHub > **Settings** (votre profil) > **Developer settings**
2. **Personal access tokens** > **Tokens (classic)**
3. **Generate new token** > **Generate new token (classic)**
4. Nom : `Railway Deployment`
5. Cochez **`repo`** (accès complet aux repositories)
6. **Generate token**
7. **COPIEZ LE TOKEN** (vous ne le reverrez plus !)
8. Utilisez ce token comme mot de passe quand Git vous le demande

---

## Après avoir corrigé

Une fois que le code est poussé sur GitHub avec le bon nom d'utilisateur :

1. Allez sur Railway
2. Créez un nouveau projet
3. Sélectionnez "Deploy from GitHub repo"
4. Vous devriez maintenant voir votre repository `fmos-mfmc` dans la liste !

---

**Dites-moi votre nom d'utilisateur GitHub et je peux vous donner la commande exacte à exécuter !**

