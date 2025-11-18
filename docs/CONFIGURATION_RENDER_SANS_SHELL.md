# 🔧 Configuration Render Sans Accès au Shell

Si vous n'avez pas accès au Shell Render, voici **3 solutions** pour configurer votre site déployé.

---

## ✅ Solution 1 : Interface Web de Configuration (RECOMMANDÉ)

Une interface web a été créée pour configurer votre site directement depuis votre navigateur !

### 📋 Étape 1 : Définir un Token Secret

1. Dans Render, allez dans votre **Web Service** > **Environment**
2. Ajoutez une nouvelle variable d'environnement :
   - **Key** : `SETUP_SECRET_TOKEN`
   - **Value** : Choisissez un mot de passe fort (ex: `MonTokenSecret123!`)
3. Cliquez sur **"Save Changes"**
4. Render redémarre automatiquement votre application

### 🌐 Étape 2 : Accéder à l'Interface de Configuration

Une fois le redémarrage terminé, ouvrez votre navigateur et allez sur :

```
https://fmos-mfmc.onrender.com/setup/?token=VOTRE_TOKEN
```

Remplacez `VOTRE_TOKEN` par la valeur que vous avez définie dans `SETUP_SECRET_TOKEN`.

### ⚙️ Étape 3 : Configurer le Site

Dans l'interface web, vous pouvez :

1. **Appliquer les migrations** : Cliquez sur "Appliquer les migrations"
2. **Créer un superutilisateur** : Remplissez le formulaire avec :
   - Username : `admin` (ou votre choix)
   - Email : `votre@email.com`
   - Password : Un mot de passe fort
3. **Initialiser le programme DESMFMC** : Cliquez sur "Initialiser (détaillé)"
4. **Vérifier le statut** : Cliquez sur "Vérifier le statut" pour voir l'état

### 🔒 Sécurité

⚠️ **IMPORTANT** : Après avoir configuré votre site, **supprimez ces vues** pour des raisons de sécurité :

1. Supprimez le fichier `core/views_setup.py`
2. Supprimez les routes dans `core/urls.py` (lignes 159-164)
3. Supprimez la variable `SETUP_SECRET_TOKEN` dans Render
4. Commitez et poussez les changements

---

## ✅ Solution 2 : Utiliser le Script release.sh

Le script `release.sh` s'exécute automatiquement lors de chaque déploiement sur Render.

### 📋 Configuration dans Render

1. Dans Render, allez dans votre **Web Service** > **Settings**
2. Cherchez **"Post Deploy Command"** ou **"Deploy Hook"**
3. Ajoutez cette commande :
   ```bash
   python manage.py migrate --noinput && python manage.py collectstatic --noinput
   ```

Les migrations seront appliquées automatiquement à chaque déploiement.

### 👤 Créer un Superutilisateur

Pour créer un superutilisateur sans Shell, utilisez la **Solution 1** (interface web) ou ajoutez une variable d'environnement :

1. Dans Render > **Environment**, ajoutez :
   - **Key** : `CREATE_SUPERUSER`
   - **Value** : `true`
   - **Key** : `SUPERUSER_USERNAME`
   - **Value** : `admin`
   - **Key** : `SUPERUSER_EMAIL`
   - **Value** : `admin@example.com`
   - **Key** : `SUPERUSER_PASSWORD`
   - **Value** : `VotreMotDePasse123!`

2. Modifiez `release.sh` pour créer automatiquement le superutilisateur (voir ci-dessous)

### 🔧 Modifier release.sh (Optionnel)

Vous pouvez modifier `release.sh` pour créer automatiquement un superutilisateur :

```bash
#!/bin/bash
# Script exécuté par Render avant le démarrage de l'application

echo "🚀 Démarrage du script de release..."
echo "📦 Application des migrations..."
python manage.py migrate --noinput

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Créer un superutilisateur si les variables sont définies
if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "👤 Création du superutilisateur..."
    python manage.py creer_superuser \
        --username "$SUPERUSER_USERNAME" \
        --email "$SUPERUSER_EMAIL" \
        --password "$SUPERUSER_PASSWORD" || echo "Superutilisateur déjà existant ou erreur"
fi

echo "✅ Script de release terminé !"
```

⚠️ **Attention** : Cette méthode stocke le mot de passe en clair dans les variables d'environnement. Supprimez ces variables après la création.

---

## ✅ Solution 3 : Utiliser les URLs Directes

Vous pouvez aussi appeler directement les endpoints avec un token :

### Appliquer les migrations
```
https://fmos-mfmc.onrender.com/setup/migrate/?token=VOTRE_TOKEN
```

### Créer un superutilisateur
```
https://fmos-mfmc.onrender.com/setup/create-superuser/?token=VOTRE_TOKEN&username=admin&email=admin@example.com&password=MotDePasse123!
```

### Initialiser le programme
```
https://fmos-mfmc.onrender.com/setup/init-programme/?token=VOTRE_TOKEN&type=detaille
```

### Vérifier le statut
```
https://fmos-mfmc.onrender.com/setup/status/?token=VOTRE_TOKEN
```

---

## 📝 Checklist de Configuration

- [ ] Variable `SETUP_SECRET_TOKEN` définie dans Render
- [ ] Application redémarrée
- [ ] Migrations appliquées (via interface web ou release.sh)
- [ ] Superutilisateur créé
- [ ] Programme DESMFMC initialisé
- [ ] Accès à l'admin vérifié (`/admin/`)
- [ ] Vues de configuration supprimées (après configuration)

---

## 🆘 Résolution de Problèmes

### L'interface web ne s'affiche pas

1. Vérifiez que `SETUP_SECRET_TOKEN` est défini dans Render
2. Vérifiez que l'application a redémarré
3. Vérifiez que le token dans l'URL correspond exactement

### Erreur "Token invalide"

- Vérifiez que le token dans l'URL correspond exactement à `SETUP_SECRET_TOKEN`
- Le token est sensible à la casse

### Les migrations ne s'appliquent pas

1. Vérifiez les logs dans Render
2. Vérifiez que `DATABASE_URL` est correcte
3. Essayez d'appliquer les migrations via l'interface web

### Le superutilisateur n'est pas créé

1. Vérifiez que l'utilisateur n'existe pas déjà
2. Vérifiez les logs dans Render
3. Essayez avec un autre username/email

---

## 🎯 Prochaines Étapes

Une fois la configuration terminée :

1. **Accédez à l'admin** : `https://fmos-mfmc.onrender.com/admin/`
2. **Connectez-vous** avec votre superutilisateur
3. **Supprimez les vues de configuration** pour la sécurité
4. **Testez votre site** : `https://fmos-mfmc.onrender.com`

---

**Votre site est maintenant configuré ! 🎉**

