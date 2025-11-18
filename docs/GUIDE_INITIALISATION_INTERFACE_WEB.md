# 🌐 Guide : Initialisation via l'Interface Web Setup

Guide étape par étape pour initialiser votre site via l'interface web, sans accès au Shell Render.

---

## ✅ Prérequis

- ✅ Site déployé sur Render
- ✅ Application accessible (même si elle affiche des erreurs)
- ✅ Base de données PostgreSQL créée et connectée

---

## 🚀 Étapes d'Initialisation

### Étape 1 : Configurer le Token Secret

1. Allez sur [render.com](https://render.com)
2. Cliquez sur votre **Web Service** `fmos-mfmc`
3. Cliquez sur **"Environment"** (dans le menu de gauche)
4. Cliquez sur **"Add Environment Variable"**
5. Remplissez :
   - **Key** : `SETUP_SECRET_TOKEN`
   - **Value** : `VotreTokenSecretTresLongEtComplexe123!` (choisissez un token fort et unique)
6. Cliquez sur **"Save Changes"**

**⚠️ Important** : Notez ce token, vous en aurez besoin pour accéder à l'interface setup.

---

### Étape 2 : Accéder à l'Interface Setup

1. Ouvrez votre navigateur
2. Allez sur : 
   ```
   https://fmos-mfmc.onrender.com/setup/?token=VotreTokenSecretTresLongEtComplexe123!
   ```
   (Remplacez `VotreTokenSecretTresLongEtComplexe123!` par le token que vous avez créé)

3. Vous devriez voir une interface avec plusieurs boutons

---

### Étape 3 : Appliquer les Migrations

1. Cliquez sur le bouton **"Appliquer les migrations"**
2. Attendez quelques secondes
3. Vous verrez un message JSON avec le résultat
4. Si c'est un succès, vous verrez : `"success": true`

**Note** : Les migrations sont aussi appliquées automatiquement au démarrage grâce au script `startup.py`, mais cette étape permet de vérifier qu'elles sont bien appliquées.

---

### Étape 4 : Créer un Superutilisateur

1. Dans la section **"Créer un superutilisateur"**, remplissez le formulaire :
   - **Username** : `admin` (ou votre choix)
   - **Email** : `votre@email.com`
   - **Password** : `VotreMotDePasse123!` (choisissez un mot de passe fort)
2. Cliquez sur **"Créer le superutilisateur"**
3. Vous verrez un message de succès avec les détails

**⚠️ Important** : Notez ces identifiants, vous en aurez besoin pour accéder à l'admin.

---

### Étape 5 : Initialiser le Programme DESMFMC

1. Cliquez sur le bouton **"Initialiser (détaillé)"**
2. Attendez quelques secondes (cela peut prendre 30-60 secondes)
3. Vous verrez un message de succès avec les détails

**Alternative** : Si vous préférez la structure de base, cliquez sur **"Initialiser (base)"**

---

### Étape 6 : Vérifier le Statut

1. Cliquez sur le bouton **"Vérifier le statut"**
2. Vous verrez un résumé de l'état du site :
   - Nombre d'utilisateurs
   - Nombre de superutilisateurs
   - État de la base de données
   - État des migrations

---

### Étape 7 : Tester l'Accès à l'Admin

1. Ouvrez un nouvel onglet dans votre navigateur
2. Allez sur : `https://fmos-mfmc.onrender.com/admin/`
3. Connectez-vous avec votre superutilisateur
4. Vous devriez voir le tableau de bord Django

---

## 🔒 Sécurité : Supprimer l'Interface Setup

**⚠️ IMPORTANT** : Après l'initialisation, supprimez les vues setup pour des raisons de sécurité.

### Option 1 : Supprimer via Git (Recommandé)

1. Dans votre projet local, modifiez `core/urls.py` :
   - Supprimez les lignes 159-165 (les routes setup)
   - Supprimez la ligne 13 (`from core import views_setup`)
2. Supprimez le fichier `core/views_setup.py`
3. Commitez et poussez sur GitHub :
   ```bash
   git add core/urls.py core/views_setup.py
   git commit -m "Suppression des vues setup après initialisation"
   git push
   ```
4. Render redéploiera automatiquement

### Option 2 : Désactiver Temporairement

Si vous voulez garder les vues pour plus tard, vous pouvez simplement changer le token dans Render pour empêcher l'accès.

---

## 🆘 Résolution de Problèmes

### L'interface setup ne s'affiche pas

**Solutions** :
1. Vérifiez que le token dans l'URL correspond exactement à celui dans Render
2. Vérifiez que `SETUP_SECRET_TOKEN` est bien défini dans Render > Environment
3. Vérifiez que les vues setup sont présentes dans `core/urls.py`
4. Vérifiez les logs Render pour voir s'il y a des erreurs

### Erreur "Token invalide"

**Solutions** :
1. Vérifiez que le token dans l'URL correspond exactement à celui dans Render
2. Vérifiez qu'il n'y a pas d'espaces avant/après le token
3. Vérifiez que `SETUP_SECRET_TOKEN` est bien défini dans Render

### Les migrations échouent

**Solutions** :
1. Vérifiez que `DATABASE_URL` est correcte dans Render > Environment
2. Vérifiez les logs Render pour voir l'erreur exacte
3. Les migrations sont aussi appliquées automatiquement au démarrage, vérifiez les logs de démarrage

### Impossible de créer un superutilisateur

**Solutions** :
1. Vérifiez que les migrations sont appliquées
2. Vérifiez que le username/email n'existe pas déjà
3. Vérifiez les logs Render pour voir l'erreur exacte
4. Essayez avec un autre username/email

### Le programme DESMFMC ne s'initialise pas

**Solutions** :
1. Vérifiez que les migrations sont appliquées
2. Vérifiez les logs Render pour voir l'erreur exacte
3. Essayez la version "base" au lieu de "détaillé"
4. Attendez un peu plus longtemps (cela peut prendre du temps)

---

## 📝 Checklist d'Initialisation

- [ ] Token secret configuré dans Render (`SETUP_SECRET_TOKEN`)
- [ ] Interface setup accessible (`/setup/?token=...`)
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Programme DESMFMC initialisé
- [ ] Statut vérifié
- [ ] Accès à l'admin testé (`/admin/`)
- [ ] Vues setup supprimées (après initialisation)

---

## 🎉 Félicitations !

Votre site est maintenant initialisé et prêt à être utilisé !

---

## 📚 Documentation Supplémentaire

- **Initialisation sans Shell** : `INITIALISATION_SANS_SHELL_RENDER.md`
- **Guide complet Render** : `GUIDE_RENDER_COMPLET.md`
- **Configuration rapide** : `CONFIGURATION_RENDER_RAPIDE.md`

---

**Dernière mise à jour** : Novembre 2025

