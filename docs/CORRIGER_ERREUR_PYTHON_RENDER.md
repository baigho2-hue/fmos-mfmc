# 🔧 Correction : Python 3.13 au lieu de 3.11.0 sur Render

## 🔍 Problème

Render utilise Python 3.13 au lieu de Python 3.11.0 spécifié dans `runtime.txt`, ce qui cause l'erreur :

```
ModuleNotFoundError: No module named 'settings'
```

---

## ✅ Solution

### Étape 1 : Vérifier runtime.txt

Assurez-vous que `runtime.txt` contient exactement :

```
python-3.11.0
```

**Important** : Pas d'espaces supplémentaires, pas de ligne vide après.

### Étape 2 : Configurer dans Render Dashboard

1. Allez dans votre **Web Service** sur Render
2. Cliquez sur **"Settings"**
3. Dans **"Python Version"**, sélectionnez **"3.11.0"** (ou la version spécifiée dans runtime.txt)
4. Cliquez sur **"Save Changes"**

### Étape 3 : Ajouter DJANGO_SETTINGS_MODULE

Dans **Environment Variables**, ajoutez :

- **Key** : `DJANGO_SETTINGS_MODULE`
- **Value** : `core.settings`

### Étape 4 : Redéployer

1. Cliquez sur **"Manual Deploy"** > **"Deploy latest commit"**
2. Surveillez les logs pour vérifier que Python 3.11.0 est utilisé

---

## 🔍 Vérification dans les Logs

Après le redéploiement, vérifiez dans les logs que vous voyez :

```
Python 3.11.0
```

Et non :

```
Python 3.13
```

---

## 📝 Note Importante

Si Render continue d'utiliser Python 3.13 :

1. **Supprimez et recréez le service** avec la bonne version
2. **Ou utilisez render.yaml** qui force la version Python via `PYTHON_VERSION`

---

## 🚀 Utilisation de render.yaml

Le fichier `render.yaml` a été mis à jour pour inclure :

```yaml
envVars:
  - key: PYTHON_VERSION
    value: 3.11.0
  - key: DJANGO_SETTINGS_MODULE
    value: core.settings
```

Cela garantit que la bonne version de Python est utilisée.

