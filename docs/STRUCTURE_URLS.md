# Structure des URLs - FMOS MFMC

## Organisation des URLs par module

### URLs principales (core/urls.py)

#### Pages publiques
- `/` - Page d'accueil
- `/accueil/` - Accueil
- `/activites/` - Activités
- `/formations/` - Formations
- `/programme/` - Programmes
- `/cours/` - Cours
- `/enseignants/` - Enseignants
- `/etudiants/` - Étudiants
- `/contact/` - Contact
- `/inscription/` - Inscription

#### Authentification
- `/login/` - Connexion
- `/logout/` - Déconnexion
- `/login/med6/` - Connexion Med6

#### Espaces utilisateurs
- `/dashboard/etudiant/` - Tableau de bord étudiant
- `/dashboard/enseignant/` - Tableau de bord enseignant

#### Modules intégrés
- `/messagerie/` - Messagerie interne (apps.communications)
- `/admissions/` - Admissions (apps.admissions)
- `/evaluations/stage/` - Évaluations de stage (apps.evaluations.urls_stage)
- `/evaluations/grilles/` - Grilles d'évaluation (apps.evaluations.urls_grilles)

#### Administration
- `/administration/` - Dashboard administration
- `/admin/` - Admin Django

---

## Namespaces des URLs

### Communications
- Namespace: `communications`
- URLs: `/messagerie/`

### Admissions
- Namespace: `admissions`
- URLs: `/admissions/`

### Évaluations - Stage
- Namespace: `evaluations_stage`
- URLs: `/evaluations/stage/`

### Évaluations - Grilles
- Namespace: `grilles`
- URLs: `/evaluations/grilles/`

---

## Structure recommandée pour les nouvelles fonctionnalités

### Pattern d'URL
```
/module/sous-module/action/
```

### Exemples
- `/evaluations/grilles/` - Liste des grilles
- `/evaluations/grilles/creer/` - Créer une grille
- `/evaluations/grilles/<id>/modifier/` - Modifier une grille
- `/evaluations/grilles/<id>/` - Détail d'une grille

---

## Organisation des templates

### Structure
```
core/templates/
├── base.html (template de base)
├── includes/
│   ├── navigation_menu.html (menu de navigation)
│   └── boutons_pdf.html
├── administration/ (pages admin)
├── enseignant/ (pages enseignants)
├── etudiant/ (pages étudiants)
├── admissions/ (pages admissions)
└── ...
```

### Apps templates
```
apps/[app_name]/templates/[app_name]/
```

---

## Context Processors

### navigation_menu
- Fichier: `core/context_processors.py`
- Fournit: `navigation_menu`, `current_url`
- Utilisation: Menu de navigation dynamique selon le type d'utilisateur

---

## Bonnes pratiques

1. **Utiliser des namespaces** pour les apps
2. **Créer des includes** pour les composants réutilisables
3. **Utiliser le context processor** pour le menu
4. **Organiser les URLs par module** dans des fichiers séparés
5. **Utiliser des noms d'URL descriptifs** et cohérents

