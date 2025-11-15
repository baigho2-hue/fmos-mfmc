"""
Migration pour créer les leçons depuis le fichier JSON
Cette migration complète la migration 0010 en créant les objets Lecon
"""
import json
import os
from django.db import migrations
from datetime import datetime


def create_lecons_from_json(apps, schema_editor):
    """
    Crée les objets Lecon depuis le fichier JSON pour tous les cours
    """
    Cours = apps.get_model('utilisateurs', 'Cours')
    Lecon = apps.get_model('utilisateurs', 'Lecon')
    
    # Charger les données extraites depuis le répertoire racine du projet
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    json_path = os.path.join(project_root, 'cours_extracted_improved.json')
    
    if not os.path.exists(json_path):
        print(f"[ATTENTION] Fichier JSON non trouve: {json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    total_lecons_crees = 0
    
    # Traiter chaque année
    for annee_num in range(1, 5):
        annee_key = f'annee_{annee_num}'
        if annee_key not in data:
            continue
        
        annee_data = data[annee_key]
        cours_list = annee_data['cours']
        
        # Pour chaque cours dans cette année
        for cours_data in cours_list:
            code = cours_data['code']
            lecons_data = cours_data.get('lecons', [])
            
            # Trouver le cours correspondant
            cours = Cours.objects.filter(code=code).first()
            
            if not cours:
                continue
            
            # Créer les leçons pour ce cours
            for lecon_data in lecons_data:
                lecon_num = lecon_data.get('numero', 0)
                lecon_titre = lecon_data.get('titre', '').strip()
                lecon_type = lecon_data.get('type', 'lecon')
                
                if not lecon_titre or lecon_titre == '...':
                    continue
                
                # Vérifier si la leçon existe déjà
                lecon_existante = Lecon.objects.filter(cours=cours, numero=lecon_num).first()
                
                if not lecon_existante:
                    # Créer la leçon
                    Lecon.objects.create(
                        cours=cours,
                        titre=lecon_titre,
                        numero=lecon_num,
                        type_lecon=lecon_type,
                        ordre=lecon_num,
                        contenu=None,  # Le contenu sera ajouté manuellement ou via upload
                        actif=True
                    )
                    total_lecons_crees += 1
    
    print(f"[OK] {total_lecons_crees} lecons creees depuis le fichier JSON")


def reverse_create_lecons(apps, schema_editor):
    """
    Supprime les leçons créées par cette migration
    """
    Lecon = apps.get_model('utilisateurs', 'Lecon')
    # Supprimer uniquement les leçons qui n'ont pas de contenu (créées par cette migration)
    Lecon.objects.filter(contenu__isnull=True, fichier_contenu__isnull=True).delete()
    print("[OK] Lecons sans contenu supprimees")


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0012_convert_lecons_from_contenu'),
    ]

    operations = [
        migrations.RunPython(create_lecons_from_json, reverse_create_lecons),
    ]

