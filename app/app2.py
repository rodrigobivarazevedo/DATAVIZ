from flask import Flask, request, jsonify, render_template, url_for
from datetime import datetime
import requests
from cs50 import SQL
from healthy_levels import healthy_levels_young_adults, older_adults_reference_ranges, older_elderly_reference_ranges
from blood_functions import color_mapping, transform_to_fhir_blood_test, color_percentages


app2 = Flask(__name__)
db = SQL("sqlite:////home/rodrigo/repos/DATAVIZ_project/db/blood_tests.db")
    

@app2.route("/")
def patient_data():
    return render_template("views2.html")  

@app2.route("/heatmap")
def visualization():
    return render_template("heatmap.html") 
    
# Sample raw data endpoint for patient data
@app2.route('/<int:patientID>/raw', methods=["POST"])
def get_patient_raw(patientID):
    # Get patient information from the database
    patient_data = db.execute("SELECT * FROM patients WHERE ID = ?", patientID)
    # date_of_birth is in the format 'YYYY-MM-DD'
    birth_date = datetime.strptime(patient_data[0]["BIRTH_DATE"], '%Y-%m-%d')
    current_date = datetime.now()
    
    # Calculate the difference in years
    age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    # Add the "AGE" key to the dictionary
    patient_data[0]["AGE"] = age
    return patient_data 

# Sample FHIR data endpoint for Patient data
@app2.route('/<int:patientID>/fhir', methods=["POST"])
def get_patient_fhir(patientID):
    
    patient_data = db.execute("SELECT * FROM patients WHERE ID = ?", patientID)
    
    fhir_patient = {
        "resourceType": "Patient",
        "id": patient_data.ID,
        "name": [
            {
                "given": [patient_data.FIRST_NAME],
                "family": patient_data.LAST_NAME,
            }
        ],
        "birthDate": str(patient_data.BIRTH_DATE),
        "gender": patient_data.GENDER,
        
    }

    # Convert to regular dictionary if needed
    return jsonify(fhir_patient)



@app2.route('/blood_tests/fhir/<int:patientID>', methods=['GET'])
def get_blood_tests_fhir(patientID):
    # Build the URL for the raw data endpoint
    raw_data_url = url_for('get_blood_tests_raw', patientID=patientID)

    # Make a request to the raw data endpoint
    response = requests.get(raw_data_url)  # Use requests.get instead of request.get

    if response.status_code == 200:
        # Process blood_tests as needed and return the raw data with colors
        colored_blood_test_data = response.json()

        # Transform each blood test data to FHIR format
        return [transform_to_fhir_blood_test(blood_test, patientID) for blood_test in colored_blood_test_data]
    else:
        # Handle the case where the raw data request fails
        return "Failed to retrieve raw blood test data.", response.status_code

@app2.route("/blood_dates")
def dates():
    q = request.args.get("q")
    if q:
        dates = db.execute("SELECT DATE FROM blood_indicators WHERE ID = ?", q)
    else:
        dates = []
    return dates
    
        
# base_url}/blood_tests/{patient_id}?date={date_param}
# Sample FHIR data endpoint for blood test
@app2.route('/blood_tests/raw/<int:patientID>', methods=['GET'])
def get_blood_tests_raw(patientID):
    
    date_param_str = request.args.get('date', None)
    date_param = datetime.strptime(date_param_str, '%Y-%m-%d').date()
    try:
        query = "SELECT * FROM blood_indicators WHERE ID = ? AND `DATE` = ?"
        values = (patientID, date_param)
        blood_tests = db.execute(query, *values)
    
    except Exception as e:
        print("Error executing SQL query:", e)

  
    formated_blood_tests = []
    for blood_test in blood_tests:
        formated_blood_tests.append({
            
            'Albumin (g/dL)': blood_test['Albumin_g_dL'],
            'Albumin (g/L)': blood_test['Albumin_g_L'],
            'Alanine aminotransferase ALT (U/L)': blood_test['Alanine_aminotransferase_ALT_U_L'],
            'Aspartate aminotransferase AST (U/L)': blood_test['Aspartate_aminotransferase_AST_U_L'],
            'Alkaline phosphatase (U/L)': blood_test['Alkaline_phosphatase_U_L'],
            'Blood urea nitrogen (mg/dL)': blood_test['Blood_urea_nitrogen_mg_dL'],
            'Blood urea nitrogen (mmol/L)': blood_test['Blood_urea_nitrogen_mmol_L'],
            'Total calcium (mg/dL)': blood_test['Total_calcium_mg_dL'],
            'Total calcium (mmol/L)': blood_test['Total_calcium_mmol_L'],
            'Creatine Phosphokinase (CPK) (IU/L)': blood_test['Creatine_Phosphokinase_CPK_IU_L'],
            'Cholesterol (mg/dL)': blood_test['Cholesterol_mg_dL'],
            'Cholesterol (mmol/L)': blood_test['Cholesterol_mmol_L'],
            'Bicarbonate (mmol/L)': blood_test['Bicarbonate_mmol_L'],
            'Creatinine (mg/dL)': blood_test['Creatinine_mg_dL'],
            'Creatinine (umol/L)': blood_test['Creatinine_umol_L'],
            'Gamma glutamyl transferase (U/L)': blood_test['Gamma_glutamyl_transferase_U_L'],
            'Glucose, serum (mg/dL)': blood_test['Glucose_serum_mg_dL'],
            'Glucose, serum (mmol/L)': blood_test['Glucose_serum_mmol_L'],
            'Iron, refrigerated (ug/dL)': blood_test['Iron_refrigerated_ug_dL'],
            'Iron, refrigerated (umol/L)': blood_test['Iron_refrigerated_umol_L'],
            'Lactate Dehydrogenase (U/L)': blood_test['Lactate_dehydrogenase_U_L'],
            'Phosphorus (mg/dL)': blood_test['Phosphorus_mg_dL'],
            'Phosphorus (mmol/L)': blood_test['Phosphorus_mmol_L'],
            'Total bilirubin (mg/dL)': blood_test['Total_bilirubin_mg_dL'],
            'Total bilirubin (umol/L)': blood_test['Total_bilirubin_umol_L'],
            'Total protein (g/dL)': blood_test['Total_protein_g_dL'],
            'Total protein (g/L)': blood_test['Total_protein_g_L'],
            'Uric acid (mg/dL)': blood_test['Uric_acid_mg_dL'],
            'Uric acid (umol/L)': blood_test['Uric_acid_umol_L'],
            'Sodium (mmol/L)': blood_test['Sodium_mmol_L'],
            'Potassium (mmol/L)': blood_test['Potassium_mmol_L'],
            'Chloride (mmol/L)': blood_test['Chloride_mmol_L'],
            'Osmolality (mmol/Kg)': blood_test['Osmolality_mmol_Kg'],
            'Globulin (g/dL)': blood_test['Globulin_g_dL'],
            'Globulin (g/L)': blood_test['Globulin_g_L'],
            'Triglycerides (mg/dL)': blood_test['Triglycerides_mg_dL'],
            'Triglycerides (mmol/L)': blood_test['Triglycerides_mmol_L']
        })
    
    patient_age = get_patient_raw(patientID)[0]["AGE"]
    reference_ranges = get_blood_tests_references(patient_age)
            
    colored_blood_test_data = [color_mapping(blood_test, reference_ranges) for blood_test in formated_blood_tests]
    
    return jsonify(colored_blood_test_data)

@app2.route('/blood_tests_references/raw/<int:age>', methods=['GET'])
def get_blood_tests_references(age):
    if 20 <= age <= 39:
        reference_ranges = healthy_levels_young_adults
        
    elif 40 <= age < 65:
        reference_ranges = older_adults_reference_ranges
        
    elif age >= 65:
        reference_ranges = older_elderly_reference_ranges
    
    return reference_ranges

if __name__ == '__main__':
    app2.run(debug=True)
