# Guide de Vérification des Utilisateurs

## ✅ Résultat de la vérification

**Total : 10 utilisateurs créés avec succès !**

### Superutilisateur
- **admin** (admin@fmos-mfmc.ml) - Étudiant (mais superuser)

### Étudiants (5)
1. **etudiant1** (etudiant1@fmos-mfmc.ml) - DESMFMC 1ère année
2. **etudiant2** (etudiant2@fmos-mfmc.ml) - DESMFMC 1ère année
3. **etudiant3** (etudiant3@fmos-mfmc.ml) - DESMFMC 2ème année
4. **etudiant4** (etudiant4@fmos-mfmc.ml) - DESMFMC 2ème année
5. **etudiant5** (etudiant5@fmos-mfmc.ml) - DESMFMC 3ème année

### Enseignants (4)
1. **enseignant1** (enseignant1@fmos-mfmc.ml) - Accès complet
2. **enseignant2** (enseignant2@fmos-mfmc.ml) - Accès complet
3. **enseignant3** (enseignant3@fmos-mfmc.ml) - Accès standard
4. **enseignant4** (enseignant4@fmos-mfmc.ml) - Accès complet

---

## 🔍 Méthodes de Vérification

### 1. Via la ligne de commande

#### Lister tous les utilisateurs
```bash
python manage.py liste_utilisateurs
```

#### Rechercher un utilisateur par email
```bash
python manage.py liste_utilisateurs --email etudiant1@fmos-mfmc.ml
```

#### Vérifier les doublons d'email
```bash
python manage.py nettoyer_doublons_email --dry-run
```

---

### 2. Via l'interface d'administration Django

1. **Démarrer le serveur Django** :
   ```bash
   python manage.py runserver
   ```

2. **Accéder à l'admin** :
   - URL : http://127.0.0.1:8000/admin/
   - Username : `admin`
   - Password : `admin123`

3. **Dans l'admin, vous pouvez** :
   - Voir tous les utilisateurs dans la section "Utilisateurs"
   - Modifier les informations des utilisateurs
   - Voir les codes de vérification
   - Gérer les formations, classes, cours, etc.

---

### 3. Via le shell Django

```bash
python manage.py shell
```

Puis dans le shell Python :
```python
from apps.utilisateurs.models import Utilisateur

# Lister tous les utilisateurs
users = Utilisateur.objects.all()
for user in users:
    print(f"{user.username} - {user.email} - {user.get_type_utilisateur_display()}")

# Compter les utilisateurs par type
print(f"Total: {Utilisateur.objects.count()}")
print(f"Étudiants: {Utilisateur.objects.filter(type_utilisateur='etudiant').count()}")
print(f"Enseignants: {Utilisateur.objects.filter(type_utilisateur='enseignant').count()}")

# Rechercher un utilisateur spécifique
user = Utilisateur.objects.get(username='etudiant1')
print(f"Classe: {user.classe}")
print(f"Email vérifié: {user.email_verifie}")
```

---

### 4. Tester la connexion

1. **Démarrer le serveur** :
   ```bash
   python manage.py runserver
   ```

2. **Accéder à la page de connexion** :
   - URL : http://127.0.0.1:8000/login/

3. **Tester avec un étudiant** :
   - Username : `etudiant1`
   - Password : `etudiant123`
   - Vous serez redirigé vers le dashboard étudiant

4. **Tester avec un enseignant** :
   - Username : `enseignant1`
   - Password : `enseignant123`
   - Vous serez redirigé vers le dashboard enseignant

5. **Tester avec le superutilisateur** :
   - Username : `admin`
   - Password : `admin123`
   - Accès complet à l'admin et aux dashboards

---

## 📋 Identifiants de Test

### Étudiants
| Username | Password | Classe |
|----------|----------|--------|
| etudiant1 | etudiant123 | DESMFMC 1ère année |
| etudiant2 | etudiant123 | DESMFMC 1ère année |
| etudiant3 | etudiant123 | DESMFMC 2ème année |
| etudiant4 | etudiant123 | DESMFMC 2ème année |
| etudiant5 | etudiant123 | DESMFMC 3ème année |

### Enseignants
| Username | Password | Accès |
|----------|----------|-------|
| enseignant1 | enseignant123 | Complet |
| enseignant2 | enseignant123 | Complet |
| enseignant3 | enseignant123 | Standard |
| enseignant4 | enseignant123 | Complet |

### Superutilisateur
| Username | Password |
|----------|----------|
| admin | admin123 |

---

## ⚠️ Notes Importantes

1. **Tous les emails sont vérifiés** pour faciliter les tests (pas besoin de vérification par email)
2. **Tous les comptes sont actifs** et prêts à être utilisés
3. **Le superutilisateur** a accès à tout (admin Django + dashboards)
4. **Les enseignants avec accès complet** peuvent voir et modifier tous les contenus
5. **Les étudiants** ont accès uniquement à leurs cours et leur progression

---

## 🔧 Commandes Utiles

### Créer un nouvel utilisateur de test
```bash
python manage.py creer_utilisateurs_test
```

### Créer un superutilisateur
```bash
python manage.py creer_superuser --username nom --email email@example.com --password motdepasse
```

### Réinitialiser tous les utilisateurs
```bash
python manage.py reinitialiser_utilisateurs
```

### Vérifier un utilisateur spécifique
```bash
python manage.py liste_utilisateurs --email email@example.com
```

