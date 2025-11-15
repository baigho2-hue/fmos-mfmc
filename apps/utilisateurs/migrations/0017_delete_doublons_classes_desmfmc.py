"""
Migration pour supprimer les classes DESMFMC doublons
"""
from django.db import migrations


def delete_doublons_classes(apps, schema_editor):
    """Supprime les classes DESMFMC doublons"""
    Classe = apps.get_model('utilisateurs', 'Classe')
    Cours = apps.get_model('utilisateurs', 'Cours')
    Planification = apps.get_model('utilisateurs', 'Planification')
    
    # IDs des classes doublons à supprimer
    classes_doublons_ids = [5, 6, 7, 8]
    
    # Noms des classes doublons (pour vérification)
    noms_doublons = [
        'DESMFMC - Année 1 Internat rotatoire',
        'DESMFMC - Année 2 Immersion CSCOM-U',
        'DESMFMC - Année 3 Consolidation communautaire',
        'DESMFMC - Année 4 Autonomie et expertise',
    ]
    
    classes_a_supprimer = Classe.objects.filter(id__in=classes_doublons_ids)
    
    print("\n[INFO] Suppression des classes doublons DESMFMC:")
    
    for classe in classes_a_supprimer:
        # Vérifier les données associées
        nb_cours = Cours.objects.filter(classe=classe).count()
        nb_planifications = Planification.objects.filter(classe=classe).count()
        
        print(f"\n  Classe: {classe.nom} (ID: {classe.id})")
        print(f"    - Cours associés: {nb_cours}")
        print(f"    - Planifications associées: {nb_planifications}")
        
        if nb_cours > 0:
            print(f"    [ATTENTION] {nb_cours} cours seront également supprimés")
            # Supprimer les cours associés
            Cours.objects.filter(classe=classe).delete()
        
        if nb_planifications > 0:
            print(f"    [ATTENTION] {nb_planifications} planifications seront également supprimées")
            # Supprimer les planifications associées
            Planification.objects.filter(classe=classe).delete()
        
        # Supprimer la classe
        classe.delete()
        print(f"    [OK] Classe supprimée")
    
    print("\n[OK] Suppression terminée")


def reverse_delete_doublons_classes(apps, schema_editor):
    """Ne peut pas restaurer les classes supprimées"""
    # Cette migration ne peut pas être inversée car les données ont été supprimées
    print("[INFO] Cette migration ne peut pas être inversée")


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0016_seed_methodes_pedagogiques'),
    ]

    operations = [
        migrations.RunPython(delete_doublons_classes, reverse_delete_doublons_classes),
    ]

