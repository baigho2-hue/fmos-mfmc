# Scripts d'administration

Ce dossier contient les scripts d'administration pour le projet FMOS MFMC.

## ⚠️ Important : Comment exécuter les scripts

**TOUJOURS exécuter les scripts depuis la racine du projet**, pas depuis le dossier `scripts/`.

### ✅ Méthode correcte :

```bash
# Depuis la racine du projet (C:\Users\HP\Documents\fmos-mfmc)
python scripts/nom_du_script.py
```

### ❌ Méthode incorrecte :

```bash
# NE PAS faire ça :
cd scripts
python nom_du_script.py
```

## Scripts disponibles

### 1. `ajouter_etudiants_en_cours.py`

Script interactif pour ajouter manuellement des étudiants en cours de formation avant la création du site.

**Usage :**
```bash
python scripts/ajouter_etudiants_en_cours.py
```

**Fonctionnalités :**
- Créer un utilisateur étudiant
- L'associer à la bonne classe selon la formation
- Définir l'année d'étude actuelle
- Pour DESMFMC : créer les `ResultatAnneeDES` pour les années précédentes validées

### 2. `initialiser_documents_requis_desmfmc.py`

Initialise les 6 documents requis pour le dossier DESMFMC dans la base de données.

**Usage :**
```bash
python scripts/initialiser_documents_requis_desmfmc.py
```

**Fonctionnalités :**
- Crée les 6 documents requis pour DESMFMC
- Met à jour les documents existants si nécessaire

### 3. `maj_etudiants_desmfmc.py`

Script interactif pour mettre à jour les étudiants DESMFMC des années 2 à 4.

**Usage :**
```bash
python scripts/maj_etudiants_desmfmc.py
```

**Fonctionnalités :**
- Associer la bonne classe (DESMFMC année 2/3/4) sur le modèle Utilisateur
- Marquer l'année correspondante comme "admis" dans ResultatAnneeDES

### 4. `test_import.py`

Script de diagnostic pour vérifier que les imports Django fonctionnent correctement.

**Usage :**
```bash
python scripts/test_import.py
```

## Résolution des problèmes

### Erreur : `ModuleNotFoundError: No module named 'core'`

**Cause :** Le script est exécuté depuis le mauvais répertoire.

**Solution :**
1. Vérifiez que vous êtes dans la racine du projet :
   ```bash
   cd C:\Users\HP\Documents\fmos-mfmc
   ```

2. Exécutez le script avec le chemin complet :
   ```bash
   python scripts/nom_du_script.py
   ```

### Erreur : `EOFError: EOF when reading a line`

**Cause :** Le script essaie de lire depuis stdin mais il n'y a pas d'entrée interactive disponible.

**Solution :** Cette erreur est normale si vous exécutez le script dans un environnement non-interactif. Les scripts interactifs nécessitent une console avec entrée utilisateur.

### Vérifier que tout fonctionne

Exécutez le script de diagnostic :
```bash
python scripts/test_import.py
```

Si tous les tests passent avec `[OK]`, alors votre environnement est correctement configuré.

## Notes

- Tous les scripts ajoutent automatiquement le répertoire racine au `PYTHONPATH`
- Les scripts configurent automatiquement `DJANGO_SETTINGS_MODULE`
- Les scripts gèrent l'encodage UTF-8 pour Windows

