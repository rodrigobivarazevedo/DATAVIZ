import sqlite3
import csv

# Create or connect to the SQLite database
conn = sqlite3.connect('blood_tests.db')
cursor = conn.cursor()

# Load data from the "blood_indicators.csv" CSV file into the "blood_indicators" table
with open('/home/rodrigo/repos/DATAVIZ_project/dataviz_venv/jupyter_notebooks/blood_indicators.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    # Skip the header row
    next(csv_reader)
    for row in csv_reader:
        cursor.execute("""
    INSERT INTO blood_indicators (
        ID, 
        DATE, 
        Albumin_g_dL, 
        Albumin_g_L, 
        Alanine_aminotransferase_ALT_U_L, 
        Aspartate_aminotransferase_AST_U_L, 
        Alkaline_phosphatase_U_L, 
        Blood_urea_nitrogen_mg_dL, 
        Blood_urea_nitrogen_mmol_L, 
        Total_calcium_mg_dL, 
        Total_calcium_mmol_L, 
        Creatine_Phosphokinase_CPK_IU_L, 
        Cholesterol_mg_dL, 
        Cholesterol_mmol_L, 
        Bicarbonate_mmol_L, 
        Creatinine_mg_dL, 
        Creatinine_umol_L, 
        Gamma_glutamyl_transferase_U_L, 
        Glucose_serum_mg_dL, 
        Glucose_serum_mmol_L, 
        Iron_refrigerated_ug_dL, 
        Iron_refrigerated_umol_L, 
        Lactate_dehydrogenase_U_L, 
        Phosphorus_mg_dL, 
        Phosphorus_mmol_L, 
        Total_bilirubin_mg_dL, 
        Total_bilirubin_umol_L, 
        Total_protein_g_dL, 
        Total_protein_g_L, 
        Uric_acid_mg_dL, 
        Uric_acid_umol_L, 
        Sodium_mmol_L, 
        Potassium_mmol_L, 
        Chloride_mmol_L, 
        Osmolality_mmol_Kg, 
        Globulin_g_dL, 
        Globulin_g_L, 
        Triglycerides_mg_dL, 
        Triglycerides_mmol_L
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", row)



# Load data from the "patients.csv" CSV file into the "patients" table
with open('/home/rodrigo/repos/DATAVIZ_project/dataviz_venv/jupyter_notebooks/patients.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        cursor.execute("INSERT INTO patients (ID, FIRST_NAME, LAST_NAME, BIRTH_DATE, GENDER) VALUES (?, ?, ?, ?, ?)", row)

# Commit the changes and close the database connection
conn.commit()
conn.close()
