# 🔧 Résolution : Erreur "Out of Memory" sur Render

Si vous voyez l'erreur `Worker was sent SIGKILL! Perhaps out of memory?`, c'est que votre application dépasse la limite de mémoire du plan gratuit Render (512 MB).

---

## 🔍 Causes

1. **Script startup.py** qui s'exécute au démarrage et charge trop de données
2. **Trop de workers Gunicorn** qui consomment chacun de la mémoire
3. **Chargement de trop de données** en mémoire au démarrage

---

## ✅ Solutions Appliquées

### Solution 1 : Désactiver le Script Startup au Démarrage

Le script `startup.py` a été désactivé dans `wsgi.py` pour économiser la mémoire. Les migrations sont maintenant appliquées uniquement dans le `buildCommand` de `render.yaml`.

### Solution 2 : Optimiser Gunicorn

La configuration Gunicorn a été optimisée pour utiliser moins de mémoire :
- **1 worker** au lieu de plusieurs
- **2 threads** par worker
- **Limite de requêtes** pour redémarrer les workers périodiquement

---

## 🔧 Configuration Optimisée

### Procfile

```
web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 2 --worker-class sync --max-requests 1000 --max-requests-jitter 100
```

### render.yaml

Le `startCommand` a été optimisé avec les mêmes paramètres.

---

## 📝 Alternatives pour l'Initialisation

Puisque le script startup est désactivé, utilisez :

### Option 1 : Interface Web Setup (Recommandé)

1. Accédez à : `https://fmos-mfmc.onrender.com/setup/?token=VOTRE_TOKEN`
2. Utilisez les boutons pour initialiser le site

### Option 2 : Migrations Automatiques

Les migrations sont appliquées automatiquement dans le `buildCommand` :
```yaml
buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

---

## 🚀 Redéployer

Après ces modifications :

1. Commitez et poussez les changements :
   ```bash
   git add core/wsgi.py render.yaml Procfile
   git commit -m "Optimisation mémoire pour plan gratuit Render"
   git push origin main
   ```

2. Render redéploiera automatiquement

3. Vérifiez que l'application démarre sans erreur OOM

---

## 💡 Optimisations Supplémentaires

### Si le Problème Persiste

1. **Réduire encore plus les workers** :
   ```
   --workers 1 --threads 1
   ```

2. **Désactiver les fonctionnalités non essentielles** :
   - Désactiver les middlewares non utilisés
   - Réduire le nombre d'apps Django installées

3. **Optimiser les requêtes de base de données** :
   - Utiliser `.only()` et `.defer()` pour limiter les champs chargés
   - Utiliser la pagination partout

4. **Vérifier les logs Render** :
   - Surveillez l'utilisation mémoire dans les logs
   - Identifiez les requêtes qui consomment le plus

---

## 📊 Monitoring

Dans Render > Web Service > **Metrics**, vous pouvez voir :
- L'utilisation CPU
- L'utilisation mémoire
- Les requêtes par seconde

Surveillez ces métriques pour identifier les pics de consommation.

---

## 🆘 Si Rien ne Fonctionne

Si l'application continue de crasher à cause de la mémoire :

1. **Upgrade vers un plan payant** Render (plus de mémoire)
2. **Utilisez Railway** qui offre plus de mémoire sur le plan gratuit
3. **Optimisez votre code** pour réduire l'utilisation mémoire

---

## 📚 Documentation Supplémentaire

- **Guide Render** : `GUIDE_RENDER_COMPLET.md`
- **Initialisation** : `GUIDE_INITIALISATION_INTERFACE_WEB.md`

---

**Dernière mise à jour** : Novembre 2025

