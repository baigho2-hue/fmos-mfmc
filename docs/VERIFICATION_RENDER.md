# Vérification et Correction Render

## ✅ Modifications apportées

1. **Amélioration de la commande de build** :
   - Ajout de `pip install --upgrade pip` pour s'assurer d'avoir la dernière version de pip
   - Cela évite les problèmes de compatibilité avec les nouveaux packages

## 🔍 Points à vérifier dans Render Dashboard

### 1. Variables d'environnement
Vérifiez que ces variables sont bien configurées dans Render > Web Service > Environment :

- ✅ `SECRET_KEY` : Générée automatiquement (ou définie manuellement)
- ✅ `DEBUG` : `False` (pour la production)
- ✅ `ALLOWED_HOSTS` : `fmos-mfmc.onrender.com`
- ✅ `DATABASE_URL` : Liée automatiquement à la base de données
- ✅ `DJANGO_SETTINGS_MODULE` : `core.settings`
- ✅ `PYTHON_VERSION` : `3.11.0`

### 2. Commandes de build et démarrage
Dans Render > Web Service > Settings :

**Build Command** :
```bash
pip install --upgrade pip && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

**Start Command** :
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --timeout 120 --workers 1 --threads 2 --worker-class sync --max-requests 1000 --max-requests-jitter 100
```

### 3. Base de données PostgreSQL
Vérifiez que :
- ✅ La base de données `fmos-mfmc-db` existe
- ✅ Elle est liée au service web
- ✅ La variable `DATABASE_URL` est automatiquement injectée

### 4. Logs Render
Consultez les logs dans Render > Web Service > Logs pour identifier les erreurs :

**Erreurs courantes** :
- `ModuleNotFoundError` : Package manquant dans `requirements.txt`
- `OperationalError` : Problème de connexion à la base de données
- `DisallowedHost` : `ALLOWED_HOSTS` incorrect
- `ImproperlyConfigured` : Variable d'environnement manquante

## 🚀 Actions à effectuer

1. **Pousser les modifications** :
   ```bash
   git add render.yaml
   git commit -m "Amélioration de la configuration Render"
   git push
   ```

2. **Dans Render Dashboard** :
   - Allez dans votre service web
   - Cliquez sur "Manual Deploy" > "Deploy latest commit"
   - Surveillez les logs pendant le déploiement

3. **Vérifier les logs** :
   - Si le build échoue, consultez les logs de build
   - Si le service ne démarre pas, consultez les logs runtime
   - Copiez l'erreur exacte pour diagnostic

## 🔧 Problèmes courants et solutions

### Problème : Build échoue avec "ModuleNotFoundError"
**Solution** : Vérifiez que tous les packages sont dans `requirements.txt`

### Problème : "Could not connect to database"
**Solution** : 
- Vérifiez que la base de données est créée et liée
- Vérifiez que `DATABASE_URL` est bien définie
- Consultez les logs de la base de données

### Problème : "DisallowedHost"
**Solution** : Vérifiez que `ALLOWED_HOSTS` contient bien `fmos-mfmc.onrender.com`

### Problème : Timeout lors du démarrage
**Solution** : Le timeout est déjà configuré à 120 secondes. Si le problème persiste, vérifiez les migrations qui pourraient prendre trop de temps.

## 📝 Notes importantes

- Le plan gratuit Render a des limitations (mémoire, CPU)
- Les services gratuits s'endorment après 15 minutes d'inactivité
- Le premier démarrage peut prendre plus de temps
- Les migrations sont appliquées automatiquement lors du build

