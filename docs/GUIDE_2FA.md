# Guide - Double Authentification (2FA)

## 🔐 Vue d'ensemble

Le système de double authentification (2FA) ajoute une couche supplémentaire de sécurité pour les fonctionnalités sensibles de la plateforme FMOS MFMC. Il est particulièrement recommandé pour les superviseurs cliniques, CEC et membres de la coordination.

## 📋 Fonctionnalités

### 1. Activation du 2FA

Pour activer la double authentification :

1. Connectez-vous à votre compte
2. Allez dans **Espace Enseignant** → **🔐 Double authentification**
3. Cliquez sur **"Envoyer le code de vérification"**
4. Un code à 6 chiffres sera envoyé à votre adresse email
5. Entrez le code reçu dans le formulaire de vérification
6. Le 2FA sera activé pour votre compte

### 2. Utilisation du 2FA

Une fois activé, le 2FA sera requis pour accéder aux fonctionnalités suivantes :

- **Évaluations de stages** (superviseurs/CEC)
- Toutes les fonctionnalités administratives sensibles

Lors de l'accès à une fonctionnalité protégée :

1. Un code de vérification sera automatiquement envoyé à votre email
2. Entrez le code dans le formulaire de vérification
3. La vérification est valide pendant **30 minutes** pour cette session
4. Après 30 minutes, une nouvelle vérification sera requise

### 3. Désactivation du 2FA

Pour désactiver la double authentification :

1. Allez dans **Espace Enseignant** → **🔐 Double authentification**
2. Cliquez sur **"Désactiver le 2FA"**
3. Un code de vérification sera envoyé à votre email
4. Entrez le code pour confirmer la désactivation

## 🔧 Configuration Technique

### Modèles

- **`Utilisateur.deux_facteurs_actives`** : Champ booléen indiquant si le 2FA est activé pour l'utilisateur
- **`Code2FA`** : Modèle stockant les codes de vérification temporaires

### Décorateur `@deux_facteurs_required`

Pour protéger une vue avec le 2FA, utilisez le décorateur :

```python
from core.views_2fa import deux_facteurs_required

@deux_facteurs_required
def ma_vue_protegee(request):
    # Votre code ici
    pass
```

### Vérification automatique

Le système vérifie automatiquement si le 2FA est requis pour :
- Les enseignants (superviseurs/CEC)
- Les membres de la coordination

## 📧 Envoi des codes

### Mode développement (DEBUG=True)

En mode développement, les codes sont :
- Envoyés par email (si configuré)
- **Affichés dans la console du serveur Django** pour faciliter les tests

Exemple de sortie console :
```
============================================================
CODE 2FA (MODE DEVELOPPEMENT)
============================================================
Utilisateur: enseignant1 (enseignant1@fmos-mfmc.ml)
Code 2FA: 123456
Valide jusqu'à: 2025-11-15 10:30:00+00:00
============================================================
```

### Mode production (DEBUG=False)

En production, les codes sont uniquement envoyés par email via SMTP.

## ⚙️ Paramètres des codes

- **Durée de validité** : 5 minutes
- **Format** : 6 chiffres (000000-999999)
- **Session** : La vérification est valide pendant 30 minutes après entrée du code

## 🔒 Sécurité

### Mesures de sécurité implémentées

1. **Codes à usage unique** : Chaque code ne peut être utilisé qu'une seule fois
2. **Expiration automatique** : Les codes expirent après 5 minutes
3. **Enregistrement des tentatives** : L'adresse IP et le User-Agent sont enregistrés pour chaque code
4. **Validation de session** : La vérification expire après 30 minutes d'inactivité
5. **Vérification du type d'utilisateur** : Seuls les enseignants et la coordination peuvent activer le 2FA

### Bonnes pratiques

- Activez le 2FA pour tous les comptes avec accès aux données sensibles
- Ne partagez jamais vos codes de vérification
- Vérifiez régulièrement votre boîte email pour les codes
- Désactivez le 2FA uniquement si nécessaire et en toute sécurité

## 🐛 Dépannage

### Le code n'arrive pas par email

1. Vérifiez votre dossier spam/courrier indésirable
2. Vérifiez que votre adresse email est correcte dans votre profil
3. En mode développement, vérifiez la console du serveur Django
4. Contactez l'administration si le problème persiste

### Le code a expiré

1. Demandez un nouveau code en cliquant sur "Renvoyer le code"
2. Les codes expirent après 5 minutes pour des raisons de sécurité

### Impossible d'accéder à une fonctionnalité protégée

1. Assurez-vous que le 2FA est activé pour votre compte
2. Vérifiez que vous êtes connecté avec un compte enseignant ou coordination
3. Vérifiez que votre session 2FA n'a pas expiré (30 minutes)

## 📝 Exemple d'utilisation

### Pour un superviseur/CEC

1. **Première utilisation** :
   - Se connecter avec nom d'utilisateur et mot de passe
   - Aller dans "Espace Enseignant" → "🔐 Double authentification"
   - Activer le 2FA en suivant les étapes

2. **Accès aux évaluations de stages** :
   - Cliquer sur "📋 Évaluations de stages"
   - Un code sera envoyé automatiquement
   - Entrer le code pour accéder à la fonctionnalité
   - La vérification reste valide pendant 30 minutes

### Pour la coordination

Le processus est identique, avec accès aux fonctionnalités administratives protégées.

## 🔄 Migration et mise à jour

Pour ajouter le 2FA à une nouvelle vue :

```python
from core.views_2fa import deux_facteurs_required

@login_required
@deux_facteurs_required
def ma_nouvelle_vue(request):
    # Votre code ici
    pass
```

## 📞 Support

Pour toute question ou problème lié au 2FA, contactez l'administration de la plateforme.

