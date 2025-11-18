# 🔧 Résolution Erreur SSL PostgreSQL sur Render

## ❌ Erreur Rencontrée

```
OperationalError: connection to server at "dpg-xxxxx-a.frankfurt-postgres.render.com" (18.196.138.205), port 5432 failed: SSL connection has been closed unexpectedly
```

## ✅ Solution Appliquée

La configuration SSL a été ajoutée dans `core/settings.py` pour forcer l'utilisation de SSL avec Render PostgreSQL.

### Ce qui a été modifié

Le fichier `core/settings.py` a été mis à jour pour :
1. Détecter automatiquement les connexions Render PostgreSQL
2. Ajouter les paramètres SSL requis (`sslmode: require`)

## 🚀 Étapes pour Appliquer la Correction

### Option 1 : Redéployer sur Render (Recommandé)

1. **Commiter les changements** :
   ```bash
   git add core/settings.py
   git commit -m "Fix: Ajout configuration SSL pour Render PostgreSQL"
   git push
   ```

2. **Render redéploiera automatiquement** votre application

3. **Attendre 2-3 minutes** que le déploiement soit terminé

4. **Tester** : Visitez `https://fmos-mfmc.onrender.com/programme/desmfmc/`

### Option 2 : Redémarrer Manuellement dans Render

1. Dans Render, allez dans votre **Web Service**
2. Cliquez sur **"Manual Deploy"** > **"Deploy latest commit"**
3. Attendez que le déploiement soit terminé

## 🔍 Vérification

### Vérifier que la Configuration SSL est Active

1. Dans Render, allez dans **Logs**
2. Recherchez les messages de démarrage Django
3. Vérifiez qu'il n'y a pas d'erreurs de connexion à la base de données

### Tester la Connexion

1. Visitez votre site : `https://fmos-mfmc.onrender.com`
2. Essayez d'accéder à une page qui utilise la base de données
3. Si l'erreur persiste, voir les solutions alternatives ci-dessous

## 🆘 Solutions Alternatives si le Problème Persiste

### Solution Alternative 1 : Modifier DATABASE_URL dans Render

Si la solution automatique ne fonctionne pas, vous pouvez modifier directement `DATABASE_URL` dans Render :

1. Dans Render, allez dans **Web Service** > **Environment**
2. Trouvez `DATABASE_URL`
3. Ajoutez `?sslmode=require` à la fin de l'URL :
   ```
   postgresql://user:password@host:port/dbname?sslmode=require
   ```
4. Sauvegardez et attendez le redémarrage

### Solution Alternative 2 : Utiliser l'URL Interne

Render fournit deux URLs pour PostgreSQL :
- **Internal Database URL** : Pour les connexions depuis Render (sans SSL requis)
- **External Database URL** : Pour les connexions externes (avec SSL requis)

**Vérifiez que vous utilisez l'Internal Database URL** :

1. Dans Render, allez dans votre **PostgreSQL Database**
2. Cliquez sur **"Connections"**
3. Copiez **"Internal Database URL"** (pas External)
4. Dans votre **Web Service** > **Environment**, mettez à jour `DATABASE_URL` avec cette URL interne

### Solution Alternative 3 : Configuration SSL Plus Robuste

Si les solutions précédentes ne fonctionnent pas, modifiez `core/settings.py` avec cette configuration plus robuste :

```python
# Base de données PostgreSQL
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    db_config = dj_database_url.parse(os.environ.get('DATABASE_URL'))
    
    # Configuration SSL robuste pour Render PostgreSQL
    if 'render.com' in db_config.get('HOST', ''):
        db_config['OPTIONS'] = {
            'sslmode': 'require',
            'connect_timeout': 10,
        }
        # Réutiliser les connexions pour éviter les fermetures
        db_config['CONN_MAX_AGE'] = 600
    
    DATABASES = {
        'default': db_config
    }
```

Puis redéployez.

## 📋 Checklist de Dépannage

- [ ] Configuration SSL ajoutée dans `core/settings.py`
- [ ] Changements commités et poussés sur GitHub
- [ ] Application redéployée sur Render
- [ ] Vérifié que `DATABASE_URL` utilise l'URL interne (si disponible)
- [ ] Testé l'accès au site
- [ ] Vérifié les logs Render pour d'autres erreurs

## 🔍 Diagnostic Avancé

### Vérifier les Logs Render

1. Dans Render, allez dans **Web Service** > **Logs**
2. Recherchez les erreurs liées à PostgreSQL
3. Notez les messages d'erreur exacts

### Tester la Connexion Manuellement

Si vous avez accès au Shell Render (ou localement avec les mêmes credentials) :

```bash
python manage.py dbshell
```

Si cela fonctionne, le problème est ailleurs. Si cela échoue, vérifiez `DATABASE_URL`.

### Vérifier la Version de psycopg2

```bash
pip show psycopg2-binary
```

Assurez-vous d'avoir une version récente (>= 2.9).

## 📚 Ressources

- [Documentation Render PostgreSQL](https://render.com/docs/databases)
- [Documentation Django PostgreSQL SSL](https://docs.djangoproject.com/en/stable/ref/databases/#postgresql-notes)
- [Documentation psycopg2 SSL](https://www.psycopg.org/docs/module.html#psycopg2.connect)

---

**Si le problème persiste après avoir essayé toutes ces solutions, consultez les logs Render et partagez les messages d'erreur exacts.**

