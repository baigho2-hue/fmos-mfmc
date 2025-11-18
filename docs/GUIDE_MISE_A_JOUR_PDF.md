# Guide de Mise à Jour du Programme avec le PDF

## Objectif

Mettre à jour le programme DESMFMC avec les données exactes du fichier **"Programme DES de MF-MC.pdf"**.

## Étapes

### 1. Extraire le texte du PDF

#### Option A : Utiliser le script fourni
```bash
# Installer une bibliothèque PDF (choisir une seule)
pip install PyPDF2
# ou
pip install pdfplumber
# ou
pip install pypdf

# Extraire le texte
python manage.py parse_pdf_programme "Programme DES de MF-MC.pdf"
```

Le script créera un fichier `programme_desmfmc_extrait.txt` avec le contenu du PDF.

#### Option B : Lecture manuelle
Ouvrir le PDF et noter les informations suivantes pour chaque année/semestre :
- Nom du jalon
- Modules avec leurs volumes horaires
- Cours dans chaque module
- Objectifs et compétences

### 2. Mettre à jour le script d'initialisation

#### Option A : Utiliser la structure détaillée existante
Le script `init_programme_desmfmc_detaille.py` contient déjà une structure complète avec :
- 8 jalons (4 années × 2 semestres)
- ~30 modules répartis sur les 4 années
- Volumes horaires estimés

**Pour l'utiliser :**
```bash
python manage.py init_programme_desmfmc_detaille
```

#### Option B : Modifier le script selon le PDF

1. Ouvrir `apps/utilisateurs/management/commands/init_programme_desmfmc_detaille.py`

2. Pour chaque jalon, mettre à jour :
   ```python
   {
       'nom': 'Nom exact du jalon selon le PDF',
       'code': 'DESMFMC-A1-S1',
       'description': 'Description du jalon',
       'modules': [
           {
               'nom': 'Nom exact du module',
               'code': 'CODE-MODULE',
               'volume_horaire': 120,  # Volume horaire exact du PDF
               'description': 'Description du module'
           },
           # ... autres modules
       ]
   }
   ```

3. Vérifier les volumes horaires totaux

4. Exécuter le script mis à jour :
   ```bash
   python manage.py init_programme_desmfmc_detaille
   ```

### 3. Créer les cours

Après avoir créé les jalons et modules :

1. Aller dans l'admin Django
2. Pour chaque module, créer les cours correspondants dans les classes appropriées
3. Lier les cours aux modules via **CoursProgramme** :
   - Sélectionner le module
   - Sélectionner le cours
   - Définir l'ordre dans le module
   - Indiquer si le cours est obligatoire

### 4. Ajouter les objectifs et compétences

Pour chaque module :
1. Créer les **ObjectifApprentissage** liés au module
2. Créer les **Competence** visées par le module
3. Lier les objectifs et compétences au module

### 5. Vérifier et ajuster

1. Vérifier que tous les jalons sont créés
2. Vérifier que tous les modules sont créés
3. Vérifier que les volumes horaires correspondent au PDF
4. Vérifier que les cours sont bien liés aux modules
5. Tester l'affichage du programme complet

## Structure attendue dans le PDF

Le PDF devrait contenir :

### Pour chaque année (1 à 4) :

#### Semestre 1 :
- Nom du jalon
- Modules :
  - Nom du module
  - Volume horaire
  - Cours (liste)
  - Objectifs
  - Compétences

#### Semestre 2 :
- (même structure)

## Exemple de données à extraire

```
ANNÉE 1 - SEMESTRE 1
Jalon : Fondamentaux de la médecine de famille

Module 1 : Introduction à la médecine de famille
- Volume horaire : 40h
- Cours :
  * Histoire de la médecine de famille (10h)
  * Philosophie et valeurs (10h)
  * Rôle du médecin de famille (20h)
- Objectifs : ...
- Compétences : ...

Module 2 : Médecine générale de base
- Volume horaire : 120h
- Cours :
  * Histoire clinique (30h)
  * Examen physique (40h)
  * Décision clinique (50h)
- ...
```

## Commandes utiles

```bash
# Créer les migrations
python manage.py makemigrations utilisateurs

# Appliquer les migrations
python manage.py migrate

# Initialiser la structure de base
python manage.py init_programme_desmfmc

# Initialiser la structure détaillée
python manage.py init_programme_desmfmc_detaille

# Extraire le texte du PDF
python manage.py parse_pdf_programme "Programme DES de MF-MC.pdf"
```

## Fichiers à modifier

- `apps/utilisateurs/management/commands/init_programme_desmfmc_detaille.py` : Structure détaillée du programme
- `PROGRAMME_DESMFMC_DONNEES.py` : Fichier de données (optionnel, pour référence)

## Support

Si vous rencontrez des difficultés :
1. Vérifier que le PDF est bien lisible
2. Vérifier que les données extraites sont cohérentes
3. Vérifier que les volumes horaires sont corrects
4. Vérifier que les codes des modules sont uniques

