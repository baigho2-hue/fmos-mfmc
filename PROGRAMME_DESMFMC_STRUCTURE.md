# Structure du Programme DESMFMC sur 4 ans

## Vue d'ensemble
Le programme DESMFMC est structuré en 4 années, chaque année étant divisée en jalons (semestres ou trimestres), contenant des modules, eux-mêmes composés de cours.

## Structure hiérarchique
```
Formation DESMFMC
├── Année 1
│   ├── Jalon 1.1 (Semestre 1)
│   │   ├── Module 1.1.1
│   │   │   ├── Cours 1
│   │   │   ├── Cours 2
│   │   │   └── ...
│   │   ├── Module 1.1.2
│   │   └── ...
│   └── Jalon 1.2 (Semestre 2)
│       └── ...
├── Année 2
│   └── ...
├── Année 3
│   └── ...
└── Année 4
    └── ...
```

## Modèles créés

### 1. JalonProgramme
- Représente un jalon temporel (semestre, trimestre) dans une année
- Contient : nom, code, année, semestre, dates, volume horaire

### 2. ModuleProgramme
- Représente un module de cours dans un jalon
- Contient : objectifs, compétences, prérequis, volume horaire

### 3. CoursProgramme
- Lie un cours existant à un module
- Permet de définir l'ordre et si le cours est obligatoire

### 4. SuiviProgressionProgramme
- Suit la progression d'un étudiant dans chaque jalon
- Contient : statut, pourcentage, notes, commentaires

## Utilisation

### Pour créer le programme dans l'admin Django :
1. Créer la Formation DESMFMC (si pas déjà fait)
2. Créer les Jalons pour chaque année/semestre
3. Créer les Modules dans chaque jalon
4. Créer les Cours (dans les Classes appropriées)
5. Lier les Cours aux Modules via CoursProgramme

### Pour les étudiants :
- Accès au programme complet via `/programme/desmfmc/complet/`
- Voir leur progression via `/etudiant/progression-programme/`
- Détail d'un jalon via `/programme/jalon/<id>/`

## Prochaines étapes
1. Créer les données de base du programme (jalons, modules, cours)
2. Créer les templates pour l'affichage
3. Implémenter le suivi automatique de progression

