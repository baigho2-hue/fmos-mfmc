# 🚀 Déploiement Rapide des Vues Setup

Guide rapide pour déployer les vues setup sur Render.

---

## ⚡ Étapes Rapides

### 1️⃣ Ajouter les Fichiers à Git

```bash
git add core/views_setup.py core/startup.py core/urls.py core/wsgi.py render.yaml
```

### 2️⃣ Commiter

```bash
git commit -m "Ajout des vues setup pour initialisation Render"
```

### 3️⃣ Pousser sur GitHub

```bash
git push origin main
```

(ou `git push origin master` si votre branche principale s'appelle `master`)

### 4️⃣ Attendre le Redéploiement Render

1. Allez sur [render.com](https://render.com)
2. Cliquez sur votre **Web Service** `fmos-mfmc`
3. Surveillez le déploiement (2-5 minutes)

### 5️⃣ Tester

Une fois le déploiement terminé, accédez à :
```
https://fmos-mfmc.onrender.com/setup/?token=FMOS2024ConfigSecret!
```

---

## ✅ Vérification

Si vous voyez l'interface setup avec les boutons, c'est que tout fonctionne !

---

## 🆘 Si ça ne Fonctionne Toujours Pas

Consultez : **`RESOLUTION_404_SETUP.md`**

