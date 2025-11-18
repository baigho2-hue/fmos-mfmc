# 🎯 Guide de Préparation au Déploiement - Étape par Étape

## ✅ Étape 1 : Initialiser Git (si pas déjà fait)

Ouvrez PowerShell ou Terminal dans le dossier de votre projet et exécutez :

```powershell
# Initialiser Git
git init

# Ajouter tous les fichiers
git add .

# Premier commit
git commit -m "Initial commit - Préparation déploiement Railway"
```

## 📤 Étape 2 : Créer un repository sur GitHub

1. Allez sur **https://github.com** et connectez-vous
2. Cliquez sur **"+"** en haut à droite > **"New repository"**
3. Nommez-le : `fmos-mfmc`
4. Choisissez **Public** ou **Private**
5. **NE PAS** cocher "Initialize with README" (vous avez déjà des fichiers)
6. Cliquez sur **"Create repository"**

## 🔗 Étape 3 : Connecter votre projet local à GitHub

GitHub vous donnera des commandes. Utilisez celles-ci :

```powershell
# Ajouter le repository distant (remplacez VOTRE_USERNAME)
git remote add origin https://github.com/VOTRE_USERNAME/fmos-mfmc.git

# Renommer la branche principale en 'main' (si nécessaire)
git branch -M main

# Pousser votre code sur GitHub
git push -u origin main
```

## 🚀 Étape 4 : Déployer sur Railway

Maintenant suivez le guide dans **DEPLOIEMENT_RAILWAY.md** !

---

## 📋 Checklist avant de commencer

- [ ] Projet fonctionne localement (`python manage.py runserver`)
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Fichiers statiques collectés (`python manage.py collectstatic`)
- [ ] Git initialisé
- [ ] Repository GitHub créé
- [ ] Code poussé sur GitHub
- [ ] Compte Railway créé

---

## 🔑 SECRET_KEY générée

Votre SECRET_KEY pour la production :
```
gutp!g9gqbuhq9)514-r*tkds6v3p0r(myo0rvgmgc0svu&0-i
```

**⚠️ IMPORTANT :** Gardez cette clé secrète ! Ne la partagez jamais publiquement.

---

## 📝 Variables d'environnement à configurer sur Railway

Quand vous configurerez Railway, vous aurez besoin de ces variables :

### Obligatoires :
- `SECRET_KEY` = `gutp!g9gqbuhq9)514-r*tkds6v3p0r(myo0rvgmgc0svu&0-i`
- `DEBUG` = `False`
- `ALLOWED_HOSTS` = `votre-projet.railway.app` (Railway vous donnera cette URL)

### Base de données :
Railway créera automatiquement `DATABASE_URL` - vous n'avez rien à faire !

### Optionnelles (pour les emails) :
- `EMAIL_HOST` = `smtp.gmail.com`
- `EMAIL_PORT` = `587`
- `EMAIL_USE_TLS` = `True`
- `EMAIL_HOST_USER` = votre email Gmail
- `EMAIL_HOST_PASSWORD` = mot de passe d'application Gmail
- `DEFAULT_FROM_EMAIL` = `noreply@fmos-mfmc.ml`

---

## 🎬 Prochaines étapes

1. **Maintenant** : Suivez les étapes ci-dessus pour préparer Git et GitHub
2. **Ensuite** : Suivez **DEPLOIEMENT_RAILWAY.md** pour déployer sur Railway
3. **Enfin** : Testez votre site en ligne !

---

## 💡 Besoin d'aide ?

Si vous rencontrez des problèmes :
1. Vérifiez les logs dans Railway Dashboard
2. Vérifiez que toutes les variables d'environnement sont correctes
3. Vérifiez que les migrations sont appliquées
4. Consultez le guide de dépannage dans DEPLOIEMENT_RAILWAY.md

