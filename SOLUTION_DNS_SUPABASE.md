# 🔧 Solutions pour le problème DNS avec Supabase

## ⚠️ Problème actuel

La connexion à Supabase échoue avec une erreur DNS lors de `migrate`, même si `check` fonctionne.

---

## ✅ Solution 1 : Utiliser Connection Pooling (Recommandé)

Au lieu de "Direct connection", utilisez "Connection Pooling" :

### Étapes :

1. Dans Supabase : **Settings** > **Database** > **Connect**
2. Choisissez **"Pooler session mode"** ou **"Pooler transaction mode"**
3. L'URL aura le port **`6543`** au lieu de `5432`
4. Copiez cette nouvelle URL
5. Mettez à jour le fichier `.env` avec cette URL

**Exemple d'URL avec pooling** :
```
postgresql://postgres:VOTRE_MOT_DE_PASSE@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true
```

---

## ✅ Solution 2 : Vérifier les restrictions IP dans Supabase

1. Dans **Settings** > **Database**
2. Cherchez **"Connection Pooling"** ou **"Network Restrictions"**
3. Vérifiez s'il y a des restrictions IP
4. Si oui, ajoutez votre IP ou désactivez temporairement pour tester

---

## ✅ Solution 3 : Utiliser l'adresse IPv6 directement

Si le DNS ne résout qu'en IPv6, vous pouvez essayer d'utiliser l'adresse IPv6 directement dans l'URL (mais ce n'est pas recommandé car l'IP peut changer).

---

## ✅ Solution 4 : Vérifier la connexion Internet

Assurez-vous que :
- Votre connexion Internet fonctionne
- Aucun VPN n'interfère avec la connexion
- Aucun pare-feu ne bloque le port 5432 ou 6543

---

## ✅ Solution 5 : Utiliser un autre DNS

Essayez de changer votre DNS temporairement :

1. Utilisez Google DNS : `8.8.8.8` et `8.8.4.4`
2. Ou Cloudflare DNS : `1.1.1.1` et `1.0.0.1`

---

## 🎯 Recommandation

**Utilisez "Connection Pooling"** (Solution 1) car :
- C'est plus fiable pour les connexions intermittentes
- Fonctionne mieux avec les problèmes DNS
- Recommandé par Supabase pour les applications web

---

## 📝 Après avoir changé l'URL

1. Mettez à jour le fichier `.env` avec la nouvelle URL
2. Testez : `python manage.py check --database default`
3. Si ça fonctionne, appliquez les migrations : `python manage.py migrate`

