# Système de Grilles d'Évaluation

Ce module permet de créer et gérer des grilles d'évaluation structurées pour différents types d'activités pédagogiques.

## Types de grilles disponibles

- **Évaluation Formative** : Évaluation continue pour suivre les progrès
- **Évaluation Sommative** : Évaluation à la fin d'une période d'apprentissage
- **Évaluation Finale** : Évaluation finale du programme
- **Supervision** : Grille pour les supervisions cliniques
- **Activité de Simulation** : Évaluation des simulations cliniques
- **Activité de Scénario** : Évaluation des activités basées sur des scénarios
- **Présentation** : Évaluation des présentations orales
- **Habiletés Cliniques** : Évaluation des compétences cliniques pratiques

## Structure des modèles

### GrilleEvaluation
Modèle principal représentant une grille d'évaluation complète.

### CritereEvaluation
Critères d'évaluation dans une grille. Chaque critère peut avoir :
- Un libellé et une description
- Un poids/pondération
- Une note maximale
- Une compétence ou jalon associé

### ElementEvaluation
Éléments de détail pour un critère (sous-critères).

### EvaluationAvecGrille
Instance d'évaluation utilisant une grille pour un étudiant spécifique.

### ReponseCritere / ReponseElement
Réponses/évaluations pour chaque critère et élément.

## Utilisation

### 1. Initialiser les types de grilles

```bash
python manage.py init_types_grilles
```

### 2. Créer une grille dans l'admin Django

1. Aller dans **Évaluations > Types de grilles d'évaluation**
2. Créer ou sélectionner un type de grille
3. Aller dans **Évaluations > Grilles d'évaluation**
4. Créer une nouvelle grille :
   - Sélectionner le type de grille
   - Ajouter un titre et une description
   - Associer un cours/classe si nécessaire
   - Ajouter les critères d'évaluation
   - Pour chaque critère, ajouter des éléments si nécessaire

### 3. Exporter une grille en CSV

Dans l'admin Django, sur la page de détail d'une grille, vous pouvez :
- Exporter la grille vide (structure) en CSV
- Exporter une évaluation complète avec les réponses en CSV

### 4. Utiliser les formulaires

Les formulaires sont disponibles via les vues :
- Liste des grilles : `/evaluations/grilles/`
- Détail d'une grille : `/evaluations/grilles/<id>/`
- Créer une évaluation : `/evaluations/grilles/<grille_id>/evaluer/`
- Export CSV grille : `/evaluations/grilles/<grille_id>/export/`
- Export CSV évaluation : `/evaluations/grilles/evaluation/<evaluation_id>/export/`

## Export CSV

### Export de la grille (structure)

Le CSV contient :
- Informations générales de la grille
- Liste des critères avec leurs éléments
- Pondérations et notes maximales

### Export d'une évaluation (avec réponses)

Le CSV contient :
- Informations de l'évaluation (étudiant, évaluateur, date)
- Note globale et pourcentage
- Commentaires généraux, points forts, axes d'amélioration
- Détail des réponses par critère et élément

## Exemple d'utilisation

1. **Créer une grille pour une présentation** :
   - Type : Présentation
   - Critères : Structure, Contenu, Communication, Support visuel
   - Pour chaque critère, ajouter des éléments détaillés

2. **Évaluer un étudiant** :
   - Sélectionner la grille
   - Choisir l'étudiant
   - Remplir les réponses pour chaque critère
   - Ajouter des commentaires

3. **Exporter les résultats** :
   - Exporter en CSV pour analyse ou archivage
   - Le CSV peut être ouvert dans Excel ou Google Sheets

## Intégration avec les compétences

Les grilles peuvent être liées aux :
- **Compétences** : Compétences générales du programme
- **Jalons** : Jalons de compétences spécifiques par classe

Cela permet de suivre l'acquisition des compétences à travers les différentes évaluations.

