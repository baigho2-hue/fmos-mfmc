"""
Migration pour insérer les cours et leurs leçons depuis les fichiers Word du programme DESMFMC
"""
import json
import os
from django.db import migrations
from django.utils import timezone
from datetime import datetime, timedelta


def seed_cours_lecons(apps, schema_editor):
    """
    Insère les cours et leurs leçons pour les 4 années du DESMFMC
    Les données sont extraites du fichier JSON généré depuis les fichiers Word
    """
    Classe = apps.get_model('utilisateurs', 'Classe')
    Cours = apps.get_model('utilisateurs', 'Cours')
    Formation = apps.get_model('utilisateurs', 'Formation')
    
    # Charger les données extraites depuis le répertoire racine du projet
    # Le fichier JSON doit être dans le répertoire racine (même niveau que manage.py)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    json_path = os.path.join(project_root, 'cours_extracted_improved.json')
    
    if not os.path.exists(json_path):
        print(f"[ATTENTION] Fichier JSON non trouvé: {json_path}")
        print("Veuillez d'abord exécuter extract_cours_improved.py pour générer les données")
        print(f"Recherche dans: {json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Récupérer la formation DESMFMC
    try:
        formation = Formation.objects.get(code='DESMFMC')
    except Formation.DoesNotExist:
        print("[ERREUR] Formation DESMFMC non trouvée. Veuillez d'abord exécuter la migration 0006_seed_desmfmc_programme.py")
        return
    
    # Dates de référence pour les cours (année académique 2025-2026)
    date_debut_annee = {
        1: datetime(2025, 9, 1).date(),
        2: datetime(2025, 9, 1).date(),
        3: datetime(2025, 9, 1).date(),
        4: datetime(2025, 9, 1).date(),
    }
    
    total_cours_crees = 0
    total_lecons_inserees = 0
    
    # Traiter chaque année
    for annee_num in range(1, 5):
        annee_key = f'annee_{annee_num}'
        if annee_key not in data:
            continue
        
        annee_data = data[annee_key]
        annee = annee_data['annee']
        cours_list = annee_data['cours']
        
        # Trouver ou créer la classe pour cette année
        # Format: "DESMFMC - Année X" ou similaire
        classe_nom = f"DESMFMC - Année {annee}"
        classe_code = f"DESMFMC-A{annee}"
        
        # Dates pour la classe (année académique)
        classe_date_debut = date_debut_annee[annee]
        classe_date_fin = datetime(classe_date_debut.year + 1, 8, 31).date()  # Fin août de l'année suivante
        
        classe, created = Classe.objects.get_or_create(
            code=classe_code,
            defaults={
                'formation': formation,
                'nom': classe_nom,
                'annee': annee,
                'date_debut': classe_date_debut,
                'date_fin': classe_date_fin,
                'actif': True
            }
        )
        
        if created:
            print(f"[OK] Classe créée: {classe_nom}")
        else:
            # Mettre à jour si nécessaire
            classe.nom = classe_nom
            classe.annee = annee
            classe.date_debut = classe_date_debut
            classe.date_fin = classe_date_fin
            classe.actif = True
            classe.save()
        
        # Date de début pour les cours de cette année
        date_debut = date_debut_annee[annee]
        date_courante = date_debut
        
        # Créer les cours pour cette année
        for idx, cours_data in enumerate(cours_list):
            titre = cours_data['titre']
            code = cours_data['code']
            volume_horaire = cours_data.get('volume_horaire', 0)
            lecons = cours_data.get('lecons', [])
            competence = cours_data.get('competence', '')
            
            # Construire la description avec les leçons
            description_parts = []
            if competence:
                description_parts.append(f"Compétence: {competence}")
            
            if cours_data.get('titre_complet'):
                description_parts.append(f"Cours: {cours_data['titre_complet']}")
            
            # Construire le contenu avec les leçons
            contenu_parts = []
            if lecons:
                contenu_parts.append("LEÇONS DU COURS:\n")
                contenu_parts.append("=" * 60)
                for lecon in lecons:
                    lecon_num = lecon.get('numero', '')
                    lecon_titre = lecon.get('titre', '')
                    lecon_type = lecon.get('type', 'lecon')
                    
                    if lecon_type == 'atelier':
                        contenu_parts.append(f"\nAtelier {lecon_num}: {lecon_titre}")
                    else:
                        contenu_parts.append(f"\nLeçon {lecon_num}: {lecon_titre}")
                contenu_parts.append("\n" + "=" * 60)
            
            description = "\n".join(description_parts) if description_parts else f"Cours de {titre}"
            contenu = "\n".join(contenu_parts) if contenu_parts else description
            
            # Calculer les dates (répartir les cours sur l'année)
            # Chaque cours dure environ 2-4 semaines selon le volume horaire
            duree_semaines = max(2, min(8, volume_horaire // 5))  # 5h par semaine en moyenne
            date_fin = date_courante + timedelta(weeks=duree_semaines)
            
            # Créer ou mettre à jour le cours
            cours, created = Cours.objects.get_or_create(
                code=code,
                classe=classe,
                defaults={
                    'titre': titre,
                    'description': description,
                    'contenu': contenu,
                    'volume_horaire': volume_horaire,
                    'date_debut': date_courante,
                    'date_fin': date_fin,
                    'ordre': idx + 1,
                    'actif': True
                }
            )
            
            if not created:
                # Mettre à jour le cours existant
                cours.titre = titre
                cours.description = description
                cours.contenu = contenu
                cours.volume_horaire = volume_horaire
                cours.date_debut = date_courante
                cours.date_fin = date_fin
                cours.ordre = idx + 1
                cours.actif = True
                cours.save()
            
            total_cours_crees += 1
            total_lecons_inserees += len(lecons)
            
            # Passer à la date suivante pour le prochain cours
            date_courante = date_fin + timedelta(days=7)  # 1 semaine entre les cours
        
        print(f"[OK] Année {annee}: {len(cours_list)} cours créés/mis à jour")
    
    print(f"\n[OK] Migration terminée:")
    print(f"  - {total_cours_crees} cours créés/mis à jour")
    print(f"  - {total_lecons_inserees} leçons insérées")


def unseed_cours_lecons(apps, schema_editor):
    """
    Supprime les cours créés par cette migration
    """
    Classe = apps.get_model('utilisateurs', 'Classe')
    Cours = apps.get_model('utilisateurs', 'Cours')
    
    # Supprimer les cours des classes DESMFMC
    classes = Classe.objects.filter(code__startswith='DESMFMC-A')
    for classe in classes:
        Cours.objects.filter(classe=classe).delete()
        print(f"[OK] Cours supprimés pour {classe.nom}")


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0009_seed_cscom_u'),
    ]

    operations = [
        migrations.RunPython(seed_cours_lecons, unseed_cours_lecons),
    ]

