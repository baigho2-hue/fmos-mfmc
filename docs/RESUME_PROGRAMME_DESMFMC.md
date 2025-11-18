# Résumé - Programme DESMFMC Structuré sur 4 ans

## ✅ Système Créé

### 1. Modèles de Données (`apps/utilisateurs/models_programme_desmfmc.py`)

#### JalonProgramme
- Représente un jalon temporel (semestre/trimestre) dans une année
- Champs : nom, code, année (1-4), semestre (1-2), dates, volume horaire total
- Permet de structurer le programme par périodes

#### ModuleProgramme
- Représente un module thématique dans un jalon
- Champs : nom, code, description, volume horaire, ordre
- Lié aux objectifs d'apprentissage et compétences
- Peut avoir des prérequis (autres modules)

#### CoursProgramme
- Lie un cours existant à un module
- Permet de définir l'ordre et si le cours est obligatoire
- Structure : Module → Cours (avec ordre)

#### SuiviProgressionProgramme
- Suit la progression d'un étudiant dans chaque jalon
- Champs : statut, pourcentage de complétion, note finale, commentaires
- Dates de début/fin et dernière activité

### 2. Vues (`core/views_programme_desmfmc.py`)

#### programme_desmfmc_complet
- Affiche le programme complet sur 4 ans
- Organisé par année et jalons
- Affiche la progression de l'étudiant si connecté
- Statistiques globales du programme

#### detail_jalon
- Détail d'un jalon avec tous ses modules
- Affiche les cours de chaque module
- Progression de l'étudiant dans le jalon

#### ma_progression_programme
- Vue dédiée pour l'étudiant
- Progression globale avec graphique circulaire
- Progression par année avec statistiques
- Détail de chaque jalon avec statut

### 3. Templates

#### programme_desmfmc_complet.html
- Vue d'ensemble du programme sur 4 ans
- Affichage par année avec jalons
- Barres de progression par année
- Cartes pour chaque jalon avec statistiques

#### detail_jalon.html
- Détail complet d'un jalon
- Liste des modules avec objectifs et compétences
- Liste des cours par module
- Progression de l'étudiant

#### ma_progression_programme.html
- Vue de progression détaillée pour l'étudiant
- Graphique circulaire de progression globale
- Progression par année avec statistiques
- Détail de chaque jalon avec notes et commentaires

### 4. Script d'Initialisation

#### init_programme_desmfmc.py
- Commande Django : `python manage.py init_programme_desmfmc`
- Crée automatiquement :
  - La formation DESMFMC
  - 8 jalons (4 années × 2 semestres)
  - Modules de base pour chaque jalon
- Structure de base prête à être complétée

### 5. Interface Admin

Tous les modèles sont enregistrés dans l'admin Django avec :
- Filtres par formation, année, semestre
- Recherche par nom, code
- Gestion des relations ManyToMany
- Affichages personnalisés

## 📋 Structure du Programme

### Année 1
- **Semestre 1** : Fondamentaux de la médecine de famille
  - Médecine générale de base (120h)
  - Communication médicale (80h)
  - Systèmes de santé et santé publique (60h)
- **Semestre 2** : Pathologies courantes
  - Pathologies infectieuses (100h)
  - Pathologies cardiovasculaires (100h)
  - Pathologies respiratoires (80h)

### Année 2
- **Semestre 1** : Médecine spécialisée appliquée
  - Pédiatrie en médecine de famille (120h)
  - Gynécologie et obstétrique (100h)
- **Semestre 2** : Médecine d'urgence et soins critiques
  - Urgences médicales (120h)
  - Réanimation et soins critiques (80h)

### Année 3
- **Semestre 1** : Médecine communautaire et santé publique
  - Santé communautaire (120h)
  - Épidémiologie et recherche (100h)
- **Semestre 2** : Gestion et leadership
  - Gestion des structures de santé (100h)
  - Leadership et management d'équipe (80h)

### Année 4
- **Semestre 1** : Stage clinique avancé
  - Stage en médecine de famille (200h)
  - Mémoire de fin d'études (100h)
- **Semestre 2** : Préparation à la pratique professionnelle
  - Éthique et déontologie (60h)
  - Insertion professionnelle (80h)

**Total : ~1600 heures sur 4 ans**

## 🚀 Utilisation

### Pour initialiser le programme :
```bash
python manage.py makemigrations utilisateurs
python manage.py migrate
python manage.py init_programme_desmfmc
```

### Pour compléter le programme :
1. Aller dans l'admin Django
2. Créer les cours dans les classes appropriées
3. Lier les cours aux modules via CoursProgramme
4. Ajouter les objectifs d'apprentissage et compétences
5. Assigner les enseignants

### Pour les étudiants :
- Accéder au programme : `/programme/desmfmc/complet/`
- Voir leur progression : `/etudiant/progression-programme/`
- Détail d'un jalon : `/programme/jalon/<id>/`

## 📊 Fonctionnalités Pédagogiques

✅ **Structure jalonnée** : Programme organisé par années et semestres
✅ **Modules thématiques** : Groupement logique des cours
✅ **Objectifs d'apprentissage** : Liés aux modules (taxonomie de Bloom)
✅ **Compétences visées** : Par domaine (Savoir, Savoir-faire, Savoir-être)
✅ **Prérequis** : Modules peuvent avoir des prérequis
✅ **Suivi de progression** : Automatique par jalon
✅ **Statistiques** : Progression globale et par année
✅ **Notes et commentaires** : Suivi détaillé par enseignant

## 📝 Prochaines Étapes

1. **Créer les migrations** :
   ```bash
   python manage.py makemigrations utilisateurs
   python manage.py migrate
   ```

2. **Initialiser la structure de base** :
   ```bash
   python manage.py init_programme_desmfmc
   ```

3. **Compléter avec le document fourni** :
   - Ajouter tous les modules détaillés
   - Créer tous les cours
   - Lier les cours aux modules
   - Ajouter les objectifs et compétences spécifiques

4. **Tester le système** :
   - Créer un étudiant test
   - Vérifier l'affichage du programme
   - Tester le suivi de progression

Le système est maintenant prêt à recevoir le contenu détaillé du programme DESMFMC !

