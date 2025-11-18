# 🚀 Guide Étape par Étape - Configuration Render

Suivez ces étapes dans l'ordre pour configurer votre site déployé sur Render.

---

## 📋 ÉTAPE 1 : Définir le Token Secret dans Render

### 1.1 Ouvrir Render

1. Allez sur [https://render.com](https://render.com)
2. Connectez-vous à votre compte
3. Cliquez sur votre **Web Service** `fmos-mfmc`

### 1.2 Ajouter la Variable d'Environnement

1. Dans le menu de gauche, cliquez sur **"Environment"**
2. Cliquez sur **"Add Environment Variable"**
3. Remplissez :
   - **Key** : `SETUP_SECRET_TOKEN`
   - **Value** : `FMOS2024ConfigSecret!` (ou choisissez votre propre mot de passe fort)
4. Cliquez sur **"Save Changes"**

⚠️ **Important** : Notez bien cette valeur, vous en aurez besoin pour accéder à l'interface !

### 1.3 Attendre le Redémarrage

- Render redémarre automatiquement votre application
- Attendez 1-2 minutes que le déploiement soit terminé
- Vous pouvez vérifier dans l'onglet **"Logs"** que l'application a bien redémarré

---

## 🌐 ÉTAPE 2 : Accéder à l'Interface de Configuration

### 2.1 Ouvrir l'Interface

Une fois le redémarrage terminé, ouvrez votre navigateur et allez sur :

```
https://fmos-mfmc.onrender.com/setup/?token=FMOS2024ConfigSecret!
```

**Remplacez** `FMOS2024ConfigSecret!` par la valeur que vous avez définie dans l'étape 1.

### 2.2 Vérifier l'Accès

- Si vous voyez une page avec des boutons de configuration → ✅ C'est bon !
- Si vous voyez "Accès refusé" → Vérifiez que le token correspond exactement

---

## ⚙️ ÉTAPE 3 : Appliquer les Migrations

### 3.1 Dans l'Interface Web

1. Cliquez sur le bouton **"Appliquer les migrations"**
2. Attendez quelques secondes
3. Vous devriez voir un message de succès (format JSON)

### 3.2 Vérifier

- Si vous voyez `"success": true` → ✅ Les migrations sont appliquées !
- Si vous voyez une erreur → Consultez les logs dans Render

---

## 👤 ÉTAPE 4 : Créer un Superutilisateur

### 4.1 Remplir le Formulaire

Dans l'interface web, remplissez le formulaire "Créer un superutilisateur" :

- **Username** : `admin` (ou votre choix)
- **Email** : `admin@fmos-mfmc.ml` (ou votre email)
- **Password** : Choisissez un mot de passe fort (ex: `AdminFMOS2024!`)

⚠️ **Important** : Notez bien ces identifiants, vous en aurez besoin pour vous connecter à l'admin !

### 4.2 Soumettre

1. Cliquez sur **"Créer le superutilisateur"**
2. Attendez quelques secondes
3. Vous devriez voir un message de succès

### 4.3 Vérifier

- Si vous voyez `"success": true` → ✅ Le superutilisateur est créé !
- Si vous voyez une erreur "utilisateur existe déjà" → C'est normal, il existe déjà

---

## 📚 ÉTAPE 5 : Initialiser le Programme DESMFMC

### 5.1 Dans l'Interface Web

1. Cliquez sur le bouton **"Initialiser (détaillé)"**
2. Attendez 10-30 secondes (cela peut prendre du temps)
3. Vous devriez voir un message de succès

### 5.2 Alternative

Si vous préférez la structure de base :
- Cliquez sur **"Initialiser (base)"**

---

## ✅ ÉTAPE 6 : Vérifier le Statut

### 6.1 Vérifier la Configuration

1. Cliquez sur **"Vérifier le statut"**
2. Vous devriez voir :
   - Nombre d'utilisateurs
   - Nombre de superutilisateurs
   - État des migrations

### 6.2 Tester l'Accès à l'Admin

1. Ouvrez un nouvel onglet dans votre navigateur
2. Allez sur : `https://fmos-mfmc.onrender.com/admin/`
3. Connectez-vous avec :
   - **Username** : Celui que vous avez créé à l'étape 4
   - **Password** : Le mot de passe que vous avez défini

### 6.3 Si ça fonctionne

✅ **Félicitations ! Votre site est configuré !**

---

## 🔒 ÉTAPE 7 : Sécuriser (IMPORTANT)

Après avoir configuré votre site, **supprimez les vues de configuration** pour des raisons de sécurité.

### 7.1 Supprimer les Fichiers Localement

1. Supprimez le fichier `core/views_setup.py`
2. Ouvrez `core/urls.py`
3. Supprimez ces lignes (environ lignes 159-164) :
   ```python
   # ⚠️ VUES TEMPORAIRES POUR CONFIGURATION RENDER - À SUPPRIMER APRÈS CONFIGURATION
   path('setup/', views_setup.setup_dashboard, name='setup_dashboard'),
   path('setup/migrate/', views_setup.setup_migrate, name='setup_migrate'),
   path('setup/create-superuser/', views_setup.setup_create_superuser, name='setup_create_superuser'),
   path('setup/init-programme/', views_setup.setup_init_programme, name='setup_init_programme'),
   path('setup/status/', views_setup.setup_status, name='setup_status'),
   ```
4. Supprimez aussi cette ligne (environ ligne 13) :
   ```python
   from core import views_setup  # Vues temporaires pour la configuration Render
   ```

### 7.2 Commiter et Pousser

```bash
git add .
git commit -m "Suppression des vues de configuration temporaires"
git push
```

### 7.3 Supprimer la Variable dans Render

1. Dans Render, allez dans **Web Service** > **Environment**
2. Trouvez `SETUP_SECRET_TOKEN`
3. Cliquez sur l'icône de suppression (poubelle)
4. Cliquez sur **"Save Changes"**

---

## 🆘 En Cas de Problème

### L'interface ne s'affiche pas

1. Vérifiez que `SETUP_SECRET_TOKEN` est bien défini dans Render
2. Vérifiez que l'application a bien redémarré (onglet Logs)
3. Vérifiez que le token dans l'URL correspond exactement

### Erreur "Token invalide"

- Le token est sensible à la casse
- Vérifiez qu'il n'y a pas d'espaces avant/après
- Copiez-collez directement depuis Render

### Les migrations échouent

1. Vérifiez les logs dans Render
2. Vérifiez que `DATABASE_URL` est correcte dans Environment
3. Vérifiez que la base PostgreSQL est active

### Le superutilisateur n'est pas créé

1. Vérifiez que l'utilisateur n'existe pas déjà
2. Essayez avec un autre username/email
3. Consultez les logs dans Render

---

## 📝 Résumé des URLs Importantes

- **Interface de configuration** : `https://fmos-mfmc.onrender.com/setup/?token=VOTRE_TOKEN`
- **Admin Django** : `https://fmos-mfmc.onrender.com/admin/`
- **Site principal** : `https://fmos-mfmc.onrender.com`

---

## ✅ Checklist Finale

- [ ] Token `SETUP_SECRET_TOKEN` défini dans Render
- [ ] Application redémarrée
- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Programme DESMFMC initialisé
- [ ] Accès à l'admin vérifié
- [ ] Vues de configuration supprimées
- [ ] Variable `SETUP_SECRET_TOKEN` supprimée dans Render

---

**Votre site est maintenant complètement configuré et sécurisé ! 🎉**

