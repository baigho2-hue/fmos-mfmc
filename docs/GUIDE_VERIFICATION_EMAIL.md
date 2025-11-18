# Guide - Système de Vérification par Email

## 🔧 Configuration Actuelle

En mode **développement** (DEBUG=True), le système utilise le **backend console** pour les emails. Cela signifie que :
- ✅ Les emails ne sont **pas envoyés** par SMTP
- ✅ Les codes de vérification sont **affichés dans la console** du serveur Django
- ✅ Aucune configuration SMTP n'est nécessaire pour les tests

## 📋 Comment Utiliser le Système de Connexion

### 1. Démarrer le serveur Django

```bash
python manage.py runserver
```

### 2. Se connecter

1. Aller sur : http://127.0.0.1:8000/login/
2. Entrer votre **username** et **password**
3. Cliquer sur "Se connecter"

### 3. Récupérer le code de vérification

Après avoir entré vos identifiants, le code de vérification sera affiché dans la **console du serveur Django** :

```
============================================================
CODE DE VERIFICATION (MODE DEVELOPPEMENT)
============================================================
Utilisateur: etudiant1 (etudiant1@fmos-mfmc.ml)
Code: 123456
Valide jusqu'à: 2025-11-10 16:10:00+00:00
============================================================
```

4. **Copier le code** affiché dans la console
5. **Entrer le code** dans le formulaire de vérification sur la page web
6. Cliquer sur "Vérifier"

## 🔍 Récupérer un Code depuis la Base de Données

Si vous avez besoin de récupérer un code de vérification :

```bash
python manage.py recuperer_code_verification --username etudiant1
```

Ou par email :
```bash
python manage.py recuperer_code_verification --email etudiant1@fmos-mfmc.ml
```

## ⚠️ En Cas d'Erreur

Si vous voyez l'erreur `[WinError 10061]`, cela signifie que le système essaie d'utiliser SMTP. 

### Solution 1 : Vérifier que DEBUG est True

Vérifiez dans `core/settings.py` :
```python
DEBUG = os.getenv('DEBUG', 'True') == 'True'
```

### Solution 2 : Redémarrer le serveur

Après toute modification de `settings.py`, **redémarrez le serveur Django** :
1. Arrêter le serveur (Ctrl+C)
2. Relancer : `python manage.py runserver`

### Solution 3 : Vérifier la configuration

```bash
python -c "from core import settings; print(f'DEBUG: {settings.DEBUG}'); print(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')"
```

Vous devriez voir :
```
DEBUG: True
EMAIL_BACKEND: django.core.mail.backends.console.EmailBackend
```

## 🚀 Pour la Production

Quand vous passerez en production, vous devrez :

1. **Configurer DEBUG = False** dans les variables d'environnement
2. **Configurer les paramètres SMTP** dans le fichier `.env` :
   ```
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=votre-email@gmail.com
   EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
   DEFAULT_FROM_EMAIL=noreply@fmos-mfmc.ml
   ```

## 📝 Identifiants de Test

### Étudiants
- Username: `etudiant1`, `etudiant2`, etc.
- Password: `etudiant123`

### Enseignants
- Username: `enseignant1`, `enseignant2`, etc.
- Password: `enseignant123`

### Superutilisateur
- Username: `admin`
- Password: `admin123`

## 💡 Astuce

Pour faciliter les tests, vous pouvez aussi **désactiver temporairement la vérification par email** en modifiant la vue `login_view` dans `core/views.py`, mais il est recommandé de garder le système actif pour tester le flux complet.

