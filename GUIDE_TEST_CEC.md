# Guide de Test - Utilisateur CEC (Chargé d'Encadrement Clinique)

## 📋 Informations de Connexion

Un utilisateur CEC de test a été créé avec les identifiants suivants :

- **Username:** `cec_test`
- **Email:** `cec_test@fmos-mfmc.ml`
- **Password:** `cec123456`
- **Nom:** Dr. Mamadou Cissé
- **Statut:** Enseignant + Superviseur/CEC
- **Email vérifié:** Oui
- **Actif:** Oui
- **Centre de supervision:** Assigné automatiquement (si disponible)

## 🔗 URLs Importantes

Pour faciliter vos tests, voici toutes les URLs importantes :

- **Connexion:** http://127.0.0.1:8000/login/
- **Dashboard enseignant:** http://127.0.0.1:8000/dashboard/enseignant/
- **Évaluations de stages:** http://127.0.0.1:8000/superviseur/evaluations-stages/
- **Activer 2FA:** http://127.0.0.1:8000/2fa/activer/
- **Vérifier code 2FA:** http://127.0.0.1:8000/2fa/verifier/
- **Désactiver 2FA:** http://127.0.0.1:8000/2fa/desactiver/
- **Django Admin:** http://127.0.0.1:8000/admin/

## 🧪 Scénarios de Test

### 1. Connexion et Accès Initial

1. **Se connecter**
   - URL: http://127.0.0.1:8000/login/
   - Entrer: `cec_test` / `cec123456`
   - Vous devriez être redirigé vers le dashboard enseignant

2. **Vérifier le menu**
   - Dans le menu "Espace Enseignant", vous devriez voir :
     - Tableau de bord
     - **📋 Évaluations de stages** (visible uniquement pour les superviseurs/CEC)
     - 🔐 Double authentification

3. **Note importante sur le centre de supervision**
   - L'utilisateur de test peut avoir un centre de supervision assigné automatiquement
   - Si un centre est assigné, les évaluations seront automatiquement filtrées par ce centre lors de l'accès
   - Pour modifier ou assigner un centre, voir la section "🔍 Vérifications dans Django Admin"

### 2. Test de l'Accès aux Évaluations de Stages (Sans 2FA)

1. **Tenter d'accéder aux évaluations**
   - Cliquer sur "📋 Évaluations de stages"
   - Vous devriez être redirigé vers la page d'activation du 2FA
   - Message: "Cette fonctionnalité nécessite la double authentification"

### 3. Activation du 2FA

1. **Activer le 2FA**
   - URL: http://127.0.0.1:8000/2fa/activer/
   - Cliquer sur "📧 Envoyer le code de vérification"
   - Un code à 6 chiffres sera envoyé par email
   - **En mode développement:** Le code est également affiché dans la console du serveur Django

2. **Vérifier le code**
   - URL: http://127.0.0.1:8000/2fa/verifier/
   - Entrer le code à 6 chiffres reçu
   - Cliquer sur "✅ Vérifier et Activer"
   - Message de succès: "Double authentification activée avec succès !"

### 4. Accès aux Évaluations de Stages (Avec 2FA)

1. **Accéder aux évaluations**
   - Cliquer sur "📋 Évaluations de stages"
   - Si c'est la première fois dans cette session, un code 2FA sera demandé
   - Entrer le code reçu par email
   - Vous devriez accéder à la liste des évaluations de stages

2. **Vérifier le filtrage automatique**
   - Si un centre de supervision est assigné, un message informatif s'affiche en haut
   - Les évaluations sont automatiquement filtrées par votre centre de supervision
   - La période actuelle est également affichée selon le calendrier :
     - **Période 1** : janvier-avril
     - **Période 2** : mai-août
     - **Hors période** : septembre-décembre
   - L'année scolaire actuelle est affichée (format YYYY-YYYY)

3. **Filtrer par classe**
   - Sélectionner une classe dans le filtre (ex: "DESMFMC 1ère année")
   - La liste des évaluations pour cette classe s'affiche
   - Les filtres manuels prennent priorité sur le filtrage automatique

4. **Filtrer par centre ou répartition**
   - Utiliser le filtre "Filtrer par centre/lieu" pour voir tous les étudiants d'un centre
   - Utiliser le filtre "Filtrer par répartition de stage" pour une répartition spécifique
   - Ces filtres permettent d'affiner les résultats au-delà du filtrage automatique

5. **Remplir une évaluation**
   - Cliquer sur "Remplir" pour une évaluation
   - Remplir les champs de l'évaluation
   - Ajouter des compétences si nécessaire
   - Enregistrer l'évaluation

### 5. Test de Sécurité

1. **Tester avec un enseignant normal**
   - Créer un enseignant sans le statut superviseur/CEC
   - Se connecter avec cet enseignant
   - Vérifier que le lien "Évaluations de stages" n'apparaît pas
   - Tenter d'accéder directement à l'URL: http://127.0.0.1:8000/superviseur/evaluations-stages/
   - Vous devriez voir un message d'erreur: "Accès réservé aux superviseurs cliniques et CEC"

2. **Tester l'expiration du code 2FA**
   - Attendre 5 minutes après la génération d'un code
   - Essayer d'utiliser le code expiré
   - Vous devriez voir un message d'erreur: "Code invalide ou expiré"

3. **Tester l'expiration de la session 2FA**
   - Après avoir vérifié le 2FA, attendre 30 minutes
   - Tenter d'accéder à nouveau aux évaluations
   - Un nouveau code devrait être demandé

## 🔍 Vérifications dans Django Admin

1. **Vérifier le statut de l'utilisateur**
   - Aller dans Django Admin: http://127.0.0.1:8000/admin/
   - Utilisateurs → Rechercher "cec_test"
   - Vérifier que:
     - Type d'utilisateur: Enseignant
     - Superviseur clinique / CEC: ✅ (coché)
     - Email vérifié: ✅ (coché)
     - Actif: ✅ (coché)

2. **Vérifier les codes 2FA**
   - Aller dans "Codes 2FA"
   - Vous devriez voir les codes générés pour cet utilisateur
   - Vérifier les dates d'expiration et les statuts (utilisé/non utilisé)

3. **Assigner un centre de supervision**
   - Dans la fiche de l'utilisateur `cec_test`
   - Trouver le champ "Centre de supervision principal"
   - Sélectionner un centre CSCom-U dans la liste déroulante
   - Sauvegarder
   - Après cette configuration, les évaluations seront automatiquement filtrées par ce centre

## 📝 Checklist de Test

- [ ] Connexion réussie avec `cec_test`
- [ ] Menu "Évaluations de stages" visible
- [ ] Redirection vers 2FA si non activé
- [ ] Activation du 2FA réussie
- [ ] Code 2FA reçu par email (ou console en dev)
- [ ] Accès aux évaluations de stages après vérification 2FA
- [ ] Message de période actuelle affiché (selon le mois)
- [ ] Filtrage automatique par centre fonctionnel (si centre assigné)
- [ ] Filtrage par classe fonctionnel
- [ ] Filtrage par centre/lieu fonctionnel
- [ ] Filtrage par répartition fonctionnel
- [ ] Remplissage d'évaluation fonctionnel
- [ ] Enseignant normal ne peut pas accéder
- [ ] Code 2FA expire après 5 minutes
- [ ] Session 2FA expire après 30 minutes

## 🐛 Dépannage

### Le code 2FA n'arrive pas par email

En mode développement (DEBUG=True), le code est affiché dans la console du serveur Django. Vérifiez la console où vous avez lancé `python manage.py runserver`.

### Impossible d'accéder aux évaluations

1. Vérifiez que le statut "Superviseur clinique / CEC" est coché dans Django Admin
2. Vérifiez que le 2FA est activé
3. Vérifiez que vous avez entré le code 2FA correctement

### Message "Accès refusé"

Assurez-vous que:
- L'utilisateur est de type "Enseignant"
- Le champ "Superviseur clinique / CEC" est coché
- L'utilisateur est actif
- L'email est vérifié

## 🔄 Recréer l'utilisateur de test

Si vous devez recréer l'utilisateur de test, exécutez:

```bash
python manage.py creer_cec_test
```

Cette commande créera ou mettra à jour l'utilisateur `cec_test` avec le statut CEC et assignera automatiquement un centre de supervision si disponible.

## 📅 Système de Périodes

Le système détermine automatiquement la période actuelle selon le calendrier de l'année scolaire :

- **Période 1** : janvier-avril (mois 1-4)
- **Période 2** : mai-août (mois 5-8)
- **Hors période** : septembre-décembre (mois 9-12)

L'année scolaire suit le format "YYYY-YYYY" et commence en septembre.

### Comportement du filtrage automatique

1. **Si vous avez un centre de supervision assigné** :
   - Les évaluations sont automatiquement filtrées par votre centre
   - Si une période est active, les évaluations sont également filtrées par cette période
   - Un message informatif s'affiche en haut de la page

2. **Si aucun centre n'est assigné** :
   - Toutes les évaluations sont affichées (sans filtre automatique)
   - Vous pouvez toujours utiliser les filtres manuels

3. **Priorité des filtres** :
   - Filtre manuel par répartition (priorité la plus élevée)
   - Filtre manuel par centre
   - Filtre manuel par classe
   - Filtre automatique par centre + période (si aucun filtre manuel)

## 📞 Support

Pour toute question ou problème lors des tests, vérifiez:
1. Les logs Django dans la console
2. Les messages d'erreur dans l'interface
3. La configuration dans Django Admin

