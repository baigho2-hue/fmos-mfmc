# Guide de Création du Programme DESMFMC

## Vue d'ensemble

Ce guide explique comment créer et structurer le programme DESMFMC sur 4 ans dans le système.

## Structure du Programme

Le programme est organisé en 4 niveaux :
1. **Formation** : DESMFMC (une seule)
2. **Jalons** : Semestres ou trimestres dans chaque année (ex: Année 1 - Semestre 1)
3. **Modules** : Groupes de cours thématiques dans un jalon
4. **Cours** : Cours individuels liés à un module

## Étapes de Création

### 1. Créer la Formation DESMFMC

Dans l'admin Django :
- Aller dans **Formations**
- Créer une nouvelle formation :
  - **Nom** : "Diplôme d'Études Spécialisées en Médecine de Famille et Médecine Communautaire"
  - **Code** : "DESMFMC"
  - **Type** : Formation initiale
  - **Nature** : Certifiante
  - **Durée en années** : 4
  - **Durée totale en heures** : (à calculer selon le programme)
  - Remplir les objectifs généraux, compétences visées, etc.

### 2. Créer les Classes

Pour chaque promotion/année d'entrée :
- Créer une classe liée à la formation DESMFMC
- Exemple : "DESMFMC Promotion 2025 - Année 1"

### 3. Créer les Jalons

Pour chaque année et semestre :
- **Année 1 - Semestre 1** : Code "DESMFMC-A1-S1"
- **Année 1 - Semestre 2** : Code "DESMFMC-A1-S2"
- **Année 2 - Semestre 1** : Code "DESMFMC-A2-S1"
- ... et ainsi de suite

Chaque jalon doit avoir :
- Dates de début et fin
- Volume horaire total
- Description

### 4. Créer les Modules

Dans chaque jalon, créer des modules thématiques :
- Exemple pour Année 1 - Semestre 1 :
  - Module "Médecine générale de base"
  - Module "Anatomie et physiologie appliquées"
  - Module "Communication et relation patient"
  - etc.

Chaque module doit avoir :
- Objectifs d'apprentissage (liés aux ObjectifApprentissage)
- Compétences visées (liés aux Competence)
- Prérequis (autres modules si nécessaire)
- Volume horaire

### 5. Créer les Cours

Dans chaque classe, créer les cours :
- Lier chaque cours à la classe appropriée
- Définir les objectifs, compétences, méthodes pédagogiques
- Assigner un enseignant

### 6. Lier les Cours aux Modules

Via **CoursProgramme** :
- Pour chaque module, lier les cours correspondants
- Définir l'ordre des cours dans le module
- Indiquer si le cours est obligatoire ou optionnel

## Exemple de Structure Complète

### Année 1 - Semestre 1

**Jalon** : "Fondamentaux de la médecine de famille"
- **Module 1** : "Médecine générale de base" (120h)
  - Cours : Introduction à la médecine de famille
  - Cours : Histoire clinique et examen physique
  - Cours : Décision clinique en médecine de famille
- **Module 2** : "Communication médicale" (80h)
  - Cours : Communication patient-médecin
  - Cours : Entretien motivationnel
- **Module 3** : "Systèmes de santé" (60h)
  - Cours : Organisation des soins primaires
  - Cours : Santé publique et épidémiologie

### Année 1 - Semestre 2

**Jalon** : "Pathologies courantes en médecine de famille"
- **Module 1** : "Pathologies infectieuses" (100h)
- **Module 2** : "Pathologies cardiovasculaires" (100h)
- **Module 3** : "Pathologies respiratoires" (80h)

... et ainsi de suite pour les 4 années.

## Suivi de Progression

Le système suit automatiquement :
- La progression de chaque étudiant dans chaque jalon
- Le pourcentage de complétion
- Les notes et commentaires
- Les dates de début/fin

## Accès

- **Programme complet** : `/programme/desmfmc/complet/`
- **Détail d'un jalon** : `/programme/jalon/<id>/`
- **Progression étudiante** : `/etudiant/progression-programme/`

## Notes Importantes

1. Les jalons doivent être créés dans l'ordre chronologique
2. Les modules peuvent avoir des prérequis (autres modules)
3. Les cours peuvent être liés à plusieurs modules si nécessaire
4. La progression est calculée automatiquement à partir des ProgressionEtudiant liées aux cours

