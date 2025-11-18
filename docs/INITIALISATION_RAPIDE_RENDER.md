# ⚡ Initialisation Rapide du Site sur Render

Guide rapide pour initialiser votre site en 5 minutes.

---

## 🚀 Étapes Rapides

### 1️⃣ Ouvrir le Shell Render

1. Allez sur [render.com](https://render.com)
2. Cliquez sur votre **Web Service** `fmos-mfmc`
3. Cliquez sur **"Shell"** (en haut à droite)

### 2️⃣ Copier-Coller ces Commandes

Exécutez les commandes suivantes **une par une** dans le Shell :

#### Étape 1 : Migrations
```bash
python manage.py migrate
```

#### Étape 2 : Créer un Superutilisateur
```bash
python manage.py createsuperuser
```
**Entrez** : username, email, password

#### Étape 3 : Initialiser le Programme DESMFMC
```bash
python manage.py init_programme_desmfmc_detaille
```

#### Étape 4 : Initialiser les Coûts (Optionnel)
```bash
python manage.py init_couts_formations
```

---

## ✅ Vérification

### Tester l'Admin

1. Ouvrez : `https://fmos-mfmc.onrender.com/admin/`
2. Connectez-vous avec votre superutilisateur
3. Vous devriez voir le tableau de bord Django

### Vérifier la Base de Données

Dans le Shell :
```bash
python manage.py shell
```

Puis :
```python
from apps.utilisateurs.models import Utilisateur
print(f"Utilisateurs : {Utilisateur.objects.count()}")
exit()
```

---

## 🎉 C'est Fait !

Votre site est maintenant initialisé et prêt à être utilisé.

---

## 📚 Documentation Complète

Pour plus de détails, consultez : **`INITIALISATION_SITE_RENDER.md`**

