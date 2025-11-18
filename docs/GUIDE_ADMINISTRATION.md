# Guide - Menu Administration

## 📋 Vue d'ensemble

Le menu **Administration** est accessible uniquement aux membres de la coordination DESMFMC. Il permet de gérer :
- 📅 L'agenda de toutes les activités
- 📝 Les notes et progressions des classes
- ⚠️ Les alertes pour les activités à venir
- 📊 Les résultats des évaluations
- ✏️ La gestion des inscriptions aux formations

## 🔐 Accès

### Attribuer le statut de membre de la coordination

Pour donner accès au menu Administration à un utilisateur :

1. **Via l'admin Django** :
   - Aller sur : http://127.0.0.1:8000/admin/
   - Se connecter avec un compte superutilisateur
   - Aller dans "Utilisateurs" > Sélectionner l'utilisateur
   - Cocher la case **"Membre de la coordination DESMFMC"**
   - Enregistrer

2. **Via la ligne de commande** :
   ```bash
   python manage.py shell
   ```
   ```python
   from apps.utilisateurs.models import Utilisateur
   user = Utilisateur.objects.get(username='nom_utilisateur')
   user.membre_coordination = True
   user.save()
   ```

### Note importante
- Les **superutilisateurs** ont automatiquement accès au menu Administration
- Le champ `membre_coordination` peut être activé pour n'importe quel type d'utilisateur (étudiant, enseignant, etc.)

## 📑 Fonctionnalités du menu Administration

### 1. Tableau de bord (`/administration/`)
- Vue d'ensemble des statistiques :
  - Nombre d'étudiants actifs
  - Nombre d'enseignants actifs
  - Nombre de formations actives
  - Nombre de classes actives
- Alertes pour les activités à venir (7 prochains jours)
- Liens rapides vers toutes les sections

### 2. Agenda (`/administration/agenda/`)
- Vue complète de toutes les activités planifiées (60 prochains jours)
- Alertes pour les activités dans les 3 prochains jours
- Activités groupées par date
- Informations détaillées : classe, cours, description

### 3. Notes des classes (`/administration/notes/`)
- Liste de toutes les classes actives
- Statistiques par classe :
  - Nombre d'étudiants
  - Nombre de cours
  - Progression moyenne
- Accès au détail des notes pour chaque classe

### 4. Détail des notes d'une classe (`/administration/notes/classe/<id>/`)
- Tableau récapitulatif des notes de tous les étudiants
- Progression par cours pour chaque étudiant
- Moyenne générale par étudiant
- Statut de progression (non commencé, en cours, terminé, validé)

### 5. Alertes Agenda (`/administration/alertes/`)
- **Activités à venir** : dans les 3 prochains jours (urgent)
- **Activités récentes** : dans les 7 derniers jours (suivi)
- Permet de suivre les activités importantes

### 6. Résultats des évaluations (`/administration/resultats/`)
- **Évaluations des cours** :
  - Nombre de participants
  - Moyenne, note maximale, note minimale
- **Évaluations des enseignants** :
  - Qualité pédagogique
  - Disponibilité
  - Clarté des explications
  - Gestion de classe

### 7. Gestion des inscriptions (`/administration/inscriptions/`)
- Liste de toutes les formations actives
- Statistiques par formation :
  - Nombre de classes
  - Nombre d'étudiants inscrits
- Accès au détail des inscriptions pour chaque formation

### 8. Détail des inscriptions d'une formation (`/administration/inscriptions/formation/<id>/`)
- Liste des étudiants par classe
- Informations détaillées :
  - Nom, prénom
  - Email, téléphone
  - Date d'inscription

## 🎯 Utilisation

### Pour accéder au menu Administration

1. Se connecter avec un compte ayant le statut de membre de la coordination
2. Le menu **"Administration"** apparaît dans le menu principal
3. Cliquer sur "Administration" pour voir le sous-menu avec toutes les options

### Menu Administration disponible :
- Tableau de bord
- Agenda
- Notes des classes
- Alertes
- Résultats évaluations
- Gestion inscriptions

## 🔧 Configuration

### Créer un membre de la coordination

```bash
python manage.py shell
```

```python
from apps.utilisateurs.models import Utilisateur

# Créer ou modifier un utilisateur
user = Utilisateur.objects.get(username='coordinateur')
user.membre_coordination = True
user.save()

# Vérifier
print(user.est_membre_coordination())  # True
```

### Vérifier les membres de la coordination

```python
from apps.utilisateurs.models import Utilisateur

coordinateurs = Utilisateur.objects.filter(membre_coordination=True)
for coord in coordinateurs:
    print(f"{coord.username} - {coord.email}")
```

## 📝 Notes importantes

1. **Sécurité** : Seuls les membres de la coordination et les superutilisateurs peuvent accéder à ces pages
2. **Permissions** : Le décorateur `@coordination_required` protège toutes les vues d'administration
3. **Données sensibles** : Les pages d'administration affichent des données sensibles (notes, résultats, etc.)
4. **Accès complet** : Les membres de la coordination ont accès à toutes les données, toutes formations confondues

## 🚀 Prochaines étapes

Pour améliorer le système d'administration, vous pouvez :
- Ajouter des fonctionnalités d'export (PDF, Excel)
- Créer des graphiques de progression
- Ajouter des filtres et recherches avancées
- Implémenter des notifications automatiques pour les alertes
- Créer des rapports périodiques

