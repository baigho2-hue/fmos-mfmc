# 🔑 Réinitialiser le mot de passe Supabase

## ⚠️ Problème actuel

L'authentification échoue avec l'erreur : `password authentication failed for user "postgres"`

---

## ✅ Solution : Réinitialiser le mot de passe dans Supabase

### Étape 1 : Accéder aux paramètres Database

1. Allez dans votre projet Supabase
2. Cliquez sur **⚙️ Settings**
3. Cliquez sur **"Database"**

### Étape 2 : Réinitialiser le mot de passe

1. Cherchez la section **"Database password"** ou **"Reset database password"**
2. Cliquez sur **"Reset database password"** ou **"Generate new password"**
3. **⚠️ IMPORTANT : Notez le nouveau mot de passe immédiatement !** Vous ne le reverrez plus après.

### Étape 3 : Mettre à jour le fichier .env

Une fois que vous avez le nouveau mot de passe :

1. **Encodez le mot de passe** si nécessaire (caractères spéciaux)
2. **Mettez à jour** le fichier `.env` avec le nouveau mot de passe

---

## 🔧 Encoder le mot de passe

Si votre nouveau mot de passe contient des caractères spéciaux, ils doivent être encodés dans l'URL :

- `@` → `%40`
- `#` → `%23`
- `%` → `%25`
- `&` → `%26`
- `+` → `%2B`
- `=` → `%3D`
- ` ` (espace) → `%20`

**Exemple** :
- Mot de passe : `MonNouveauMot@123`
- Encodé : `MonNouveauMot%40123`
- URL : `postgresql://postgres.bmfkvwpfeuyserrfrqjb:MonNouveauMot%40123@aws-1-eu-north-1.pooler.supabase.com:5432/postgres`

---

## 📝 Format de l'URL complète

Votre URL devrait ressembler à :

```
postgresql://postgres.bmfkvwpfeuyserrfrqjb:VOTRE_NOUVEAU_MOT_DE_PASSE_ENCODE@aws-1-eu-north-1.pooler.supabase.com:5432/postgres
```

---

## ✅ Après avoir mis à jour le mot de passe

1. Mettez à jour le fichier `.env`
2. Testez : `python manage.py check --database default`
3. Si ça fonctionne, appliquez les migrations : `python manage.py migrate`

---

## 💡 Astuce

Si vous avez des difficultés à encoder le mot de passe, dites-moi le nouveau mot de passe et je l'encoderai pour vous et mettrai à jour le fichier `.env`.

