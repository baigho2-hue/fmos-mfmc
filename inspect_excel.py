import openpyxl

file_path = r"c:\Users\HP\Documents\fmos-mfmc\Liste Med6 2024-2025.xlsx"
output_path = "inspect_result.txt"

with open(output_path, "w", encoding="utf-8") as f:
    try:
        wb = openpyxl.load_workbook(file_path, read_only=True)
        sheet = wb.active
        f.write(f"Feuille active: {sheet.title}\n")
        
        # Lire la première ligne (en-têtes)
        headers = []
        for cell in sheet[1]:
            headers.append(str(cell.value))
        
        f.write("=== Colonnes (En-têtes) ===\n")
        f.write(str(headers) + "\n")
        
        f.write("\n=== 5 premières lignes de données ===\n")
        rows = sheet.iter_rows(min_row=2, max_row=6, values_only=True)
        for row in rows:
            f.write(str(row) + "\n")
            
    except Exception as e:
        f.write(f"Erreur avec openpyxl: {e}\n")
