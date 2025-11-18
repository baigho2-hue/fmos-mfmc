# 🚀 Initialisation du Site SANS Accès au Shell Render

Ce guide vous montre comment initialiser votre site sur Render sans avoir accès au Shell.

---

## 🎯 Méthode 1 : Interface Web Setup (Recommandé)

Cette méthode utilise une interface web sécurisée pour initialiser le site.

### Étape 1 : Configurer le Token Secret

1. Dans Render > Web Service > **Environment**
2. Ajoutez la variable :
   - **Key** : `SETUP_SECRET_TOKEN`
   - **Value** : `VotreTokenSecretTresLongEtComplexe123!` (choisissez un token fort)
3. Cliquez sur **"Save Changes"**

### Étape 2 : Accéder à l'Interface Setup

1. Ouvrez votre navigateur
2. Allez sur : `https://fmos-mfmc.onrender.com/setup/?token=VotreTokenSecretTresLongEtComplexe123!`
3. Vous verrez une interface avec des boutons pour chaque étape

### Étape 3 : Initialiser le Site

Cliquez sur les boutons dans l'ordre :

1. **"Appliquer les migrations"** → Attendez le message de succès
2. **"Créer le superutilisateur"** → Remplissez le formulaire et cliquez sur le bouton
3. **"Initialiser (détaillé)"** → Attendez le message de succès
4. **"Vérifier le statut"** → Vérifiez que tout est OK

### Étape 4 : Vérifier

1. Allez sur : `https://fmos-mfmc.onrender.com/admin/`
2. Connectez-vous avec votre superutilisateur
3. Vérifiez que tout fonctionne

### ⚠️ Important : Sécurité

**Après l'initialisation, supprimez les vues setup** pour des raisons de sécurité :

1. Supprimez les lignes 159-165 dans `core/urls.py`
2. Supprimez la ligne 13 dans `core/urls.py` (`from core import views_setup`)
3. Supprimez le fichier `core/views_setup.py`
4. Poussez les changements sur GitHub
5. Render redéploiera automatiquement

---

## 🎯 Méthode 2 : Commande Post-Deploy Automatique

Cette méthode exécute automatiquement les migrations à chaque déploiement.

### Modifier render.yaml

Ajoutez une commande post-deploy dans `render.yaml` :

```yaml
services:
  - type: web
    name: fmos-mfmc
    # ... autres configurations ...
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

**Note** : Cette méthode applique seulement les migrations automatiquement. Vous devrez toujours créer le superutilisateur et initialiser le programme manuellement via l'interface web setup.

---

## 🎯 Méthode 3 : Script d'Initialisation Automatique

Créez un script qui s'exécute au démarrage de l'application.

### Créer le script

Créez un fichier `core/startup.py` :

```python
# core/startup.py
import os
import sys
from django.core.management import call_command
from django.db import connection

def run_startup_tasks():
    """Exécute les tâches d'initialisation au démarrage"""
    # Vérifier si c'est la première exécution
    if os.environ.get('SKIP_STARTUP', 'False') == 'True':
        return
    
    try:
        # Vérifier la connexion à la base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        # Appliquer les migrations
        call_command('migrate', '--noinput', verbosity=0)
        
        # Vérifier si un superutilisateur existe
        from apps.utilisateurs.models import Utilisateur
        if not Utilisateur.objects.filter(is_superuser=True).exists():
            print("⚠️  Aucun superutilisateur trouvé. Créez-en un via l'interface setup.")
        
        # Vérifier si le programme DESMFMC est initialisé
        from apps.utilisateurs.models_programme_desmfmc import JalonProgramme
        if not JalonProgramme.objects.exists():
            print("⚠️  Programme DESMFMC non initialisé. Utilisez l'interface setup.")
            
    except Exception as e:
        print(f"⚠️  Erreur lors de l'initialisation : {e}")
```

### Modifier wsgi.py

Ajoutez l'appel au démarrage dans `core/wsgi.py` :

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Exécuter les tâches d'initialisation
try:
    from core.startup import run_startup_tasks
    run_startup_tasks()
except Exception as e:
    print(f"Erreur startup : {e}")

application = get_wsgi_application()
```

**Note** : Cette méthode applique automatiquement les migrations mais ne crée pas de superutilisateur automatiquement (pour des raisons de sécurité).

---

## 🎯 Méthode 4 : Utiliser Render Deploy Hook (Si Disponible)

Si votre plan Render le permet, vous pouvez utiliser un Deploy Hook.

1. Dans Render > Web Service > **Settings**
2. Cherchez **"Deploy Hook"** ou **"Post Deploy Command"**
3. Ajoutez : `python manage.py migrate --noinput`

**Note** : Cette option n'est disponible que sur certains plans Render.

---

## 📋 Comparaison des Méthodes

| Méthode | Migrations | Superutilisateur | Programme DESMFMC | Sécurité |
|---------|-----------|------------------|-------------------|----------|
| Interface Web Setup | ✅ | ✅ | ✅ | ⚠️ Token requis |
| Post-Deploy Auto | ✅ | ❌ | ❌ | ✅ |
| Script Startup | ✅ | ⚠️ Vérification | ⚠️ Vérification | ✅ |
| Deploy Hook | ✅ | ❌ | ❌ | ✅ |

---

## 🎯 Recommandation

**Utilisez la Méthode 1 (Interface Web Setup)** car elle :
- ✅ Permet de tout initialiser facilement
- ✅ Ne nécessite pas de Shell
- ✅ Est sécurisée avec un token
- ✅ Donne un retour visuel de chaque étape

**Puis supprimez les vues setup** après l'initialisation pour la sécurité.

---

## 🆘 Résolution de Problèmes

### L'interface setup ne s'affiche pas

1. Vérifiez que les vues setup sont dans `core/urls.py`
2. Vérifiez que `SETUP_SECRET_TOKEN` est défini dans Render
3. Vérifiez que le token dans l'URL correspond exactement

### Les migrations échouent

1. Vérifiez que `DATABASE_URL` est correcte dans Render
2. Vérifiez les logs Render pour voir l'erreur exacte
3. Essayez de redéployer l'application

### Impossible de créer un superutilisateur

1. Vérifiez que les migrations sont appliquées
2. Vérifiez les logs Render pour voir l'erreur
3. Essayez avec un autre username/email

---

## 📚 Documentation Supplémentaire

- **Guide complet** : `INITIALISATION_SITE_RENDER.md`
- **Guide rapide** : `INITIALISATION_RAPIDE_RENDER.md`
- **Configuration Render** : `GUIDE_RENDER_COMPLET.md`

---

**Dernière mise à jour** : Novembre 2025

