# 🚀 Initialisation du Site sur Render

Ce guide vous accompagne pour initialiser votre site Django après le déploiement sur Render.

---

## 📋 Prérequis

- ✅ Site déployé sur Render
- ✅ Application accessible (même si elle affiche des erreurs)
- ✅ Base de données PostgreSQL créée et connectée
- ✅ Variables d'environnement configurées

---

## 🎯 Méthode 1 : Utilisation du Shell Render (Recommandé)

### Étape 1 : Ouvrir le Shell Render

1. Allez sur [render.com](https://render.com)
2. Cliquez sur votre **Web Service** `fmos-mfmc`
3. Cliquez sur **"Shell"** (en haut à droite)
4. Un terminal s'ouvrira dans votre navigateur

### Étape 2 : Appliquer les Migrations

Dans le Shell, exécutez :

```bash
python manage.py migrate
```

**Résultat attendu** : Vous devriez voir les migrations s'appliquer une par une.

**Vérifier l'état** :
```bash
python manage.py showmigrations
```

Toutes les migrations doivent avoir un `[X]` (appliquées).

### Étape 3 : Créer un Superutilisateur

```bash
python manage.py createsuperuser
```

**Entrez les informations** :
- **Username** : `admin` (ou votre choix)
- **Email** : `votre@email.com`
- **Password** : `VotreMotDePasse123!` (choisissez un mot de passe fort)

**Note** : Le mot de passe ne s'affichera pas pendant la saisie (c'est normal).

**Alternative** : Si vous avez une commande personnalisée :
```bash
python manage.py creer_superuser
```

### Étape 4 : Initialiser le Programme DESMFMC

Pour initialiser la structure complète du programme :

```bash
python manage.py init_programme_desmfmc_detaille
```

**Ou pour la structure de base** :
```bash
python manage.py init_programme_desmfmc
```

**Résultat attendu** : Le programme DESMFMC sera créé avec tous ses jalons, modules et cours.

### Étape 5 : Initialiser les Coûts de Formations (Optionnel)

```bash
python manage.py init_couts_formations
```

### Étape 6 : Vérifier que Tout Fonctionne

#### Vérifier l'accès à l'admin :

1. Ouvrez votre navigateur
2. Allez sur : `https://fmos-mfmc.onrender.com/admin/`
3. Connectez-vous avec votre superutilisateur
4. Vous devriez voir le tableau de bord Django

#### Vérifier la base de données :

Dans le Shell Render :

```bash
python manage.py shell
```

Puis dans le shell Python :

```python
from apps.utilisateurs.models import Utilisateur
print(f"Nombre d'utilisateurs : {Utilisateur.objects.count()}")
print(f"Superutilisateurs : {Utilisateur.objects.filter(is_superuser=True).count()}")
exit()
```

#### Tester le site :

- **Page d'accueil** : `https://fmos-mfmc.onrender.com`
- **Admin** : `https://fmos-mfmc.onrender.com/admin/`

---

## 🎯 Méthode 2 : Utilisation de l'Interface Web Setup (Alternative)

Si vous avez configuré les vues setup temporaires, vous pouvez utiliser l'interface web.

### ⚠️ Important : Configuration du Token

1. Dans Render > Web Service > **Environment**
2. Ajoutez la variable :
   - **Key** : `SETUP_SECRET_TOKEN`
   - **Value** : `VotreTokenSecretTresLongEtComplexe123!`
3. Cliquez sur **"Save Changes"**

### Accéder à l'Interface Setup

1. Ouvrez votre navigateur
2. Allez sur : `https://fmos-mfmc.onrender.com/setup/?token=VotreTokenSecretTresLongEtComplexe123!`
3. Utilisez les boutons pour :
   - Appliquer les migrations
   - Créer un superutilisateur
   - Initialiser le programme DESMFMC
   - Vérifier le statut

### ⚠️ Sécurité

**IMPORTANT** : Supprimez les vues setup après l'initialisation pour des raisons de sécurité !

Pour supprimer :
1. Supprimez les routes dans `core/urls.py` (lignes 159-165)
2. Supprimez l'import `views_setup` (ligne 13)
3. Supprimez le fichier `core/views_setup.py`
4. Redéployez

---

## 📝 Checklist d'Initialisation

### Configuration de Base
- [ ] Migrations appliquées (`python manage.py migrate`)
- [ ] Superutilisateur créé (`python manage.py createsuperuser`)
- [ ] Accès à l'admin vérifié (`/admin/`)

### Configuration du Programme
- [ ] Programme DESMFMC initialisé (`init_programme_desmfmc_detaille`)
- [ ] Coûts de formations initialisés (`init_couts_formations`)

### Vérifications
- [ ] Site accessible sur `https://fmos-mfmc.onrender.com`
- [ ] Admin accessible et fonctionnel
- [ ] Base de données contient des données (utilisateurs, programme, etc.)

---

## 🔧 Commandes Utiles Supplémentaires

### Créer des Utilisateurs de Test

```bash
python manage.py creer_utilisateurs_test
```

### Attribuer des Classes DESMFMC

```bash
python manage.py attribuer_classes_desmfmc
```

### Vérifier les Logs

Dans Render > Web Service > **Logs**, vous pouvez voir :
- Les erreurs éventuelles
- Les requêtes HTTP
- Les messages de l'application

---

## 🆘 Résolution de Problèmes

### Problème : Les migrations échouent

**Solution** :
1. Vérifiez que `DATABASE_URL` est correcte dans Render > Environment
2. Vérifiez que la base PostgreSQL est active
3. Essayez de réinitialiser : `python manage.py migrate --run-syncdb`

### Problème : Impossible de créer un superutilisateur

**Solution** :
1. Vérifiez que les migrations sont appliquées
2. Utilisez la commande personnalisée : `python manage.py creer_superuser`
3. Vérifiez les logs Render pour voir les erreurs

### Problème : Le programme DESMFMC ne s'initialise pas

**Solution** :
1. Vérifiez les logs dans le Shell Render
2. Essayez la version de base : `python manage.py init_programme_desmfmc`
3. Vérifiez que la base de données est accessible

### Problème : Erreur 500 sur le site

**Solution** :
1. Activez temporairement `DEBUG=True` dans Render > Environment
2. Consultez les logs Render pour voir l'erreur exacte
3. Vérifiez que toutes les migrations sont appliquées
4. Remettez `DEBUG=False` après résolution

---

## ✅ Après l'Initialisation

Une fois l'initialisation terminée :

1. **Testez toutes les fonctionnalités** :
   - Connexion/Inscription
   - Navigation dans le site
   - Accès aux cours
   - Administration

2. **Configurez les emails** (si nécessaire) :
   - Ajoutez les variables d'environnement pour SMTP
   - Testez l'envoi d'emails

3. **Configurez les fichiers statiques** :
   - Vérifiez que les CSS/JS se chargent correctement
   - Vérifiez que les images s'affichent

4. **Supprimez les vues setup** (si utilisées) :
   - Pour des raisons de sécurité
   - Suivez les instructions ci-dessus

---

## 📚 Documentation Supplémentaire

- **Guide complet Render** : `GUIDE_RENDER_COMPLET.md`
- **Configuration rapide** : `CONFIGURATION_RENDER_RAPIDE.md`
- **Résolution de problèmes** : `RESOLUTION_BAD_GATEWAY_RENDER.md`

---

## 🎉 Félicitations !

Votre site est maintenant initialisé et prêt à être utilisé !

Pour toute question ou problème, consultez les guides de résolution de problèmes ou les logs Render.

---

**Dernière mise à jour** : Novembre 2025

