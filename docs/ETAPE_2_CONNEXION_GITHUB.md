# 🔗 Étape 2 : Connecter à GitHub

## Option 1 : Si vous avez votre URL GitHub

Exécutez cette commande (remplacez VOTRE_USERNAME) :

```powershell
git remote add origin https://github.com/VOTRE_USERNAME/fmos-mfmc.git
git push -u origin main
```

## Option 2 : Si vous avez créé le repository avec SSH

```powershell
git remote add origin git@github.com:VOTRE_USERNAME/fmos-mfmc.git
git push -u origin main
```

## Vérification

Après avoir exécuté les commandes, vérifiez avec :

```powershell
git remote -v
```

Vous devriez voir votre repository GitHub listé.

---

**Une fois fait, dites-moi "étape 2 connexion terminée" pour passer à l'étape 3 (Déploiement sur Railway)**

