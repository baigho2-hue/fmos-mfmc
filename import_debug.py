import openpyxl
from apps.utilisateurs.models import Utilisateur
import os
import sys

file_path = r"c:\Users\HP\Documents\fmos-mfmc\Liste Med6 2024-2025.xlsx"
log_path = "import_log_debug.txt"

def log(msg):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
        f.flush() # Force write
    print(msg)

def import_students_debug():
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("")
        
    log("=== DEBUG IMPORT (5 rows) ===")
    
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = wb.active
        log(f"Sheet: {sheet.title}")
        
        rows = sheet.iter_rows(min_row=3, values_only=True)
        
        count = 0
        for i, row in enumerate(rows, 3):
            if count >= 5:
                break
                
            if not row[1]:
                continue
                
            matricule = str(row[1]).strip()
            log(f"Processing {matricule}...")
            
            try:
                user, created = Utilisateur.objects.get_or_create(
                    username=matricule,
                    defaults={
                        'first_name': 'Test',
                        'last_name': 'Debug',
                        'email': f"{matricule}@debug.com",
                        'type_utilisateur': 'etudiant',
                        'classe': 'Médecine 6'
                    }
                )
                log(f"Result: {'Created' if created else 'Exists'}")
                count += 1
            except Exception as e:
                log(f"Error: {e}")
                
    except Exception as e:
        log(f"Critical Error: {e}")

import_students_debug()
