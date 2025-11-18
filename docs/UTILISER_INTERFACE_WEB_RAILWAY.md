# 🌐 Utiliser l'Interface Web Railway (Plus Simple)

## ✅ Pas besoin de Railway CLI !

Vous pouvez tout faire directement depuis l'interface web de Railway. C'est plus simple !

---

## 🎯 Pour le Terminal : Utiliser l'Interface Web

### Option 1 : Via l'onglet "Deployments"

1. Dans Railway, allez dans votre **service Django**
2. Cliquez sur l'onglet **"Deployments"** (en haut)
3. Cliquez sur le **dernier déploiement** (celui qui est actif)
4. Dans la page du déploiement, cherchez :
   - Un bouton **"Shell"**
   - Un bouton **"Terminal"**
   - Un onglet **"Shell"**
   - Un bouton **"Open Shell"**
5. Cliquez dessus pour ouvrir le terminal

### Option 2 : Via le menu du service

1. Dans votre service Django, cherchez dans le menu :
   - Un bouton **"Shell"** ou **"Terminal"**
   - Un menu **"..."** (trois points) avec option "Shell"
2. Cliquez dessus

---

## 🗄️ Pour la Base de Données : Créer PostgreSQL dans Railway

### Étapes simples :

1. Dans Railway, allez dans votre **projet** (pas le service Django)
2. Cliquez sur **"New"** (bouton vert en haut à droite)
3. Sélectionnez **"Database"** > **"Add PostgreSQL"**
4. Railway va créer automatiquement une base PostgreSQL

### Obtenir l'URL de connexion :

1. Cliquez sur le **service PostgreSQL** créé
2. Allez dans **"Variables"**
3. Copiez la valeur de **`DATABASE_URL`**

### Configurer votre service Django :

1. Allez dans votre **service Django**
2. Allez dans **"Variables"**
3. Ajoutez ou modifiez **`DATABASE_URL`** avec l'URL copiée
4. Redéployez votre service Django

---

## 📝 Variables d'Environnement à Configurer

Dans votre service Django > Variables, assurez-vous d'avoir :

```
SECRET_KEY=votre-cle-secrete-generee
DEBUG=False
ALLOWED_HOSTS=*.railway.app
DATABASE_URL=postgresql://postgres:motdepasse@containers-us-west-xxx.railway.app:5432/railway
```

(Remplacez `DATABASE_URL` par l'URL de votre base PostgreSQL Railway)

---

## 🚀 Après le Déploiement

Une fois votre service Django déployé avec la base de données :

1. **Trouvez le terminal** via l'interface web (voir Option 1 ci-dessus)
2. **Lancez les migrations** :
   ```bash
   python manage.py migrate --noinput
   ```
3. **Collectez les fichiers statiques** :
   ```bash
   python manage.py collectstatic --noinput
   ```
4. **Créez un superutilisateur** :
   ```bash
   python manage.py createsuperuser
   ```

---

## 🆘 Si vous ne trouvez toujours pas le terminal

### Solution : Utiliser les logs pour vérifier

Même sans terminal, vous pouvez vérifier que tout fonctionne :

1. Allez dans **"Deployments"** > dernier déploiement > **"Logs"**
2. Vérifiez qu'il n'y a pas d'erreurs
3. Si vous voyez des erreurs de base de données, c'est que `DATABASE_URL` n'est pas correcte

### Les migrations peuvent attendre

Si vous ne trouvez pas le terminal maintenant, ce n'est pas grave ! Vous pouvez :
1. D'abord vous assurer que le déploiement fonctionne
2. Trouver le terminal plus tard pour lancer les migrations

---

## 💡 Astuce

Le terminal Railway dans l'interface web ressemble souvent à une fenêtre de terminal intégrée dans la page. Cherchez une zone avec un prompt `$` ou `#` où vous pouvez taper des commandes.

---

**Essayez de trouver le terminal via l'onglet "Deployments" - c'est là qu'il se trouve généralement !** 🚀

