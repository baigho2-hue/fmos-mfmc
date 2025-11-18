# Configuration de Render MCP Server avec Cursor

Ce guide vous explique comment connecter Render MCP Server à Cursor pour gérer votre infrastructure Render directement depuis l'éditeur.

## Prérequis

1. Un compte Render actif
2. Cursor installé sur votre système
3. Une clé API Render

## Étapes de configuration

### 1. Obtenir votre clé API Render

1. Connectez-vous à votre compte Render : https://dashboard.render.com
2. Cliquez sur votre profil en haut à droite
3. Allez dans **Account Settings** → **API Keys**
4. Cliquez sur **New API Key**
5. Donnez un nom à votre clé (ex: "Cursor MCP")
6. Copiez la clé API générée (vous ne pourrez la voir qu'une seule fois)

### 2. Configurer Cursor

Le fichier de configuration MCP de Cursor se trouve à :
- **Windows** : `%USERPROFILE%\.cursor\mcp.json`
- **macOS/Linux** : `~/.cursor/mcp.json`

#### Option A : Configuration manuelle

Ouvrez le fichier `mcp.json` et ajoutez la configuration suivante :

```json
{
  "mcpServers": {
    "supabase": {
      "url": "https://mcp.supabase.com/mcp?project_ref=bmfkvwpfeuyserrfrqjb",
      "headers": {}
    },
    "render": {
      "url": "https://mcp.render.com/mcp",
      "headers": {
        "Authorization": "Bearer VOTRE_CLE_API_RENDER"
      }
    }
  }
}
```

**Important** : Remplacez `VOTRE_CLE_API_RENDER` par votre vraie clé API Render.

#### Option B : Utiliser le script PowerShell

Exécutez le script `configurer_render_mcp.ps1` avec votre clé API :

```powershell
.\scripts\configurer_render_mcp.ps1 -ApiKey "votre_cle_api_render"
```

### 3. Redémarrer Cursor

Après avoir modifié le fichier de configuration :
1. Fermez complètement Cursor
2. Rouvrez Cursor
3. La connexion à Render MCP Server devrait être active

### 4. Vérifier la connexion

Dans Cursor, ouvrez le chat AI et testez avec des commandes comme :
- "Liste mes services Render"
- "Montre-moi les logs de mon service fmos-mfmc"
- "Quel est le statut de mon déploiement Render ?"

## Utilisation

Une fois configuré, vous pouvez utiliser Render MCP Server pour :

- **Gérer vos services** : Lister, créer, modifier, supprimer des services
- **Voir les logs** : Accéder aux logs de déploiement et d'application
- **Gérer les variables d'environnement** : Ajouter, modifier, supprimer des variables
- **Surveiller les déploiements** : Vérifier le statut des déploiements en cours
- **Gérer les bases de données** : Créer, configurer, sauvegarder des bases de données

## Exemples de commandes

```
Liste tous mes services Render
Montre-moi les logs récents de fmos-mfmc
Crée une nouvelle variable d'environnement DEBUG=True pour fmos-mfmc
Quel est le statut de ma base de données fmos-mfmc-db ?
```

## Dépannage

### La connexion ne fonctionne pas

1. Vérifiez que votre clé API est correcte
2. Vérifiez que le fichier `mcp.json` est bien formaté (JSON valide)
3. Redémarrez Cursor complètement
4. Vérifiez les logs de Cursor pour les erreurs

### Erreur "Unauthorized"

- Votre clé API est peut-être expirée ou invalide
- Générez une nouvelle clé API sur Render
- Mettez à jour le fichier `mcp.json`

## Documentation officielle

- [Render MCP Server Documentation](https://render.com/docs/mcp-server)
- [Cursor MCP Documentation](https://docs.cursor.com/mcp)

