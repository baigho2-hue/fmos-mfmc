@echo off
REM -------------------------------------------------------------
REM Script pour configurer et lancer FMOS MFMC sur Windows
REM -------------------------------------------------------------

REM 1️ Activer l'environnement virtuel
call .venv\Scripts\activate

REM 2 Vérifier que Python et Django sont accessibles
python --version
python -m django --version

REM 3️ Vérifier la connexion à PostgreSQL
echo Vérification de la base de données...
python - <<END
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
try:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    print("Connexion à la base PostgreSQL réussie !")
    conn.close()
except Exception as e:
    print(f"❌ Erreur de connexion : {e}")
END

REM 4️ Appliquer les migrations
echo Application des migrations...
python manage.py makemigrations
python manage.py migrate

REM 5️ Créer un superuser (si nécessaire)
echo Vérification du superuser...
python - <<END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("Création du superuser...")
    User.objects.create_superuser('admin', 'admin@example.com', 'Admin1234')
    print("Superuser créé avec login 'admin' et mot de passe 'Admin1234'")
else:
    print("Superuser déjà existant")
END

REM 6️ Lancer le serveur de développement
echo Lancement du serveur...
python manage.py runserver

pause
