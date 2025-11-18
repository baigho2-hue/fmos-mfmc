# 🔧 Solution Définitive pour l'Erreur SSL Render

## ⚠️ Problème Persistant

L'erreur `SSL connection has been closed unexpectedly` persiste malgré les configurations SSL.

## 🎯 Solution Principale : Vérifier l'URL DATABASE_URL

**Le problème vient probablement de l'URL utilisée dans Render.**

### Étape 1 : Vérifier l'URL dans Render

1. **Allez dans Render** > Votre **PostgreSQL Database** (pas le Web Service)
2. Cliquez sur **"Connections"** dans le menu de gauche
3. **Copiez l'Internal Database URL** (pas External)

L'URL interne ressemble à :
```
postgresql://user:password@dpg-xxxxx-a.frankfurt-postgres.render.com/fmos_mfmc
```

### Étape 2 : Mettre à Jour DATABASE_URL

1. Dans Render, allez dans votre **Web Service** `fmos-mfmc`
2. **Environment** > Trouvez `DATABASE_URL`
3. **Remplacez** par l'URL interne que vous avez copiée
4. **Sauvegardez**

### Étape 3 : Redéployer

1. Commitez et poussez les changements :
   ```bash
   git add core/settings.py
   git commit -m "Fix: Configuration SSL avec mode prefer pour Render"
   git push
   ```
2. Attendez le redéploiement (2-3 minutes)

---

## 🔄 Solution Alternative : Désactiver SSL pour les URLs Internes

Si l'URL interne ne fonctionne toujours pas, modifiez `core/settings.py` :

### Modifier core/settings.py

Remplacez la section de configuration de la base de données par :

```python
# Base de données PostgreSQL
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    
    database_url = os.environ.get('DATABASE_URL', '')
    
    if 'render.com' in database_url:
        # Pour les URLs internes Render, désactiver SSL
        # Les URLs internes commencent généralement par dpg- et n'ont pas besoin de SSL
        if 'dpg-' in database_url and 'internal' not in database_url.lower():
            # C'est probablement une URL interne, pas besoin de SSL strict
            # Retirer sslmode de l'URL si présent
            if 'sslmode' in database_url:
                import re
                database_url = re.sub(r'[?&]sslmode=[^&]*', '', database_url)
            
            db_config = dj_database_url.parse(database_url)
            # Pas d'options SSL pour les URLs internes
            db_config['OPTIONS'] = {
                'connect_timeout': 10,
            }
        else:
            # URL externe, utiliser SSL
            if 'sslmode' not in database_url:
                if '?' not in database_url:
                    database_url += '?sslmode=prefer'
                else:
                    database_url += '&sslmode=prefer'
            
            db_config = dj_database_url.parse(database_url)
            db_config['OPTIONS'] = {
                'sslmode': 'prefer',
                'connect_timeout': 10,
            }
        
        db_config['CONN_MAX_AGE'] = 600
    else:
        db_config = dj_database_url.parse(database_url)
    
    DATABASES = {
        'default': db_config
    }
```

Puis redéployez.

---

## 🆘 Solution Dernier Recours : Configuration Manuelle

Si rien ne fonctionne, configurez manuellement la base de données :

### Dans Render > Web Service > Environment

Ajoutez ces variables au lieu de `DATABASE_URL` :

- **DB_NAME** : `fmos_mfmc` (ou le nom de votre base)
- **DB_USER** : `fmos_mfmc_user` (ou votre utilisateur)
- **DB_PASSWORD** : (votre mot de passe)
- **DB_HOST** : `dpg-xxxxx-a.frankfurt-postgres.render.com` (sans le port)
- **DB_PORT** : `5432`

Puis modifiez `core/settings.py` pour utiliser ces variables :

```python
# Base de données PostgreSQL
if 'DATABASE_URL' in os.environ:
    # Utiliser DATABASE_URL si disponible
    import dj_database_url
    db_config = dj_database_url.parse(os.environ.get('DATABASE_URL'))
    DATABASES = {'default': db_config}
elif all(os.getenv(k) for k in ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']):
    # Utiliser les variables individuelles (sans SSL pour les URLs internes)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'OPTIONS': {
                'connect_timeout': 10,
            },
            'CONN_MAX_AGE': 600,
        }
    }
```

---

## 📋 Checklist de Diagnostic

- [ ] Vérifié que `DATABASE_URL` utilise l'URL interne (pas externe)
- [ ] L'URL interne commence par `postgresql://` et contient `dpg-`
- [ ] L'URL interne ne contient pas `?sslmode=require`
- [ ] Les changements dans `core/settings.py` ont été commités et poussés
- [ ] Render a redéployé l'application
- [ ] Vérifié les logs Render pour d'autres erreurs

---

## 🔍 Vérifier l'URL Actuelle

Pour voir quelle URL est utilisée, ajoutez temporairement dans `core/settings.py` :

```python
if 'DATABASE_URL' in os.environ:
    database_url = os.environ.get('DATABASE_URL', '')
    # Ne pas logger le mot de passe complet
    safe_url = database_url.split('@')[1] if '@' in database_url else 'hidden'
    print(f"DEBUG: Database URL host: {safe_url}")
```

Puis vérifiez les logs Render pour voir quelle URL est utilisée.

---

## 💡 Pourquoi ça ne fonctionne pas ?

1. **URL externe utilisée** : Les URLs externes nécessitent SSL strict qui peut échouer
2. **Configuration SSL incorrecte** : psycopg2 peut avoir des problèmes avec certaines configurations SSL
3. **Python 3.13** : Version très récente, peut avoir des problèmes de compatibilité avec psycopg2

---

**La solution la plus probable est d'utiliser l'URL interne Render qui ne nécessite pas SSL !**

