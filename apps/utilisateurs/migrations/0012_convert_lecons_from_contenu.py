"""
Migration pour convertir les leçons stockées dans le champ contenu des cours
en objets Lecon séparés
"""
import re
from django.db import migrations


def convert_lecons_from_contenu(apps, schema_editor):
    """
    Convertit les leçons stockées dans le champ contenu des cours en objets Lecon
    """
    Cours = apps.get_model('utilisateurs', 'Cours')
    Lecon = apps.get_model('utilisateurs', 'Lecon')
    
    total_lecons_crees = 0
    
    # Parcourir tous les cours qui ont du contenu avec des leçons
    for cours in Cours.objects.filter(contenu__icontains='Leçon'):
        contenu = cours.contenu
        
        # Extraire les leçons du contenu
        # Format attendu: "Leçon X: titre" ou "Atelier X: titre"
        lecons_pattern = re.compile(r'(Leçon|Atelier)\s+(\d+)\s*[:]?\s*(.+?)(?=\n(?:Leçon|Atelier|\Z))', re.MULTILINE | re.DOTALL)
        
        matches = lecons_pattern.findall(contenu)
        
        if not matches:
            # Essayer un autre format
            lecons_pattern2 = re.compile(r'(Leçon|Atelier)\s+(\d+)\s*[:]?\s*(.+?)(?=\n|$)', re.MULTILINE)
            matches = lecons_pattern2.findall(contenu)
        
        if matches:
            for match in matches:
                type_lecon_str, numero_str, titre = match
                
                # Déterminer le type
                type_lecon = 'atelier' if type_lecon_str.lower() == 'atelier' else 'lecon'
                
                # Nettoyer le titre
                titre = titre.strip()
                if not titre or titre == '...':
                    continue
                
                # Convertir le numéro
                try:
                    numero = int(numero_str)
                except ValueError:
                    continue
                
                # Vérifier si la leçon existe déjà
                lecon_existante = Lecon.objects.filter(cours=cours, numero=numero).first()
                
                if not lecon_existante:
                    # Créer la leçon
                    Lecon.objects.create(
                        cours=cours,
                        titre=titre,
                        numero=numero,
                        type_lecon=type_lecon,
                        ordre=numero,  # Utiliser le numéro comme ordre
                        contenu=None,  # Le contenu sera ajouté plus tard
                        actif=True
                    )
                    total_lecons_crees += 1
    
    print(f"[OK] {total_lecons_crees} lecons converties depuis le champ contenu")


def reverse_convert_lecons(apps, schema_editor):
    """
    Fonction inverse : supprime les leçons créées (mais ne restaure pas le contenu)
    """
    Lecon = apps.get_model('utilisateurs', 'Lecon')
    Lecon.objects.all().delete()
    print("[OK] Toutes les lecons ont ete supprimees")


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0011_lecon'),
    ]

    operations = [
        migrations.RunPython(convert_lecons_from_contenu, reverse_convert_lecons),
    ]

