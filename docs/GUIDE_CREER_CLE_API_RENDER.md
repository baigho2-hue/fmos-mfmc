# Guide : Créer une clé API Render

## Étapes détaillées

### 1. Connectez-vous à Render

1. Ouvrez votre navigateur
2. Allez sur : **https://dashboard.render.com**
3. Connectez-vous avec votre compte Render

### 2. Accéder aux paramètres de l'API

1. Une fois connecté, cliquez sur votre **nom d'utilisateur** ou **avatar** en haut à droite
2. Dans le menu déroulant, cliquez sur **"Account Settings"** ou **"Paramètres du compte"**

### 3. Créer une nouvelle clé API

1. Dans le menu de gauche, cherchez la section **"API Keys"** ou **"Clés API"**
2. Cliquez sur **"New API Key"** ou **"Nouvelle clé API"**
3. Donnez un nom à votre clé, par exemple :
   - `Cursor MCP`
   - `FMOS MFMC Cursor`
   - `Development API Key`
4. Cliquez sur **"Create API Key"** ou **"Créer la clé API"**

### 4. Copier la clé API

⚠️ **IMPORTANT** : La clé API ne sera affichée qu'une seule fois !

1. **Copiez immédiatement** la clé API qui s'affiche
2. Collez-la dans un endroit sûr (bloc-notes, gestionnaire de mots de passe)
3. La clé ressemble à : `rnd_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 5. Notez votre clé API

Une fois que vous avez votre clé API, vous pouvez :
- La coller directement dans le script PowerShell
- Ou me la donner et je configurerai le fichier pour vous

## Sécurité

- ⚠️ Ne partagez jamais votre clé API publiquement
- ⚠️ Ne commitez jamais votre clé API dans Git
- ⚠️ Si vous perdez votre clé, vous pouvez en créer une nouvelle et supprimer l'ancienne

## Prochaines étapes

Une fois que vous avez votre clé API :
1. Exécutez le script : `.\scripts\configurer_render_mcp.ps1 -ApiKey "votre_cle"`
2. Ou ouvrez le fichier `%USERPROFILE%\.cursor\mcp.json` et remplacez `VOTRE_CLE_API_RENDER`

