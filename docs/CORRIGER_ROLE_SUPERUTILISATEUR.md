# 🔧 Corriger le Rôle du Superutilisateur

Si votre superutilisateur est marqué comme "étudiant" au lieu d'enseignant avec accès complet, voici comment le corriger.

---

## 🎯 Solution 1 : Via l'Admin Django (Rapide)

1. Allez sur : `https://fmos-mfmc.onrender.com/admin/`
2. Connectez-vous avec votre superutilisateur
3. Allez dans **"Utilisateurs"**
4. Cliquez sur votre superutilisateur
5. Modifiez :
   - **Type d'utilisateur** : `Enseignant`
   - **Niveau d'accès** : `Accès complet`
6. Cliquez sur **"Enregistrer"**

---

## 🎯 Solution 2 : Via l'Interface Setup

1. Allez sur : `https://fmos-mfmc.onrender.com/setup/?token=VOTRE_TOKEN`
2. Utilisez le formulaire pour créer un nouveau superutilisateur
3. Le nouveau superutilisateur sera automatiquement créé comme enseignant avec accès complet

---

## 🎯 Solution 3 : Via la Commande Django (Recommandé)

### Dans le Shell Render (si disponible)

```bash
python manage.py corriger_superutilisateurs
```

Cela corrigera tous les superutilisateurs existants.

### Pour un utilisateur spécifique

```bash
python manage.py corriger_superutilisateurs --username admin
```

---

## ✅ Vérification

Après la correction, vérifiez dans l'admin Django que :
- **Type d'utilisateur** : `Enseignant`
- **Niveau d'accès** : `Accès complet`
- **Superutilisateur** : `Oui`

---

## 🔄 Correction Automatique

Les nouvelles créations de superutilisateurs via :
- La commande `creer_superuser`
- L'interface setup `/setup/create-superuser/`

Sont maintenant automatiquement créées comme **enseignant avec accès complet**.

---

## 📝 Note

Les superutilisateurs Django (`is_superuser=True`) ont toujours accès à tout dans l'admin Django, mais pour les fonctionnalités de l'application (cours, évaluations, etc.), ils doivent être définis comme **enseignant avec accès complet**.

---

**Dernière mise à jour** : Novembre 2025

