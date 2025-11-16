# 🔧 Configurer Railway sans Post Deploy Command

## 📍 Où trouver les options de déploiement dans Railway

### Option 1 : Vérifier dans Settings

1. Dans votre service Django, cliquez sur **"Settings"** (icône ⚙️)
2. Cherchez les sections :
   - **"Build Command"** ou **"Build"**
   - **"Start Command"** ou **"Start"**
   - **"Deploy"** ou **"Deployment"**

### Option 2 : Railway détecte automatiquement

Railway détecte automatiquement votre `Procfile`, donc la commande de démarrage devrait être correcte.

---

## ✅ Solution : Lancer les migrations manuellement après le déploiement

Si vous ne trouvez pas "Post Deploy Command", pas de problème ! Vous pouvez lancer les migrations manuellement une fois le déploiement terminé.

### Étape 1 : Attendre que le déploiement soit terminé

Attendez que Railway affiche **"Deploy successful"** ou **"Active"**.

### Étape 2 : Ouvrir le terminal Railway

1. Dans votre service Django, allez dans l'onglet **"Deployments"**
2. Cliquez sur le dernier déploiement (celui qui est actif)
3. Cherchez un bouton **"View Logs"** ou **"Open Terminal"** ou **"Shell"**
4. Cliquez dessus pour ouvrir un terminal

### Étape 3 : Lancer les migrations

Dans le terminal Railway, exécutez :

```bash
python manage.py migrate --noinput
```

### Étape 4 : Collecter les fichiers statiques

```bash
python manage.py collectstatic --noinput
```

---

## 🔄 Alternative : Créer un script de démarrage

Si vous voulez automatiser cela, vous pouvez créer un script qui lance les migrations au démarrage.

### Créer un fichier `release.sh`

Créez un fichier `release.sh` à la racine de votre projet :

```bash
#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

### Rendre le script exécutable

Dans votre terminal local :

```bash
git add release.sh
git commit -m "Ajout script release pour migrations automatiques"
git push origin main
```

Railway détectera automatiquement ce script et l'exécutera avant le démarrage.

---

## 📝 Pour l'instant : Procédez sans Post Deploy Command

**C'est OK de ne pas avoir Post Deploy Command !**

1. ✅ Configurez les 4 variables d'environnement
2. ✅ Laissez Railway déployer automatiquement
3. ✅ Une fois déployé, ouvrez le terminal Railway
4. ✅ Lancez les migrations manuellement

---

## 🎯 Prochaines étapes

1. **Configurez les variables** (si pas encore fait)
2. **Lancez le déploiement**
3. **Attendez qu'il soit terminé**
4. **Ouvrez le terminal Railway**
5. **Lancez les migrations manuellement**

Dites-moi quand le déploiement est terminé et je vous guiderai pour lancer les migrations ! 🚀

