import psycopg2
import os
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

try:
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    print("✅ Connexion réussie à PostgreSQL !")
    connection.close()
except Exception as e:
    print("❌ Erreur de connexion :", e)
