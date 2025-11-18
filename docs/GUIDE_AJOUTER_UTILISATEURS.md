# Guide : Ajouter des utilisateurs dans Django

## Méthode 1 : Interface d'administration Django (Recommandée)

### Accéder à l'admin Django

1. **Connectez-vous à l'admin** :
   - URL : `https://fmos-mfmc.onrender.com/admin/`
   - Utilisez vos identifiants superutilisateur

2. **Ajouter un utilisateur** :
   - Cliquez sur **"Utilisateurs"** dans la section "UTILISATEURS"
   - Cliquez sur **"Ajouter Utilisateur"** en haut à droite
   - Remplissez les champs obligatoires :
     - **Username** : nom d'utilisateur unique
     - **Email** : adresse email (doit être unique)
     - **Password** : mot de passe (ou générer automatiquement)
   - Cliquez sur **"Enregistrer"**

3. **Compléter le profil** :
   - Après avoir créé l'utilisateur, vous serez redirigé vers la page de modification
   - Remplissez les informations supplémentaires :
     - **Prénom** et **Nom**
     - **Type d'utilisateur** : Étudiant ou Enseignant
     - **Classe** : si c'est un étudiant (ex: "Médecine 6", "DESMFMC 1ère année")
     - **Matières enseignées** : si c'est un enseignant
     - **Niveau d'accès** : Standard, Limité ou Complet (pour les enseignants)
     - **Téléphone**, **Adresse**, **Date de naissance** (optionnels)
   - Cliquez sur **"Enregistrer"**

## Méthode 2 : Script de commande Django

### Créer un script de commande personnalisé

Créez un fichier `apps/utilisateurs/management/commands/creer_utilisateur.py` :

```python
from django.core.management.base import BaseCommand
from apps.utilisateurs.models import Utilisateur

class Command(BaseCommand):
    help = 'Crée un nouvel utilisateur'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nom d\'utilisateur')
        parser.add_argument('email', type=str, help='Email')
        parser.add_argument('password', type=str, help='Mot de passe')
        parser.add_argument('--type', type=str, choices=['etudiant', 'enseignant'], 
                          default='etudiant', help='Type d\'utilisateur')
        parser.add_argument('--classe', type=str, help='Classe (pour étudiants)')
        parser.add_argument('--prenom', type=str, help='Prénom')
        parser.add_argument('--nom', type=str, help='Nom')
        parser.add_argument('--superuser', action='store_true', help='Créer un superutilisateur')

    def handle(self, *args, **options):
        user = Utilisateur.objects.create_user(
            username=options['username'],
            email=options['email'],
            password=options['password'],
            type_utilisateur=options['type'],
            classe=options.get('classe'),
            first_name=options.get('prenom', ''),
            last_name=options.get('nom', ''),
            is_superuser=options.get('superuser', False),
            is_staff=options.get('superuser', False)
        )
        self.stdout.write(self.style.SUCCESS(f'Utilisateur "{user.username}" créé avec succès !'))
```

### Utilisation

```bash
# Créer un étudiant
python manage.py creer_utilisateur etudiant1 etudiant1@example.com motdepasse123 --type etudiant --classe "Médecine 6" --prenom "Jean" --nom "Dupont"

# Créer un enseignant
python manage.py creer_utilisateur prof1 prof1@example.com motdepasse123 --type enseignant --prenom "Marie" --nom "Martin"

# Créer un superutilisateur
python manage.py creer_utilisateur admin2 admin2@example.com motdepasse123 --superuser
```

## Méthode 3 : Shell Django interactif

### Ouvrir le shell Django

```bash
python manage.py shell
```

### Créer un utilisateur dans le shell

```python
from apps.utilisateurs.models import Utilisateur

# Créer un étudiant
etudiant = Utilisateur.objects.create_user(
    username='etudiant1',
    email='etudiant1@example.com',
    password='motdepasse123',
    type_utilisateur='etudiant',
    classe='Médecine 6',
    first_name='Jean',
    last_name='Dupont'
)

# Créer un enseignant
enseignant = Utilisateur.objects.create_user(
    username='prof1',
    email='prof1@example.com',
    password='motdepasse123',
    type_utilisateur='enseignant',
    niveau_acces='complet',
    first_name='Marie',
    last_name='Martin',
    matieres='Médecine générale, Pédiatrie'
)

# Créer un superutilisateur
admin = Utilisateur.objects.create_superuser(
    username='admin2',
    email='admin2@example.com',
    password='motdepasse123'
)
```

## Méthode 4 : Formulaire d'inscription publique

Si vous avez un formulaire d'inscription sur votre site, les utilisateurs peuvent s'inscrire eux-mêmes via :
- URL : `https://fmos-mfmc.onrender.com/inscription/`

## Vérifier les utilisateurs créés

```bash
python manage.py shell
```

```python
from apps.utilisateurs.models import Utilisateur

# Lister tous les utilisateurs
Utilisateur.objects.all()

# Compter les utilisateurs
Utilisateur.objects.count()

# Filtrer par type
Utilisateur.objects.filter(type_utilisateur='etudiant')
Utilisateur.objects.filter(type_utilisateur='enseignant')
```

## Conseils

1. **Mots de passe sécurisés** : Utilisez des mots de passe forts
2. **Emails uniques** : Chaque utilisateur doit avoir un email unique
3. **Usernames uniques** : Les noms d'utilisateurs doivent être uniques
4. **Vérification email** : Activez la vérification d'email si nécessaire
5. **Permissions** : Configurez correctement les niveaux d'accès selon le type d'utilisateur

