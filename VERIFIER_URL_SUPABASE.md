# 🔍 Vérifier votre URL Supabase

## ⚠️ Problème actuel

La connexion à Supabase échoue avec une erreur DNS. Il faut vérifier que l'URL est correcte.

---

## ✅ Étapes pour vérifier votre URL Supabase

### Étape 1 : Accéder à votre projet Supabase

1. Allez sur https://supabase.com/dashboard
2. Connectez-vous à votre compte
3. Sélectionnez votre projet

### Étape 2 : Vérifier que le projet est actif

1. Vérifiez que le projet n'est pas en pause ou suspendu
2. Si le projet est en pause, cliquez sur "Resume" pour le réactiver

### Étape 3 : Obtenir la bonne URL de connexion

1. Dans le menu de gauche, cliquez sur **⚙️ Settings**
2. Cliquez sur **"Database"**
3. Cliquez sur le bouton **"Connect"**
4. Choisissez **"Direct connection"**
5. **Copiez l'URL complète** qui s'affiche

L'URL devrait ressembler à :
```
postgresql://postgres:[YOUR-PASSWORD]@db.XXXXXXXXXXXXX.supabase.co:5432/postgres
```

### Étape 4 : Vérifier le hostname

Le hostname dans l'URL devrait être :
```
db.XXXXXXXXXXXXX.supabase.co
```

Où `XXXXXXXXXXXXX` est votre identifiant de projet unique.

**Vérifiez que le hostname dans votre URL correspond exactement à celui affiché dans Supabase.**

---

## 🔧 Si l'URL est différente

Si l'URL dans Supabase est différente de celle dans votre fichier `.env` :

1. **Copiez la nouvelle URL** depuis Supabase
2. **Remplacez `[YOUR-PASSWORD]`** par votre mot de passe Supabase
3. **Encodez le mot de passe** si nécessaire (caractères spéciaux comme `@`, `#`, `%` doivent être encodés)
4. **Mettez à jour le fichier `.env`**

---

## 🔑 Réinitialiser le mot de passe si nécessaire

Si vous ne connaissez pas votre mot de passe :

1. Dans **Settings** > **Database**
2. Cherchez **"Database password"** ou **"Reset database password"**
3. Cliquez sur **"Reset database password"**
4. **Notez le nouveau mot de passe** (vous ne le reverrez plus !)
5. Utilisez ce nouveau mot de passe dans votre URL

---

## 📝 Encoder le mot de passe dans l'URL

Si votre mot de passe contient des caractères spéciaux, ils doivent être encodés :

- `@` → `%40`
- `#` → `%23`
- `%` → `%25`
- `&` → `%26`
- `+` → `%2B`
- `=` → `%3D`
- ` ` (espace) → `%20`

**Exemple** :
- Mot de passe : `MonMot@123`
- Encodé : `MonMot%40123`
- URL : `postgresql://postgres:MonMot%40123@db.xxxxx.supabase.co:5432/postgres`

---

## 🆘 Vérifications supplémentaires

### Vérifier que le projet n'est pas suspendu

1. Dans le tableau de bord Supabase, vérifiez l'état du projet
2. Si le projet est suspendu, réactivez-le

### Vérifier les restrictions IP

1. Dans **Settings** > **Database**
2. Vérifiez s'il y a des restrictions IP
3. Si oui, ajoutez votre IP ou désactivez temporairement les restrictions pour tester

### Vérifier la connexion Internet

Assurez-vous que votre connexion Internet fonctionne correctement.

---

## ✅ Une fois l'URL vérifiée

1. Mettez à jour le fichier `.env` avec la bonne URL
2. Testez la connexion : `python manage.py check --database default`
3. Si ça fonctionne, appliquez les migrations : `python manage.py migrate`

---

## 💡 Besoin d'aide ?

Dites-moi :
1. **Le hostname exact** que vous voyez dans Supabase (Settings > Database > Connect > Direct connection)
2. **Si le projet est actif** ou en pause
3. **Si vous voyez des restrictions IP** dans les paramètres

Je pourrai vous aider à corriger l'URL !

