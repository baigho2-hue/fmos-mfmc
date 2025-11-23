import openpyxl
from apps.utilisateurs.models_med6 import ListeMed6, EtudiantMed6
from apps.utilisateurs.models import Utilisateur
from django.utils import timezone
import os
import sys

file_path = r"c:\Users\HP\Documents\fmos-mfmc\Liste Med6 2024-2025.xlsx"
log_path = "import_med6_models_log.txt"

def log(msg):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
        f.flush()
    print(msg)

def import_med6_models():
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("")
        
    log("=== Importation dans EtudiantMed6 ===")
    
    try:
        # 1. Créer ou récupérer la liste
        liste, created = ListeMed6.objects.get_or_create(
            annee_universitaire="2024-2025",
            defaults={
                'date_cloture': timezone.now().date() + timezone.timedelta(days=365),
                'fichier_source': "Liste Med6 2024-2025.xlsx",
                'active': True
            }
        )
        log(f"Liste Med 6 2024-2025: {'Créée' if created else 'Existante'}")
        
        if not os.path.exists(file_path):
            log(f"ERREUR: Fichier non trouvé: {file_path}")
            return

        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = wb.active
        
        rows = sheet.iter_rows(min_row=3, values_only=True)
        
        count_created = 0
        count_updated = 0
        count_linked = 0
        count_errors = 0
        
        for i, row in enumerate(rows, 3):
            if not row[1]: 
                continue
            
            matricule = str(row[1]).strip()
            nom = str(row[2]).strip() if row[2] else ""
            prenom = str(row[3]).strip() if row[3] else ""
            
            if i % 50 == 0:
                log(f"Traitement ligne {i}...")
            
            try:
                # Créer/MAJ EtudiantMed6
                etudiant, created_etud = EtudiantMed6.objects.update_or_create(
                    liste=liste,
                    matricule=matricule,
                    defaults={
                        'nom': nom,
                        'prenom': prenom,
                        'actif': True
                    }
                )
                
                if created_etud:
                    count_created += 1
                else:
                    count_updated += 1
                
                # Lier à l'utilisateur existant si possible
                if not etudiant.utilisateur:
                    try:
                        user = Utilisateur.objects.get(username=matricule)
                        etudiant.utilisateur = user
                        etudiant.save()
                        count_linked += 1
                    except Utilisateur.DoesNotExist:
                        pass # Sera créé à la première connexion
                        
            except Exception as e:
                count_errors += 1
                log(f"[ERREUR] Ligne {i} ({matricule}): {e}")
        
        # Mettre à jour le compteur de la liste
        liste.nombre_etudiants = EtudiantMed6.objects.filter(liste=liste).count()
        liste.save()
        
        log("\n=== Résumé EtudiantMed6 ===")
        log(f"Créés : {count_created}")
        log(f"Mis à jour : {count_updated}")
        log(f"Liés à Utilisateur : {count_linked}")
        log(f"Erreurs : {count_errors}")
        log(f"Total dans la liste : {liste.nombre_etudiants}")
        log("===========================")

    except Exception as e:
        log(f"Erreur critique : {e}")
        import traceback
        log(traceback.format_exc())

import_med6_models()
