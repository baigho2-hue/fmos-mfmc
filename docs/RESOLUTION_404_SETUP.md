# 🔧 Résolution : Erreur 404 sur /setup/

Si vous obtenez une erreur 404 en accédant à `/setup/?token=...`, voici comment résoudre le problème.

---

## 🔍 Causes Possibles

1. **Le code n'a pas été poussé sur GitHub**
2. **Render n'a pas redéployé avec les dernières modifications**
3. **Les routes setup ne sont pas dans le code déployé**

---

## ✅ Solution 1 : Vérifier et Pousser le Code

### Étape 1 : Vérifier les Modifications Locales

Dans votre terminal local :

```bash
git status
```

Vous devriez voir `core/urls.py` et `core/views_setup.py` dans les fichiers modifiés.

### Étape 2 : Ajouter et Commiter les Fichiers

```bash
git add core/urls.py core/views_setup.py core/wsgi.py core/startup.py
git commit -m "Ajout des vues setup pour initialisation Render"
```

### Étape 3 : Pousser sur GitHub

```bash
git push origin main
```

(ou `git push origin master` si votre branche principale s'appelle `master`)

### Étape 4 : Attendre le Redéploiement Render

1. Allez sur [render.com](https://render.com)
2. Cliquez sur votre **Web Service** `fmos-mfmc`
3. Vous devriez voir un nouveau déploiement en cours
4. Attendez que le déploiement soit terminé (2-5 minutes)

### Étape 5 : Réessayer

Une fois le déploiement terminé, réessayez d'accéder à :
```
https://fmos-mfmc.onrender.com/setup/?token=FMOS2024ConfigSecret!
```

---

## ✅ Solution 2 : Vérifier les Routes dans Render

Si le code est bien poussé mais que ça ne fonctionne toujours pas :

### Vérifier les Logs Render

1. Dans Render > Web Service > **Logs**
2. Cherchez des erreurs liées à `views_setup` ou `setup`
3. Vérifiez s'il y a des erreurs d'import

### Vérifier que les Fichiers sont Présents

Dans les logs de build Render, vérifiez que :
- `core/views_setup.py` est présent
- `core/urls.py` contient les routes setup

---

## ✅ Solution 3 : Redéployer Manuellement

Si Render n'a pas détecté les changements :

1. Dans Render > Web Service
2. Cliquez sur **"Manual Deploy"**
3. Sélectionnez **"Deploy latest commit"**
4. Attendez le redéploiement
5. Réessayez l'accès à `/setup/`

---

## ✅ Solution 4 : Vérifier la Configuration

### Vérifier que SETUP_SECRET_TOKEN est Défini

1. Dans Render > Web Service > **Environment**
2. Vérifiez que `SETUP_SECRET_TOKEN` est présent
3. Vérifiez que la valeur correspond à celle dans votre URL

### Vérifier les Routes dans le Code

Assurez-vous que `core/urls.py` contient :

```python
from core import views_setup

urlpatterns = [
    # ... autres routes ...
    path('setup/', views_setup.setup_dashboard, name='setup_dashboard'),
    path('setup/migrate/', views_setup.setup_migrate, name='setup_migrate'),
    path('setup/create-superuser/', views_setup.setup_create_superuser, name='setup_create_superuser'),
    path('setup/init-programme/', views_setup.setup_init_programme, name='setup_init_programme'),
    path('setup/status/', views_setup.setup_status, name='setup_status'),
]
```

---

## 🆘 Si Rien ne Fonctionne

### Alternative : Utiliser les Migrations Automatiques

Les migrations sont maintenant appliquées automatiquement au démarrage grâce à `core/startup.py`.

Vous pouvez :

1. **Créer le superutilisateur via l'admin Django** (si accessible) :
   - Allez sur `/admin/`
   - Si vous pouvez accéder, créez un superutilisateur via l'interface Django

2. **Utiliser une commande de gestion personnalisée** :
   - Créez un script Python local qui se connecte à votre base Render
   - Exécutez les commandes nécessaires

3. **Attendre que quelqu'un avec accès au Shell Render** puisse vous aider

---

## 📝 Checklist de Vérification

- [ ] Code poussé sur GitHub (`git push`)
- [ ] Render a redéployé (vérifier dans le dashboard)
- [ ] `SETUP_SECRET_TOKEN` défini dans Render > Environment
- [ ] Token dans l'URL correspond au token dans Render
- [ ] Routes setup présentes dans `core/urls.py`
- [ ] Fichier `core/views_setup.py` présent
- [ ] Pas d'erreurs dans les logs Render

---

## 🔍 Vérification Rapide

Pour vérifier rapidement si les routes sont chargées :

1. Allez sur : `https://fmos-mfmc.onrender.com/admin/`
2. Si l'admin fonctionne, les routes Django sont chargées
3. Si `/setup/` ne fonctionne pas mais `/admin/` fonctionne, le problème vient des routes setup spécifiquement

---

## 📚 Documentation Supplémentaire

- **Guide initialisation interface web** : `GUIDE_INITIALISATION_INTERFACE_WEB.md`
- **Initialisation sans Shell** : `INITIALISATION_SANS_SHELL_RENDER.md`

---

**Dernière mise à jour** : Novembre 2025

