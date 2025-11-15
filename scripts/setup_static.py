# scripts/setup_static.py
import os
from pathlib import Path

# Chemin vers le dossier static du projet
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

# Sous-dossiers à créer
subfolders = [
    "css",
    "js",
    "images",
    "fonts",
]

# Création des dossiers
for folder in subfolders:
    path = STATIC_DIR / folder
    path.mkdir(parents=True, exist_ok=True)
    print(f"Dossier créé : {path}")

# Création d'un favicon.ico par défaut
favicon_path = STATIC_DIR / "images" / "favicon.ico"
if not favicon_path.exists():
    # Contenu binaire minimal pour un favicon très simple
    favicon_content = bytes([
        0x00,0x00,0x01,0x00,0x01,0x00,0x10,0x10,0x00,0x00,0x01,0x00,0x04,0x00,
        0x28,0x01,0x00,0x00,0x16,0x00,0x00,0x00,0x28,0x00,0x00,0x00,0x10,0x00,
        0x00,0x00,0x20,0x00,0x00,0x00,0x01,0x00,0x04,0x00,0x00,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xFF,0xFF,0xFF,0x00,0x00,0x00,
        0x00,0x00,0x00,0x00
    ])
    with open(favicon_path, "wb") as f:
        f.write(favicon_content)
    print(f"Favicon créé : {favicon_path}")
else:
    print(f"Favicon déjà existant : {favicon_path}")

print("Configuration static terminée !")
