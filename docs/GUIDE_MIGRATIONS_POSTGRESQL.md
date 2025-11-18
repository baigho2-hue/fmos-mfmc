# Guide de Création des Tables PostgreSQL

## Configuration actuelle

PostgreSQL est déjà configuré dans `backend/settings.py` avec :
- **Base de données** : `fmos-mfmc`
- **Utilisateur** : `postgres`
- **Hôte** : `localhost`
- **Port** : `5432`

## Étapes pour créer les tables PostgreSQL

### 1. Activer l'environnement virtuel

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les dépendances incluent :
- `Django>=4.2,<5.0`
- `psycopg2-binary>=2.9` (driver PostgreSQL)
- `python-dotenv>=1.0`

### 3. Créer la base de données PostgreSQL

Connectez-vous à PostgreSQL et créez la base de données :

```sql
-- Se connecter à PostgreSQL
psql -U postgres

-- Créer la base de données
CREATE DATABASE "fmos-mfmc" ENCODING 'UTF8';

-- Optionnel : Créer un utilisateur dédié
CREATE USER fmos_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE "fmos-mfmc" TO fmos_user;

-- Quitter
\q
```

### 4. Vérifier la configuration

Vérifiez que les variables d'environnement sont correctes dans votre fichier `.env` :

```env
DB_NAME=fmos-mfmc
DB_USER=postgres
DB_PASSWORD=Yiriba_19
DB_HOST=localhost
DB_PORT=5432
```

### 5. Créer les migrations

```bash
# Créer les migrations pour toutes les apps
python manage.py makemigrations

# Ou pour une app spécifique
python manage.py makemigrations utilisateurs
python manage.py makemigrations evaluations
python manage.py makemigrations admissions
python manage.py makemigrations communications
python manage.py makemigrations extras
python manage.py makemigrations procedurier
```

### 6. Appliquer les migrations (créer les tables)

```bash
# Appliquer toutes les migrations
python manage.py migrate

# Vérifier l'état des migrations
python manage.py showmigrations
```

### 7. Créer un superutilisateur (optionnel)

```bash
python manage.py createsuperuser
```

## Modèles à migrer

### Apps existantes avec migrations :
- ✅ `utilisateurs` - Modèles de base (Utilisateur, CodeVerification)
- ✅ `evaluations` - Modèles d'évaluation
- ✅ `admissions` - Modèles d'admission
- ✅ `communications` - Modèles de communication
- ✅ `extras` - Modèles extras
- ✅ `procedurier` - Modèles de procédurier

### Modèles à migrer (nouveaux) :

#### Dans `apps/utilisateurs` :
- `JalonProgramme` - Jalons du programme DESMFMC
- `ModuleProgramme` - Modules dans les jalons
- `CoursProgramme` - Liaison cours-modules
- `SuiviProgressionProgramme` - Suivi de progression

#### Dans `apps/utilisateurs/models_formation.py` :
- `Formation` - Formations
- `Classe` - Classes
- `Cours` - Cours
- `ProgressionEtudiant` - Progression des étudiants
- `Planification` - Planification
- `ObjectifApprentissage` - Objectifs
- `Competence` - Compétences
- `MethodePedagogique` - Méthodes pédagogiques
- `Accompagnement` - Accompagnement
- `SessionCoursEnLigne` - Sessions de cours en ligne
- `SessionEvaluationEnLigne` - Sessions d'évaluation en ligne

#### Dans `apps/evaluations/models_questionnaire.py` :
- `Question` - Questions d'évaluation
- `ReponsePossible` - Réponses possibles
- `ReponseEtudiant` - Réponses des étudiants
- `ParticipationSession` - Participations aux sessions

## Commandes utiles

### Voir les migrations en attente
```bash
python manage.py makemigrations --dry-run
```

### Voir l'état des migrations
```bash
python manage.py showmigrations
```

### Appliquer une migration spécifique
```bash
python manage.py migrate utilisateurs 0003
```

### Annuler une migration
```bash
python manage.py migrate utilisateurs 0002
```

### Voir le SQL qui sera exécuté
```bash
python manage.py sqlmigrate utilisateurs 0003
```

### Réinitialiser la base de données (ATTENTION : supprime toutes les données)
```bash
python manage.py flush
```

## Structure des tables créées

Après les migrations, vous aurez les tables suivantes dans PostgreSQL :

### Tables principales :
- `utilisateurs_utilisateur` - Utilisateurs
- `utilisateurs_codeverification` - Codes de vérification
- `utilisateurs_formation` - Formations
- `utilisateurs_classe` - Classes
- `utilisateurs_cours` - Cours
- `utilisateurs_jalonprogramme` - Jalons du programme
- `utilisateurs_moduleprogramme` - Modules
- `utilisateurs_coursprogramme` - Liaison cours-modules
- `utilisateurs_suiviprogressionprogramme` - Suivi de progression
- `evaluations_*` - Tables d'évaluation
- `admissions_*` - Tables d'admission
- etc.

## Vérification

Pour vérifier que les tables sont créées :

```bash
# Se connecter à PostgreSQL
psql -U postgres -d fmos-mfmc

# Lister les tables
\dt

# Voir la structure d'une table
\d utilisateurs_utilisateur

# Quitter
\q
```

## Problèmes courants

### Erreur : "could not connect to server"
- Vérifiez que PostgreSQL est démarré
- Vérifiez les paramètres de connexion dans `.env`

### Erreur : "database does not exist"
- Créez la base de données manuellement (voir étape 3)

### Erreur : "permission denied"
- Vérifiez les permissions de l'utilisateur PostgreSQL
- Utilisez un utilisateur avec les droits appropriés

### Erreur : "relation already exists"
- Les tables existent déjà
- Utilisez `python manage.py migrate --fake` si nécessaire

## Prochaines étapes

Après avoir créé les tables :
1. Initialiser le programme DESMFMC : `python manage.py init_programme_desmfmc_detaille`
2. Créer des utilisateurs de test
3. Créer des formations et classes
4. Tester l'application

