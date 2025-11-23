import openpyxl

file_path = r"c:\Users\HP\Documents\fmos-mfmc\Liste Med6 2024-2025.xlsx"

wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
sheet = wb.active

# Compter les lignes avec matricule
count = 0
for row in sheet.iter_rows(min_row=3, values_only=True):
    if row[1]:  # Si matricule existe
        count += 1

print(f"Lignes avec matricule dans Excel: {count}")
