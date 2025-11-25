# Système de Gestion des Admissions et Inscriptions

Ce document décrit le système de gestion des admissions et inscriptions pour les formations de la FMOS.

## Fonctionnalités

### 1. Dossiers de Candidature

Les candidats peuvent créer des dossiers de candidature pour différentes formations. Le système gère spécifiquement les dossiers DESMFMC avec des documents requis spécifiques.

#### Documents requis pour DESMFMC (6 documents)

1. **Demande timbrée adressée au doyen de la FMOS** (une copie)
2. **Diplôme de doctorat en médecine générale** : Copie du diplôme (ou attestation) + lettre d'équivalence pour les diplômes étrangers
3. **Autorisation d'inscription de la fonction publique** : Pour les fonctionnaires d'État
4. **Extrait d'acte de naissance** : Ou jugement supplétif
5. **Certificat d'engagement de prise en charge des frais de formation**
6. **Préciser si études prises en charge par une bourse** : Avec détails si applicable

### 2. Processus d'Admission

#### Pour DESMFMC
1. Dépôt du dossier avec tous les documents requis
2. Vérification et validation des documents
3. Examen probatoire écrit
4. Entretien individuel
5. Décision d'admission
6. Inscription administrative

#### Progression DESMFMC (années 1 → 4)

- **Année 1** : inscription administrative unique (paiement validé via `Inscription`).  
- **Fin d'année 1** : la validation du `ResultatAnneeDES` (cours, stages, épreuves) + le paiement annuel (enregistré via `PaiementAnneeDES` pour l'année 2) débloquent automatiquement la classe de 2e année.
- **Années 2 & 3** : même logique – dès que les validations pédagogiques sont « admis » et que les frais annuels sont validés, l'étudiant est automatiquement basculé sur l'année suivante (classe + création du `ResultatAnneeDES` de l'année cible).
- **Année 4** : en plus des validations précédentes, le mémoire doit être validé pour obtenir la décision « diplômé ».

> Important : les frais d'inscription annuels (PaiementAnneeDES) sont exigés en **fin de chaque année** pour ouvrir l'accès aux cours de l'année suivante. La mise à jour de la classe et du `ResultatAnneeDES` est déclenchée automatiquement dès que le paiement passe en statut « validé ».

#### Pour la formation Santé communautaire
1. Dépôt du dossier avec les documents requis (voir ci-dessous)
2. Vérification du dossier et décision d'admission
3. Paiement des frais d'inscription avant le début de la formation

**Documents requis pour Santé communautaire :**
- Demande manuscrite adressée au Doyen (formation précisée)
- Attestation prouvant le niveau minimum Licence
- Extrait d'acte de naissance
- Copie certifiée du diplôme ou équivalent
- Attestation de prise en charge des frais de formation

> Astuce : exécuter `python scripts/initialiser_documents_requis_sante_communautaire.py` pour créer ces documents dans la base.

#### Pour les autres formations
1. Dépôt du dossier avec documents recommandés
2. Vérification du dossier
3. Décision d'admission
4. **Envoi automatique d'email de confirmation** si admis
5. Inscription administrative

### 3. Ajout d'Étudiants en Cours de Formation

Un script permet d'ajouter manuellement des étudiants qui étaient déjà en formation avant la création du site :

```bash
python scripts/ajouter_etudiants_en_cours.py
```

Ce script permet de :
- Créer un utilisateur étudiant
- L'associer à la bonne classe selon la formation
- Définir l'année d'étude actuelle
- Pour DESMFMC : créer les `ResultatAnneeDES` pour les années précédentes validées

## Installation et Configuration

### 1. Migrations

Après avoir ajouté les nouveaux modèles, créer et appliquer les migrations :

```bash
python manage.py makemigrations admissions
python manage.py migrate
```

### 2. Initialiser les Documents Requis DESMFMC

Exécuter le script d'initialisation :

```bash
python scripts/initialiser_documents_requis_desmfmc.py
```

Ce script crée les 6 documents requis pour DESMFMC dans la base de données.

### 3. URLs

Les URLs sont déjà intégrées dans `core/urls.py` :

- `/admissions/mes-dossiers/` - Liste des dossiers du candidat
- `/admissions/creer-dossier/` - Créer un nouveau dossier
- `/admissions/dossier/<id>/` - Voir un dossier
- `/admissions/dossier/<id>/upload-document/` - Uploader un document
- `/admissions/dossier/<id>/inscription/` - Gérer l'inscription après admission

## Utilisation

### Pour les Candidats

1. **Créer un dossier** : Accéder à `/admissions/creer-dossier/`
2. **Sélectionner la formation** : Choisir DESMFMC ou une autre formation
3. **Uploader les documents** : Pour chaque document requis, uploader le fichier
4. **Vérifier le statut** : Consulter `/admissions/mes-dossiers/` pour voir l'état du dossier
5. **Après admission** : Accéder à l'inscription pour compléter les formalités

### Pour les Administrateurs

#### Gestion des Dossiers (Admin Django)

- Accéder à `/admin/admissions/` pour gérer :
  - Les dossiers de candidature
  - Les documents uploadés
  - Les décisions d'admission
  - Les inscriptions

#### Envoi des Emails de Confirmation

Pour envoyer les emails de confirmation aux candidats admis (formations autres que DESMFMC) :

```bash
python manage.py envoyer_confirmations_admission
```

Options :
- `--force` : Renvoyer les emails même s'ils ont déjà été envoyés
- `--dry-run` : Afficher ce qui serait envoyé sans réellement envoyer

Exemple :
```bash
python manage.py envoyer_confirmations_admission --dry-run
python manage.py envoyer_confirmations_admission
```

## Modèles de Données

### DocumentRequis
Définit les documents requis pour chaque type de formation.

### DocumentDossier
Document uploadé par un candidat pour son dossier. Peut être validé par un administrateur.

### DossierCandidature
Dossier de candidature avec :
- Référence unique
- Statut (soumis, incomplet, vérifié, rejeté)
- Informations spécifiques DESMFMC (prise en charge bourse)

### DecisionAdmission
Décision finale d'admission avec suivi de l'envoi d'email.

### Inscription
Inscription administrative avec validation et paiement (pour formations certifiantes).

## Scripts Utilitaires

### `scripts/ajouter_etudiants_en_cours.py`
Script interactif pour ajouter des étudiants en cours de formation.

### `scripts/initialiser_documents_requis_desmfmc.py`
Initialise les 6 documents requis pour DESMFMC.

### `scripts/maj_etudiants_desmfmc.py`
Script existant pour mettre à jour les étudiants DESMFMC (années 2-4).

## Notes Importantes

1. **Mots de passe temporaires** : Les étudiants créés via le script `ajouter_etudiants_en_cours.py` ont un mot de passe temporaire. Ils devront utiliser la fonction "Mot de passe oublié" pour définir leur mot de passe.

2. **Validation des documents** : Les documents uploadés doivent être validés manuellement par un administrateur dans l'interface d'administration Django.

3. **Emails de confirmation** : Les emails sont envoyés uniquement pour les formations autres que DESMFMC. Pour DESMFMC, le processus est géré différemment.

4. **Formats de fichiers acceptés** : PDF, DOC, DOCX, JPG, JPEG, PNG (max 10MB pour documents, 5MB pour preuves de paiement)

## Support

Pour toute question ou problème, contacter l'équipe de développement.

