# ✅ Étapes d'Initialisation via l'Interface Setup

Vous êtes sur la page setup ! Suivez ces étapes dans l'ordre.

---

## 📋 Étapes à Suivre

### Étape 1 : Appliquer les Migrations ✅

1. Cliquez sur le bouton **"Appliquer les migrations"**
2. Attendez quelques secondes
3. Vous devriez voir un message JSON avec `"success": true`
4. Si c'est le cas, passez à l'étape suivante

**Note** : Les migrations sont aussi appliquées automatiquement au démarrage, mais cette étape permet de vérifier qu'elles sont bien appliquées.

---

### Étape 2 : Créer un Superutilisateur 👤

1. Dans la section **"Créer un superutilisateur"**, remplissez le formulaire :
   - **Username** : `admin` (ou votre choix)
   - **Email** : `votre@email.com` (votre email réel)
   - **Password** : `VotreMotDePasse123!` (choisissez un mot de passe fort)
2. Cliquez sur **"Créer le superutilisateur"**
3. Vous devriez voir un message de succès avec les détails

**⚠️ Important** : Notez ces identifiants ! Vous en aurez besoin pour accéder à l'admin.

---

### Étape 3 : Initialiser le Programme DESMFMC 📚

1. Cliquez sur le bouton **"Initialiser (détaillé)"**
2. **Attendez 30-60 secondes** (cela peut prendre du temps)
3. Vous devriez voir un message de succès avec les détails

**Alternative** : Si vous préférez la structure de base (plus rapide), cliquez sur **"Initialiser (base)"**

---

### Étape 4 : Vérifier le Statut ✅

1. Cliquez sur le bouton **"Vérifier le statut"**
2. Vous verrez un résumé de l'état du site :
   - Nombre d'utilisateurs
   - Nombre de superutilisateurs
   - État de la base de données
   - État des migrations

---

### Étape 5 : Tester l'Accès à l'Admin 🎯

1. Ouvrez un **nouvel onglet** dans votre navigateur
2. Allez sur : `https://fmos-mfmc.onrender.com/admin/`
3. Connectez-vous avec votre superutilisateur (créé à l'étape 2)
4. Vous devriez voir le tableau de bord Django

---

## ✅ Checklist

- [ ] Migrations appliquées
- [ ] Superutilisateur créé
- [ ] Programme DESMFMC initialisé
- [ ] Statut vérifié
- [ ] Accès à l'admin testé

---

## 🎉 Félicitations !

Une fois toutes ces étapes terminées, votre site est initialisé et prêt à être utilisé !

---

## 🔒 Important : Sécurité

**Après l'initialisation**, supprimez les vues setup pour des raisons de sécurité :

1. Supprimez les lignes 159-165 dans `core/urls.py`
2. Supprimez la ligne 13 dans `core/urls.py` (`from core import views_setup`)
3. Supprimez le fichier `core/views_setup.py`
4. Commitez et poussez sur GitHub :
   ```bash
   git add core/urls.py core/views_setup.py
   git commit -m "Suppression des vues setup après initialisation"
   git push origin main
   ```

---

## 🆘 En Cas de Problème

### Les migrations échouent

- Vérifiez les logs Render pour voir l'erreur exacte
- Les migrations sont aussi appliquées automatiquement au démarrage

### Impossible de créer un superutilisateur

- Vérifiez que le username/email n'existe pas déjà
- Vérifiez les logs Render pour voir l'erreur exacte
- Essayez avec un autre username/email

### Le programme DESMFMC ne s'initialise pas

- Attendez un peu plus longtemps (cela peut prendre 30-60 secondes)
- Vérifiez les logs Render pour voir l'erreur exacte
- Essayez la version "base" au lieu de "détaillé"

---

**Bonne chance avec l'initialisation ! 🚀**

