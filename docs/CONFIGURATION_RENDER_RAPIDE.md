# ⚡ Configuration Rapide du Site Render

Votre site est déployé sur **`fmos-mfmc.onrender.com`**. Suivez ces étapes pour le configurer :

---

## 🚀 Étapes Rapides (5 minutes)

### 1️⃣ Ouvrir le Shell Render

1. Allez sur [render.com](https://render.com)
2. Cliquez sur votre **Web Service** `fmos-mfmc`
3. Cliquez sur **"Shell"** (en haut à droite)

### 2️⃣ Appliquer les Migrations

Dans le Shell, exécutez :

```bash
python manage.py migrate
```

Attendez que les migrations soient appliquées.

### 3️⃣ Créer un Superutilisateur

```bash
python manage.py createsuperuser
```

Entrez :
- **Username** : `admin` (ou votre choix)
- **Email** : `votre@email.com`
- **Password** : `VotreMotDePasse123!` (choisissez un mot de passe fort)

### 4️⃣ Initialiser le Programme DESMFMC

```bash
python manage.py init_programme_desmfmc_detaille
```

### 5️⃣ Accéder à l'Admin

1. Ouvrez votre navigateur
2. Allez sur : **`https://fmos-mfmc.onrender.com/admin/`**
3. Connectez-vous avec votre superutilisateur

---

## ✅ Vérifications

### Vérifier les Variables d'Environnement

Dans Render > **Web Service** > **Environment**, vérifiez :

- ✅ `SECRET_KEY` : Définie
- ✅ `DEBUG` : `False`
- ✅ `ALLOWED_HOSTS` : `fmos-mfmc.onrender.com`
- ✅ `DATABASE_URL` : URL de votre base PostgreSQL

### Tester le Site

- **Page d'accueil** : `https://fmos-mfmc.onrender.com`
- **Admin Django** : `https://fmos-mfmc.onrender.com/admin/`

---

## 🔧 Commandes Utiles

### Voir l'état des migrations
```bash
python manage.py showmigrations
```

### Créer des utilisateurs de test
```bash
python manage.py creer_utilisateurs_test
```

### Initialiser les coûts de formations
```bash
python manage.py init_couts_formations
```

### Vérifier la base de données
```bash
python manage.py shell
```
Puis dans le shell Python :
```python
from apps.utilisateurs.models import Utilisateur
print(f"Utilisateurs : {Utilisateur.objects.count()}")
exit()
```

---

## 🆘 Problèmes Courants

### Le site ne charge pas

1. Vérifiez les **Logs** dans Render
2. Attendez 30-60 secondes (premier démarrage après "spin down")
3. Vérifiez que `ALLOWED_HOSTS` contient `fmos-mfmc.onrender.com`

### Erreur de connexion à la base de données

1. Vérifiez que `DATABASE_URL` est correcte dans **Environment**
2. Vérifiez que la base PostgreSQL est active dans Render

### Erreur 500

1. Activez temporairement `DEBUG=True` pour voir les erreurs
2. Consultez les **Logs** dans Render
3. Vérifiez que les migrations sont appliquées

---

## 📚 Documentation Complète

Pour plus de détails, consultez : **`DEPLOIEMENT_RENDER_GRATUIT.md`**

---

**Votre site est maintenant configuré ! 🎉**

