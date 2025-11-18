# 🔧 Corriger DATABASE_URL pour Render PostgreSQL

## ⚠️ Problème

L'erreur SSL persiste car Render fournit **deux types d'URLs** pour PostgreSQL :
- **Internal Database URL** : Pour les connexions depuis Render (recommandé, plus stable)
- **External Database URL** : Pour les connexions externes (nécessite SSL strict)

## ✅ Solution : Utiliser l'URL Interne

### Étape 1 : Trouver l'URL Interne dans Render

1. Allez sur [render.com](https://render.com)
2. Cliquez sur votre **PostgreSQL Database** (pas le Web Service)
3. Dans le menu de gauche, cliquez sur **"Connections"**
4. Vous verrez deux URLs :
   - **Internal Database URL** ← **UTILISEZ CELUI-CI**
   - External Database URL (ignorez celle-ci)

### Étape 2 : Copier l'URL Interne

L'URL interne ressemble à :
```
postgresql://fmos_mfmc_user:motdepasse@dpg-xxxxx-a.frankfurt-postgres.render.com/fmos_mfmc
```

**Copiez cette URL complète.**

### Étape 3 : Mettre à Jour DATABASE_URL dans Render

1. Dans Render, cliquez sur votre **Web Service** `fmos-mfmc`
2. Allez dans **"Environment"** (menu de gauche)
3. Trouvez la variable **`DATABASE_URL`**
4. Cliquez sur l'icône de modification (crayon)
5. **Remplacez** la valeur par l'URL interne que vous avez copiée
6. Cliquez sur **"Save Changes"**

### Étape 4 : Attendre le Redémarrage

- Render redémarre automatiquement votre application
- Attendez 2-3 minutes
- Vérifiez dans **"Logs"** que l'application a bien redémarré

### Étape 5 : Tester

Visitez : `https://fmos-mfmc.onrender.com/programme/desmfmc/`

L'erreur SSL devrait être résolue !

---

## 🔍 Comment Vérifier quelle URL est Utilisée

### Dans Render Logs

1. Allez dans **Web Service** > **Logs**
2. Recherchez les messages de démarrage Django
3. Si vous voyez des erreurs SSL, c'est probablement l'URL externe qui est utilisée

### Vérifier dans l'Interface Render

1. **Web Service** > **Environment**
2. Regardez la valeur de `DATABASE_URL`
3. Si elle contient `?sslmode=require` ou des paramètres SSL → C'est l'URL externe
4. L'URL interne est généralement plus simple, sans paramètres SSL

---

## 🆘 Si le Problème Persiste

### Solution Alternative 1 : Ajouter sslmode à l'URL Manuellement

Si vous devez absolument utiliser l'URL externe, ajoutez `?sslmode=require` à la fin :

1. Dans **Web Service** > **Environment** > `DATABASE_URL`
2. Ajoutez `?sslmode=require` à la fin de l'URL :
   ```
   postgresql://user:pass@host:port/db?sslmode=require
   ```
3. Sauvegardez

### Solution Alternative 2 : Vérifier la Configuration SSL dans le Code

Le code dans `core/settings.py` devrait maintenant :
- Détecter automatiquement les URLs Render
- Ajouter `sslmode=require` si nécessaire
- Configurer les options SSL pour psycopg2

Assurez-vous que les changements ont été déployés :
1. Vérifiez que `core/settings.py` contient la nouvelle configuration SSL
2. Commitez et poussez les changements :
   ```bash
   git add core/settings.py
   git commit -m "Fix: Configuration SSL robuste pour Render"
   git push
   ```
3. Attendez que Render redéploie

---

## 📋 Checklist

- [ ] Identifié la base PostgreSQL dans Render
- [ ] Trouvé l'URL interne dans "Connections"
- [ ] Copié l'URL interne complète
- [ ] Mis à jour `DATABASE_URL` dans Web Service > Environment
- [ ] Sauvegardé les changements
- [ ] Attendu le redémarrage (2-3 minutes)
- [ ] Testé l'accès au site
- [ ] Vérifié les logs pour confirmer qu'il n'y a plus d'erreurs SSL

---

## 💡 Pourquoi l'URL Interne ?

- ✅ **Plus stable** : Connexions directes dans le réseau Render
- ✅ **Pas de problèmes SSL** : Pas besoin de configuration SSL complexe
- ✅ **Plus rapide** : Latence réduite
- ✅ **Recommandé par Render** : C'est la méthode officielle

---

**Après avoir mis à jour DATABASE_URL avec l'URL interne, l'erreur SSL devrait disparaître ! 🎉**

