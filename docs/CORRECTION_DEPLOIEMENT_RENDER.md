# Correction des Problèmes de Déploiement Render

## ✅ Modifications Apportées

### 1. Amélioration de `render.yaml`
- Ajout de `setuptools` et `wheel` dans la mise à jour de pip
- Amélioration de la commande de build pour une meilleure gestion des dépendances

### 2. Amélioration de `core/settings.py`
- Création automatique du dossier `static` s'il n'existe pas
- Cela évite les erreurs lors de `collectstatic` si le dossier n'existe pas encore

## 🔍 Diagnostic des Erreurs de Déploiement

### Erreurs Courantes et Solutions

#### 1. "ModuleNotFoundError: No module named 'xxx'"
**Cause** : Package manquant dans `requirements.txt`

**Solution** :
```bash
# Vérifiez que tous les packages sont listés
pip freeze > requirements_check.txt
# Comparez avec requirements.txt
```

#### 2. "Error: collectstatic failed"
**Cause** : Problème avec les fichiers statiques

**Solution** : 
- Le dossier `static` est maintenant créé automatiquement
- Vérifiez que `STATICFILES_DIRS` pointe vers un dossier existant

#### 3. "OperationalError: could not connect to database"
**Cause** : Problème de connexion à PostgreSQL

**Solution** :
- Vérifiez que `DATABASE_URL` est bien définie dans Render
- Vérifiez que la base de données est créée et liée au service
- Vérifiez les logs de la base de données dans Render

#### 4. "DisallowedHost at /"
**Cause** : `ALLOWED_HOSTS` incorrect

**Solution** :
- Vérifiez que `ALLOWED_HOSTS` contient `fmos-mfmc.onrender.com`
- Vérifiez dans Render > Environment que la variable est bien définie

#### 5. "Migration failed"
**Cause** : Erreur lors de l'application des migrations

**Solution** :
- Vérifiez les logs de build dans Render
- Les migrations sont appliquées avec `--noinput` pour éviter les prompts
- Si une migration échoue, vérifiez la structure de la base de données

## 🚀 Étapes pour Corriger le Déploiement

### 1. Vérifier les Logs Render
1. Allez dans Render Dashboard > Web Service > **Logs**
2. Identifiez l'erreur exacte dans les logs de build ou runtime
3. Copiez le message d'erreur complet

### 2. Vérifier les Variables d'Environnement
Dans Render > Web Service > **Environment**, vérifiez :
- ✅ `SECRET_KEY` : Générée automatiquement
- ✅ `DEBUG` : `False`
- ✅ `ALLOWED_HOSTS` : `fmos-mfmc.onrender.com`
- ✅ `DATABASE_URL` : Liée automatiquement à la base
- ✅ `DJANGO_SETTINGS_MODULE` : `core.settings`
- ✅ `PYTHON_VERSION` : `3.11.0`

### 3. Vérifier la Base de Données
1. Allez dans Render > PostgreSQL
2. Vérifiez que la base `fmos-mfmc-db` existe
3. Vérifiez qu'elle est liée au service web
4. Consultez les logs de la base de données

### 4. Tester Localement
Avant de redéployer, testez localement :
```bash
# Installer les dépendances
pip install -r requirements.txt

# Tester collectstatic
python manage.py collectstatic --noinput

# Tester les migrations
python manage.py migrate --noinput

# Tester le démarrage
gunicorn core.wsgi:application
```

### 5. Redéployer
1. Commitez et poussez les modifications :
   ```bash
   git add render.yaml core/settings.py
   git commit -m "Correction configuration déploiement Render"
   git push
   ```

2. Dans Render Dashboard :
   - Allez dans votre service web
   - Cliquez sur **"Manual Deploy"** > **"Deploy latest commit"**
   - Surveillez les logs en temps réel

## 📋 Checklist de Vérification

- [ ] Tous les packages sont dans `requirements.txt`
- [ ] Le dossier `static` existe (créé automatiquement maintenant)
- [ ] Les variables d'environnement sont configurées dans Render
- [ ] La base de données est créée et liée
- [ ] Les migrations sont à jour localement
- [ ] `collectstatic` fonctionne localement
- [ ] Le service démarre localement avec gunicorn

## 🔧 Commandes Utiles pour le Diagnostic

### Vérifier les dépendances
```bash
pip list
pip check
```

### Vérifier les migrations
```bash
python manage.py showmigrations
python manage.py migrate --plan
```

### Tester collectstatic
```bash
python manage.py collectstatic --noinput --dry-run
```

### Tester la connexion à la base
```python
python manage.py shell
>>> from django.db import connection
>>> connection.ensure_connection()
```

## 📞 Si le Problème Persiste

1. **Copiez l'erreur exacte** des logs Render
2. **Vérifiez les points de la checklist**
3. **Testez localement** avec les mêmes commandes que Render
4. **Consultez la documentation Render** : https://render.com/docs

Les modifications apportées devraient résoudre la plupart des problèmes courants de déploiement.

