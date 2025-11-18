# 🔧 Résolution : Internal Server Error (500) sur /setup/

Si vous obtenez une erreur 500 sur la page setup, voici comment résoudre le problème.

---

## 🔍 Diagnostic

### Étape 1 : Vérifier les Logs Render

**C'est la première chose à faire !**

1. Allez sur [render.com](https://render.com)
2. Cliquez sur votre **Web Service** `fmos-mfmc`
3. Cliquez sur **"Logs"** (dans le menu de gauche)
4. **Lisez les dernières erreurs** - elles vous diront exactement quel est le problème

---

## 🆘 Causes Courantes et Solutions

### Cause 1 : Erreur d'Import ou Module Manquant

**Symptôme** : Erreur `ModuleNotFoundError` ou `ImportError` dans les logs

**Solution** :
1. Vérifiez que toutes les dépendances sont dans `requirements.txt`
2. Vérifiez les logs de build Render pour voir s'il y a des erreurs d'installation
3. Redéployez l'application

### Cause 2 : Erreur de Connexion à la Base de Données

**Symptôme** : Erreur `django.db.utils.OperationalError` ou `could not connect`

**Solution** :
1. Vérifiez que `DATABASE_URL` est correcte dans Render > Environment
2. Vérifiez que la base PostgreSQL est active dans Render
3. Vérifiez que la base et le service web sont dans la même région

### Cause 3 : Erreur dans le Code Python

**Symptôme** : Erreur `SyntaxError`, `AttributeError`, `TypeError`, etc.

**Solution** :
1. Vérifiez les logs Render pour voir l'erreur exacte
2. Vérifiez que le code est correct dans `core/views_setup.py`
3. Vérifiez que toutes les dépendances sont installées

### Cause 4 : Erreur lors de l'Exécution d'une Commande

**Symptôme** : Erreur lors de l'appel à `call_command` ou lors de l'exécution d'une commande Django

**Solution** :
1. Vérifiez que les migrations sont appliquées
2. Vérifiez que les modèles Django sont corrects
3. Vérifiez les logs pour voir quelle commande échoue

---

## ✅ Solution Rapide : Activer DEBUG Temporairement

Pour voir l'erreur exacte dans le navigateur :

1. Dans Render > Web Service > **Environment**
2. Changez `DEBUG` à `True`
3. Cliquez sur **"Save Changes"**
4. Render redémarre automatiquement
5. Réessayez d'accéder à `/setup/`
6. Vous verrez l'erreur détaillée dans le navigateur

**⚠️ Important** : Remettez `DEBUG=False` après avoir résolu le problème !

---

## 🔧 Solutions Spécifiques

### Si l'Erreur se Produit au Chargement de la Page

**Vérifiez** :
1. Que `core/views_setup.py` existe et est correct
2. Que l'import dans `core/urls.py` est correct : `from core import views_setup`
3. Que les routes sont bien dans `urlpatterns`

### Si l'Erreur se Produit lors de l'Exécution d'une Commande

**Vérifiez** :
1. Que les migrations sont appliquées (`python manage.py migrate`)
2. Que la base de données est accessible
3. Que les modèles Django sont corrects

### Si l'Erreur se Produit lors de la Création du Superutilisateur

**Vérifiez** :
1. Que le modèle `Utilisateur` est correct
2. Que les champs requis sont fournis
3. Que le username/email n'existe pas déjà

---

## 📝 Checklist de Vérification

- [ ] Logs Render consultés - Erreur identifiée
- [ ] `DATABASE_URL` correcte dans Render > Environment
- [ ] Base PostgreSQL active dans Render
- [ ] `DEBUG=True` activé temporairement pour voir l'erreur
- [ ] Code `core/views_setup.py` vérifié
- [ ] Dépendances dans `requirements.txt` vérifiées
- [ ] Migrations appliquées

---

## 🚀 Redéployer

Après avoir corrigé le problème :

1. Si vous avez modifié le code, commitez et poussez :
   ```bash
   git add .
   git commit -m "Correction erreur setup"
   git push origin main
   ```

2. Dans Render, cliquez sur **"Manual Deploy"** > **"Deploy latest commit"**

3. Attendez le redéploiement

4. Réessayez d'accéder à `/setup/`

---

## 💡 Astuce : Vérifier les Logs en Temps Réel

Dans Render > Web Service > **Logs**, vous pouvez voir les logs en temps réel. 

Quand vous accédez à `/setup/`, regardez les logs pour voir l'erreur exacte qui se produit.

---

## 📞 Dites-moi

1. **Quelle erreur voyez-vous** dans les logs Render ?
2. **À quelle étape** l'erreur se produit-elle ? (chargement de la page, clic sur un bouton, etc.)
3. **Les variables d'environnement** sont-elles correctement configurées ?

Avec ces informations, je pourrai vous aider à résoudre le problème précisément ! 🔧

