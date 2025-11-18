# 🔧 Résolution : ModuleNotFoundError: No module named 'settings' sur Render

## 🔍 Problème

L'erreur suivante apparaît lors du déploiement sur Render :

```
ModuleNotFoundError: No module named 'settings'
```

Cette erreur se produit généralement lorsque Django ne peut pas trouver le module de configuration.

---

## ✅ Solutions

### Solution 1 : Ajouter DJANGO_SETTINGS_MODULE dans les Variables d'Environnement

Dans Render > Web Service > **Environment**, ajoutez :

- **Key** : `DJANGO_SETTINGS_MODULE`
- **Value** : `core.settings`

### Solution 2 : Vérifier le fichier runtime.txt

Assurez-vous que `runtime.txt` contient :

```
python-3.11.0
```

**Note** : Render peut utiliser Python 3.13 par défaut si la version n'est pas spécifiée correctement.

### Solution 3 : Vérifier le Procfile

Le `Procfile` doit contenir :

```
web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

### Solution 4 : Vérifier la structure du projet

Assurez-vous que :
- Le fichier `core/settings.py` existe
- Le fichier `core/__init__.py` existe
- Le fichier `core/wsgi.py` existe et contient :
  ```python
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
  ```

### Solution 5 : Vérifier le Build Command

Dans Render > Web Service > **Settings** > **Build Command**, assurez-vous que c'est :

```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

---

## 🔄 Étapes de Correction

1. **Dans Render Dashboard** :
   - Allez dans votre Web Service
   - Cliquez sur **"Environment"**
   - Ajoutez la variable `DJANGO_SETTINGS_MODULE` avec la valeur `core.settings`
   - Cliquez sur **"Save Changes"**

2. **Vérifiez le fichier runtime.txt** :
   - Assurez-vous qu'il contient `python-3.11.0`
   - Si vous utilisez `render.yaml`, vérifiez que `PYTHON_VERSION` est défini à `3.11.0`

3. **Redéployez** :
   - Dans Render, cliquez sur **"Manual Deploy"** > **"Deploy latest commit"**
   - Surveillez les logs pour vérifier que l'erreur est résolue

---

## 📝 Vérification

Après avoir appliqué les corrections, vérifiez dans les logs Render que :

1. ✅ Python 3.11.0 est utilisé (pas 3.13)
2. ✅ Le module `core.settings` est trouvé
3. ✅ L'application démarre correctement

---

## 🆘 Si le problème persiste

1. **Vérifiez les logs complets** dans Render pour voir l'erreur exacte
2. **Vérifiez que tous les fichiers sont présents** :
   - `core/settings.py`
   - `core/wsgi.py`
   - `core/__init__.py`
   - `manage.py`
3. **Vérifiez le Build Command** pour s'assurer qu'il n'y a pas d'erreurs lors de l'installation des dépendances

---

## 📚 Documentation Supplémentaire

- Guide complet : `GUIDE_RENDER_COMPLET.md`
- Configuration rapide : `CONFIGURATION_RENDER_RAPIDE.md`

