# Configuration Supabase

Pour utiliser Supabase, vous devez mettre à jour votre fichier `.env` avec les paramètres de connexion Supabase.

## Paramètres Supabase

Dans votre projet Supabase, allez dans :
**Settings > Database > Connection string > URI**

Vous obtiendrez une URL comme :
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

## Configuration du fichier .env

Mettez à jour votre fichier `.env` avec :

```env
DEBUG=True
SECRET_KEY=django-insecure-1234567890abcdefghijklmnopqrstuvwxyz

# Configuration Supabase
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe_supabase
DB_HOST=db.xxxxx.supabase.co
DB_PORT=5432

ALLOWED_HOSTS=127.0.0.1,localhost
```

## Alternative : Connection Pooling (recommandé pour Supabase)

Pour de meilleures performances, utilisez le connection pooling de Supabase :

```env
DB_HOST=db.xxxxx.supabase.co
DB_PORT=6543  # Port de pooling (au lieu de 5432)
```

## Vérification de la connexion

Après avoir mis à jour le `.env`, testez la connexion :

```bash
python manage.py dbshell
```

Si la connexion fonctionne, vous verrez le prompt PostgreSQL.

