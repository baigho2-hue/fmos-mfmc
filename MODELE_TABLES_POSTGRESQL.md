# Liste des Tables PostgreSQL à Créer

## Vue d'ensemble

Ce document liste toutes les tables qui seront créées dans PostgreSQL lors de l'exécution des migrations Django.

## Tables par Application

### 1. Application `utilisateurs`

#### Tables de base :
- `utilisateurs_utilisateur` - Utilisateurs (étudiants, enseignants, admins)
- `utilisateurs_codeverification` - Codes de vérification pour l'authentification

#### Tables de formation :
- `utilisateurs_formation` - Formations (DESMFMC, etc.)
- `utilisateurs_classe` - Classes (promotions)
- `utilisateurs_cours` - Cours individuels
- `utilisateurs_progressionetudiant` - Progression des étudiants dans les cours
- `utilisateurs_planification` - Planification des activités
- `utilisateurs_objectifapprentissage` - Objectifs d'apprentissage
- `utilisateurs_competence` - Compétences visées
- `utilisateurs_methodepedagogique` - Méthodes pédagogiques
- `utilisateurs_accompagnement` - Accompagnement des étudiants
- `utilisateurs_sessioncoursenligne` - Sessions de cours en ligne
- `utilisateurs_sessionevaluationenligne` - Sessions d'évaluation en ligne

#### Tables du programme DESMFMC :
- `utilisateurs_jalonprogramme` - Jalons du programme (semestres)
- `utilisateurs_moduleprogramme` - Modules dans les jalons
- `utilisateurs_coursprogramme` - Liaison cours-modules
- `utilisateurs_suiviprogressionprogramme` - Suivi de progression par jalon

#### Tables de liaison (ManyToMany) :
- `utilisateurs_moduleprogramme_objectifs_module` - Objectifs des modules
- `utilisateurs_moduleprogramme_competences_module` - Compétences des modules
- `utilisateurs_moduleprogramme_prerequis_modules` - Prérequis des modules
- `utilisateurs_cours_objectifs` - Objectifs des cours
- `utilisateurs_cours_competences` - Compétences des cours
- `utilisateurs_cours_methodes_pedagogiques` - Méthodes pédagogiques des cours
- `utilisateurs_sessioncoursenligne_participants_autorises` - Participants autorisés aux sessions
- `utilisateurs_sessionevaluationenligne_etudiants_connectes` - Étudiants connectés aux évaluations
- `utilisateurs_sessionevaluationenligne_participants_autorises` - Participants autorisés aux évaluations

### 2. Application `evaluations`

#### Tables d'évaluation :
- `evaluations_typeevaluation` - Types d'évaluation
- `evaluations_evaluation` - Évaluations
- `evaluations_resultatevaluation` - Résultats d'évaluation
- `evaluations_evaluationformation` - Évaluations de formation
- `evaluations_evaluationenseignant` - Évaluations des enseignants
- `evaluations_accompagnement` - Accompagnement
- `evaluations_suiviindividuel` - Suivi individuel
- `evaluations_stage` - Stages
- `evaluations_evaluationtheorique` - Évaluations théoriques
- `evaluations_evaluationpratique` - Évaluations pratiques
- `evaluations_memoire` - Mémoires

#### Tables de questionnaire :
- `evaluations_question` - Questions d'évaluation en ligne
- `evaluations_reponsepossible` - Réponses possibles aux questions
- `evaluations_reponseetudiant` - Réponses des étudiants
- `evaluations_participationsession` - Participations aux sessions d'évaluation

#### Tables de liaison :
- `evaluations_reponseetudiant_reponses_choisies` - Réponses choisies par les étudiants

### 3. Application `admissions`

- `admissions_*` - Tables liées aux admissions

### 4. Application `communications`

- `communications_*` - Tables liées aux communications

### 5. Application `extras`

- `extras_*` - Tables extras

### 6. Application `procedurier`

- `procedurier_*` - Tables du procédurier

### 7. Tables Django de base

- `django_migrations` - Historique des migrations
- `django_content_type` - Types de contenu
- `django_session` - Sessions utilisateur
- `auth_group` - Groupes d'utilisateurs
- `auth_permission` - Permissions
- `auth_group_permissions` - Permissions des groupes
- `admin_logentry` - Logs de l'admin Django

## Commandes pour créer les tables

### Option 1 : Utiliser le script automatique

**Windows :**
```bash
creer_tables_postgresql.bat
```

**Linux/Mac :**
```bash
chmod +x creer_tables_postgresql.sh
./creer_tables_postgresql.sh
```

### Option 2 : Commandes manuelles

```bash
# 1. Activer l'environnement virtuel
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer les migrations
python manage.py makemigrations

# 4. Appliquer les migrations (créer les tables)
python manage.py migrate

# 5. Vérifier l'état
python manage.py showmigrations
```

## Vérification dans PostgreSQL

```sql
-- Se connecter à PostgreSQL
psql -U postgres -d fmos-mfmc

-- Lister toutes les tables
\dt

-- Compter les tables
SELECT COUNT(*) FROM information_schema.tables 
WHERE table_schema = 'public';

-- Voir la structure d'une table
\d utilisateurs_utilisateur

-- Voir toutes les tables d'une app
\dt utilisateurs_*

-- Quitter
\q
```

## Statistiques attendues

Après toutes les migrations, vous devriez avoir environ :
- **~50-60 tables** au total
- **~15-20 tables** pour `utilisateurs`
- **~10-15 tables** pour `evaluations`
- **~5-10 tables** pour chaque autre app
- **~10-15 tables** Django de base

## Notes importantes

1. **Ordre des migrations** : Django gère automatiquement l'ordre des migrations selon les dépendances entre modèles.

2. **Clés étrangères** : Toutes les relations ForeignKey créent automatiquement des index et des contraintes de clé étrangère.

3. **ManyToMany** : Les relations ManyToMany créent automatiquement des tables de liaison.

4. **Index** : Django crée automatiquement des index pour :
   - Les clés primaires
   - Les clés étrangères
   - Les champs avec `db_index=True`
   - Les champs `unique=True`

5. **Contraintes** : Les contraintes `unique_together` et `unique=True` sont automatiquement créées.

## Problèmes courants

### Erreur : "relation already exists"
- Les tables existent déjà
- Utilisez `python manage.py migrate --fake` si vous voulez marquer les migrations comme appliquées sans les exécuter

### Erreur : "django.db.utils.OperationalError"
- Vérifiez que PostgreSQL est démarré
- Vérifiez les paramètres de connexion dans `.env`
- Vérifiez que la base de données existe

### Erreur : "no such table"
- Les migrations n'ont pas été appliquées
- Exécutez `python manage.py migrate`

