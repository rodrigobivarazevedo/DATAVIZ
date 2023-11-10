import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('blood_tests.db')
cursor = conn.cursor()

# Create the "blood_indicators" table with the specified columns
cursor.execute('''
   CREATE TABLE IF NOT EXISTS blood_indicators (
    ID INTEGER,
    DATE DATE,
    Albumin_g_dL INTEGER,
    Albumin_g_L INTEGER,
    Alanine_aminotransferase_ALT_U_L INTEGER,
    Aspartate_aminotransferase_AST_U_L INTEGER,
    Alkaline_phosphatase_U_L INTEGER,
    Blood_urea_nitrogen_mg_dL INTEGER,
    Blood_urea_nitrogen_mmol_L INTEGER,
    Total_calcium_mg_dL INTEGER,
    Total_calcium_mmol_L INTEGER,
    Creatine_Phosphokinase_CPK_IU_L INTEGER,
    Cholesterol_mg_dL INTEGER,
    Cholesterol_mmol_L INTEGER,
    Bicarbonate_mmol_L INTEGER,
    Creatinine_mg_dL INTEGER,
    Creatinine_umol_L INTEGER,
    Gamma_glutamyl_transferase_U_L INTEGER,
    Glucose_serum_mg_dL INTEGER,
    Glucose_serum_mmol_L INTEGER,
    Iron_refrigerated_ug_dL INTEGER,
    Iron_refrigerated_umol_L INTEGER,
    Lactate_dehydrogenase_U_L INTEGER,
    Phosphorus_mg_dL INTEGER,
    Phosphorus_mmol_L INTEGER,
    Total_bilirubin_mg_dL INTEGER,
    Total_bilirubin_umol_L INTEGER,
    Total_protein_g_dL INTEGER,
    Total_protein_g_L INTEGER,
    Uric_acid_mg_dL INTEGER,
    Uric_acid_umol_L INTEGER,
    Sodium_mmol_L INTEGER,
    Potassium_mmol_L INTEGER,
    Chloride_mmol_L INTEGER,
    Osmolality_mmol_Kg INTEGER,
    Globulin_g_dL INTEGER,
    Globulin_g_L INTEGER,
    Triglycerides_mg_dL INTEGER,
    Triglycerides_mmol_L INTEGER
);

''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        ID INTEGER,
        FIRST_NAME TEXT,
        LAST_NAME TEXT,
        BIRTH_DATE DATE,
        GENDER TEXT
    )
''')

# Commit the changes and close the database connection
conn.commit()
conn.close()