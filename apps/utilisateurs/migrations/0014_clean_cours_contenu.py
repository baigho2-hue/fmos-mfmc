"""
Migration pour nettoyer le champ contenu des cours
Les leçons sont maintenant des entités séparées, donc on peut nettoyer le contenu
"""
from django.db import migrations


def clean_cours_contenu(apps, schema_editor):
    """
    Nettoie le champ contenu des cours en enlevant les sections de leçons
    puisque les leçons sont maintenant des entités séparées
    """
    Cours = apps.get_model('utilisateurs', 'Cours')
    Lecon = apps.get_model('utilisateurs', 'Lecon')
    
    cours_modifies = 0
    
    for cours in Cours.objects.all():
        contenu_original = cours.contenu or ''
        
        # Si le cours a des leçons, nettoyer le contenu
        if cours.lecons.exists():
            # Enlever les sections "LEÇONS DU COURS" et les séparateurs
            lignes = contenu_original.split('\n')
            lignes_nettoyees = []
            dans_section_lecons = False
            
            for ligne in lignes:
                ligne_stripped = ligne.strip()
                
                # Détecter le début de la section des leçons
                if 'LEÇONS DU COURS' in ligne_stripped.upper() or 'LEÇONS' in ligne_stripped.upper():
                    dans_section_lecons = True
                    continue
                
                # Détecter les séparateurs
                if ligne_stripped.startswith('=' * 20):
                    continue
                
                # Détecter les lignes de leçons (format: "Leçon X:" ou "Atelier X:")
                if dans_section_lecons and (ligne_stripped.startswith('Leçon') or ligne_stripped.startswith('Atelier')):
                    continue
                
                # Si on trouve une ligne vide après la section des leçons, on sort
                if dans_section_lecons and ligne_stripped == '':
                    dans_section_lecons = False
                    continue
                
                # Si on n'est pas dans la section des leçons, garder la ligne
                if not dans_section_lecons:
                    lignes_nettoyees.append(ligne)
            
            contenu_nettoye = '\n'.join(lignes_nettoyees).strip()
            
            # Si le contenu nettoyé est vide ou ne contient que la description, 
            # mettre une description générique
            if not contenu_nettoye or contenu_nettoye == cours.description:
                contenu_nettoye = cours.description or f"Ce cours contient {cours.lecons.count()} leçon(s)."
            
            cours.contenu = contenu_nettoye
            cours.save()
            cours_modifies += 1
    
    print(f"[OK] {cours_modifies} cours nettoyes (lecons separees)")


def reverse_clean_cours_contenu(apps, schema_editor):
    """
    Fonction inverse : ne fait rien car on ne peut pas restaurer le contenu original
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0013_create_lecons_from_json'),
    ]

    operations = [
        migrations.RunPython(clean_cours_contenu, reverse_clean_cours_contenu),
    ]

