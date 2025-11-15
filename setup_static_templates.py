import os
from pathlib import Path

# Chemin du dossier core (là où se trouve core/settings.py)
BASE_DIR = Path(__file__).resolve().parent
CORE_DIR = BASE_DIR / 'core'

# Création du dossier templates dans core
templates_dir = CORE_DIR / 'templates'
templates_dir.mkdir(parents=True, exist_ok=True)

# Création du fichier base.html minimal
base_html = templates_dir / 'base.html'
if not base_html.exists():
    base_html.write_text('''{% load static %}
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>FMOS MFMC</title>
    <link rel="shortcut icon" href="{% static 'images/favicon.ico' %}" type="image/x-icon">
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>
''', encoding='utf-8')

