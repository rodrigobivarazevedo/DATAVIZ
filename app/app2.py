from flask import Flask, request, jsonify, render_template, url_for
from datetime import datetime
import requests
from cs50 import SQL
from healthy_levels import healthy_levels_young_adults, older_adults_reference_ranges, older_elderly_reference_ranges
from blood_functions import color_mapping, transform_to_fhir_blood_test
from summary_stats import summary_stats
from fhir.resources.bundle import Bundle
import json

app2 = Flask(__name__)
db = SQL("sqlite:////home/rodrigo/repos/DATAVIZ_project/db/blood_tests.db")


@app2.route("/fhir")
def fhir():
    return render_template("fhir.html") 

@app2.route('/process_cmp', methods=['POST'])
def process_cmp():
    try:
        # Ensure the 'Content-Type' header is set to 'application/json'
        if request.headers['Content-Type'] != 'application/json':
            return jsonify({"error": "Invalid Content-Type. Please use 'application/json'"}), 400
        json_bundle = json.dumps(request.json)
        # Get the FHIR Bundle from the request
        fhir_bundle = Bundle.parse_raw(json_bundle)

        # Initialize a dictionary to store blood indicators and values
        blood_results = {}

        # Iterate through entries in the Bundle
        for entry in fhir_bundle.entry:
            if entry.resource.resource_type == "Observation":
                # Extract blood indicator and value from Observation
                code_display = entry.resource.code.text
                value_quantity = float(entry.resource.valueQuantity.value)  # Convert Decimal to float
                unit = entry.resource.valueQuantity.unit

                # Store blood indicator and value in the dictionary
                blood_results[code_display] = {"value": value_quantity, "unit": unit}
        
        return jsonify(blood_results), 200

    except KeyError as ke:
        return jsonify({"error": f"KeyError: {str(ke)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


   
@app2.route('/fhir_bundle', methods=['POST'])
def process_fhir_bundle():
    try:
        # Get the FHIR Bundle from the request
        fhir_bundle = Bundle(request.json)

        # Initialize dictionaries to store patient and blood results
        patient_info = {}
        blood_results = {}

        # Iterate through entries in the Bundle
        for entry in fhir_bundle.entry:
            if entry.resource.resource_type == "Observation":
                # Extract blood indicator, value, and unit from Observation
                code_display = entry.resource.code.text
                value_quantity = entry.resource.valueQuantity.value
                unit = entry.resource.valueQuantity.unit

                # Store blood indicator, value, and unit in the dictionary
                blood_results[code_display] = {"value": value_quantity, "unit": unit}

            elif entry.resource.resource_type == "Patient":
                # Extract patient information
                patient_name = entry.resource.name[0].text if entry.resource.name else "Unknown"
                patient_id = entry.resource.id

                # Store patient information in the dictionary
                patient_info["name"] = patient_name
                patient_info["id"] = patient_id

        return jsonify({"patient_info": patient_info, "blood_results": blood_results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
# Route to handle incoming FHIR bundle
@app2.route('/api/receive_bundle', methods=['POST'])
def receive_bundle():
    try:
        data = request.get_json()
        bundle = Bundle.parse_obj(data)
        # Extract patient information
        patient_data = bundle.Patient
        name = bundle.name
        first_name = name.given
        last_name = name.family
        birth_date = patient_data['birthDate']
        gender = patient_data['gender']

        # Insert patient information into the 'patients' table
        db.execute("INSERT INTO patients (FIRST_NAME, LAST_NAME, BIRTH_DATE, GENDER) VALUES (?, ?, ?, ?)",
                   first_name, last_name, birth_date, gender)
        patient_id = db.execute("SELECT last_insert_rowid()")[0]['last_insert_rowid()']

        # Extract blood test results information
        blood_results_data = data['blood_results']

        # Insert blood test results into the 'blood_indicators' table
        db.execute("""
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
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    patient_id, blood_results_data['date'],
                    blood_results_data['Albumin_g_dL'], blood_results_data['Albumin_g_L'],
                    blood_results_data['Alanine_aminotransferase_ALT_U_L'],
                    blood_results_data['Aspartate_aminotransferase_AST_U_L'],
                    blood_results_data['Alkaline_phosphatase_U_L'],
                    blood_results_data['Blood_urea_nitrogen_mg_dL'], blood_results_data['Blood_urea_nitrogen_mmol_L'],
                    blood_results_data['Total_calcium_mg_dL'], blood_results_data['Total_calcium_mmol_L'],
                    blood_results_data['Creatine_Phosphokinase_CPK_IU_L'], blood_results_data['Cholesterol_mg_dL'],
                    blood_results_data['Cholesterol_mmol_L'], blood_results_data['Bicarbonate_mmol_L'],
                    blood_results_data['Creatinine_mg_dL'], blood_results_data['Creatinine_umol_L'],
                    blood_results_data['Gamma_glutamyl_transferase_U_L'], blood_results_data['Glucose_serum_mg_dL'],
                    blood_results_data['Glucose_serum_mmol_L'], blood_results_data['Iron_refrigerated_ug_dL'],
                    blood_results_data['Iron_refrigerated_umol_L'], blood_results_data['Lactate_dehydrogenase_U_L'],
                    blood_results_data['Phosphorus_mg_dL'], blood_results_data['Phosphorus_mmol_L'],
                    blood_results_data['Total_bilirubin_mg_dL'], blood_results_data['Total_bilirubin_umol_L'],
                    blood_results_data['Total_protein_g_dL'], blood_results_data['Total_protein_g_L'],
                    blood_results_data['Uric_acid_mg_dL'], blood_results_data['Uric_acid_umol_L'],
                    blood_results_data['Sodium_mmol_L'], blood_results_data['Potassium_mmol_L'],
                    blood_results_data['Chloride_mmol_L'], blood_results_data['Osmolality_mmol_Kg'],
                    blood_results_data['Globulin_g_dL'], blood_results_data['Globulin_g_L'],
                    blood_results_data['Triglycerides_mg_dL'], blood_results_data['Triglycerides_mmol_L'])

        return jsonify({"message": "Data stored successfully", "patient_id": patient_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


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
@app2.route('/<int:patientID>/fhir', methods=["GET"])
def get_patient_fhir(patientID):
    
    patient_data = db.execute("SELECT * FROM patients WHERE ID = ?", patientID)
    patient_data_dict = patient_data[0]
    fhir_patient = {
        "resourceType": "Patient",
        "id": patient_data_dict["ID"],
        "name": [
            {
                "given": patient_data_dict["FIRST_NAME"],
                "family": patient_data_dict["LAST_NAME"],
            }
        ],
        "birthDate": str(patient_data_dict["BIRTH_DATE"]),
        "gender": patient_data_dict["GENDER"]
        
    }

    # Convert to regular dictionary if needed
    return jsonify(fhir_patient)



@app2.route('/blood_tests/fhir/<int:patientID>', methods=['GET'])
def get_blood_tests_fhir(patientID):
    # Build the URL for the raw data endpoint
    raw_data_url = url_for('blood_tests_raw', patientID=patientID, _external=True)

    # Make a request to the raw data endpoint
    response = requests.get(raw_data_url)

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
            'Alanine aminotransferase ALT (U/L)': blood_test['Alanine_aminotransferase_ALT_U_L'],
            'Aspartate aminotransferase AST (U/L)': blood_test['Aspartate_aminotransferase_AST_U_L'],
            'Alkaline phosphatase (U/L)': blood_test['Alkaline_phosphatase_U_L'],
            'Blood urea nitrogen (mg/dL)': blood_test['Blood_urea_nitrogen_mg_dL'],
            'Total calcium (mg/dL)': blood_test['Total_calcium_mg_dL'],
            'Creatine Phosphokinase (CPK) (IU/L)': blood_test['Creatine_Phosphokinase_CPK_IU_L'],
            'Cholesterol (mg/dL)': blood_test['Cholesterol_mg_dL'],
            'Bicarbonate (mmol/L)': blood_test['Bicarbonate_mmol_L'],
            'Creatinine (mg/dL)': blood_test['Creatinine_mg_dL'],
            'Gamma glutamyl transferase (U/L)': blood_test['Gamma_glutamyl_transferase_U_L'],
            'Glucose, serum (mg/dL)': blood_test['Glucose_serum_mg_dL'],
            'Iron, refrigerated (ug/dL)': blood_test['Iron_refrigerated_ug_dL'],
            'Lactate Dehydrogenase (U/L)': blood_test['Lactate_dehydrogenase_U_L'],
            'Phosphorus (mg/dL)': blood_test['Phosphorus_mg_dL'],
            'Total bilirubin (mg/dL)': blood_test['Total_bilirubin_mg_dL'],
            'Total protein (g/dL)': blood_test['Total_protein_g_dL'],
            'Uric acid (mg/dL)': blood_test['Uric_acid_mg_dL'],
            'Sodium (mmol/L)': blood_test['Sodium_mmol_L'],
            'Potassium (mmol/L)': blood_test['Potassium_mmol_L'],
            'Chloride (mmol/L)': blood_test['Chloride_mmol_L'],
            'Osmolality (mmol/Kg)': blood_test['Osmolality_mmol_Kg'],
            'Globulin (g/dL)': blood_test['Globulin_g_dL'],
            'Triglycerides (mg/dL)': blood_test['Triglycerides_mg_dL']
        })
            
         

    reference_ranges = get_blood_tests_references(patientID)
            
    colored_blood_test_data = [color_mapping(blood_test, reference_ranges) for blood_test in formated_blood_tests]
    combined_dict = {}
    for key, values in colored_blood_test_data[0].items():
        if key in reference_ranges:
            combined_dict[key] = values + [reference_ranges[key]]
    
    return jsonify(combined_dict)

@app2.route('/blood_tests_references/raw/<int:patientID>', methods=['GET'])
def get_blood_tests_references(patientID):
    
    patient_age = get_patient_raw(patientID)[0]["AGE"]
    
    if 20 <= patient_age <= 39:
        reference_ranges = healthy_levels_young_adults
        
    elif 40 <= patient_age < 65:
        reference_ranges = older_adults_reference_ranges
        
    elif patient_age >= 65:
        reference_ranges = older_elderly_reference_ranges
    
    return reference_ranges


@app2.route('/all_blood_tests/raw/<int:patientID>', methods=['GET'])
def blood_tests_raw(patientID):
    date_param_str = request.args.get('date', None)

    if date_param_str is not None:
        # If date parameter is provided, retrieve blood tests for that specific date
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
            'Alanine aminotransferase ALT (U/L)': blood_test['Alanine_aminotransferase_ALT_U_L'],
            'Aspartate aminotransferase AST (U/L)': blood_test['Aspartate_aminotransferase_AST_U_L'],
            'Alkaline phosphatase (U/L)': blood_test['Alkaline_phosphatase_U_L'],
            'Blood urea nitrogen (mg/dL)': blood_test['Blood_urea_nitrogen_mg_dL'],
            'Total calcium (mg/dL)': blood_test['Total_calcium_mg_dL'],
            'Creatine Phosphokinase (CPK) (IU/L)': blood_test['Creatine_Phosphokinase_CPK_IU_L'],
            'Cholesterol (mg/dL)': blood_test['Cholesterol_mg_dL'],
            'Bicarbonate (mmol/L)': blood_test['Bicarbonate_mmol_L'],
            'Creatinine (mg/dL)': blood_test['Creatinine_mg_dL'],
            'Gamma glutamyl transferase (U/L)': blood_test['Gamma_glutamyl_transferase_U_L'],
            'Glucose, serum (mg/dL)': blood_test['Glucose_serum_mg_dL'],
            'Iron, refrigerated (ug/dL)': blood_test['Iron_refrigerated_ug_dL'],
            'Lactate Dehydrogenase (U/L)': blood_test['Lactate_dehydrogenase_U_L'],
            'Phosphorus (mg/dL)': blood_test['Phosphorus_mg_dL'],
            'Total bilirubin (mg/dL)': blood_test['Total_bilirubin_mg_dL'],
            'Total protein (g/dL)': blood_test['Total_protein_g_dL'],
            'Uric acid (mg/dL)': blood_test['Uric_acid_mg_dL'],
            'Sodium (mmol/L)': blood_test['Sodium_mmol_L'],
            'Potassium (mmol/L)': blood_test['Potassium_mmol_L'],
            'Chloride (mmol/L)': blood_test['Chloride_mmol_L'],
            'Osmolality (mmol/Kg)': blood_test['Osmolality_mmol_Kg'],
            'Globulin (g/dL)': blood_test['Globulin_g_dL'],
            'Triglycerides (mg/dL)': blood_test['Triglycerides_mg_dL']
        })

        reference_ranges = get_blood_tests_references(patientID)

        colored_blood_test_data = [color_mapping(blood_test, reference_ranges) for blood_test in formated_blood_tests]

        combined_dict = {}
        for key, values in colored_blood_test_data[0].items():
            if key in reference_ranges:
                combined_dict[key] = values + [reference_ranges[key]]

        return jsonify(combined_dict)
    else:
        # If no date parameter is provided, retrieve all available blood tests for that patient
        try:
            query_all = "SELECT * FROM blood_indicators WHERE ID = ?"
            values_all = (patientID,)
            blood_tests_all = db.execute(query_all, *values_all)
        
        except Exception as e:
            print("Error executing SQL query:", e)

        # Format all blood tests
        formatted_blood_tests_all = []
        for blood_test in blood_tests_all:
            formatted_blood_tests_all.append({
            'DATE' : blood_test['DATE'],
            'Albumin (g/dL)': blood_test['Albumin_g_dL'],
            'Alanine aminotransferase ALT (U/L)': blood_test['Alanine_aminotransferase_ALT_U_L'],
            'Aspartate aminotransferase AST (U/L)': blood_test['Aspartate_aminotransferase_AST_U_L'],
            'Alkaline phosphatase (U/L)': blood_test['Alkaline_phosphatase_U_L'],
            'Blood urea nitrogen (mg/dL)': blood_test['Blood_urea_nitrogen_mg_dL'],
            'Total calcium (mg/dL)': blood_test['Total_calcium_mg_dL'],
            'Creatine Phosphokinase (CPK) (IU/L)': blood_test['Creatine_Phosphokinase_CPK_IU_L'],
            'Cholesterol (mg/dL)': blood_test['Cholesterol_mg_dL'],
            'Bicarbonate (mmol/L)': blood_test['Bicarbonate_mmol_L'],
            'Creatinine (mg/dL)': blood_test['Creatinine_mg_dL'],
            'Gamma glutamyl transferase (U/L)': blood_test['Gamma_glutamyl_transferase_U_L'],
            'Glucose, serum (mg/dL)': blood_test['Glucose_serum_mg_dL'],
            'Iron, refrigerated (ug/dL)': blood_test['Iron_refrigerated_ug_dL'],
            'Lactate Dehydrogenase (U/L)': blood_test['Lactate_dehydrogenase_U_L'],
            'Phosphorus (mg/dL)': blood_test['Phosphorus_mg_dL'],
            'Total bilirubin (mg/dL)': blood_test['Total_bilirubin_mg_dL'],
            'Total protein (g/dL)': blood_test['Total_protein_g_dL'],
            'Uric acid (mg/dL)': blood_test['Uric_acid_mg_dL'],
            'Sodium (mmol/L)': blood_test['Sodium_mmol_L'],
            'Potassium (mmol/L)': blood_test['Potassium_mmol_L'],
            'Chloride (mmol/L)': blood_test['Chloride_mmol_L'],
            'Osmolality (mmol/Kg)': blood_test['Osmolality_mmol_Kg'],
            'Globulin (g/dL)': blood_test['Globulin_g_dL'],
            'Triglycerides (mg/dL)': blood_test['Triglycerides_mg_dL']
        })
            


        # Similar to the logic for a specific date, you can proceed with coloring, combining, etc.
        reference_ranges_all = get_blood_tests_references(patientID)
        colored_blood_test_data_all = [color_mapping(blood_test_all, reference_ranges_all) for blood_test_all in formatted_blood_tests_all]
        
        combined_dict_all = {}
        for key, values in colored_blood_test_data_all[0].items():
            if key in reference_ranges_all:
                combined_dict_all[key] = values + [reference_ranges_all[key]]
        
        return jsonify(colored_blood_test_data_all)

@app2.route('/statistics/<string:blood_indicator>', methods=['GET'])
def statistics(blood_indicator):
    
    # Check if the blood indicator is in the summary_stats dictionary
    if blood_indicator in summary_stats:
        # Retrieve the statistics for the given blood indicator
        blood_stats = summary_stats[blood_indicator]
        # Return the statistics as JSON
        return jsonify(blood_stats)
    else:
        # If the blood indicator is not found, return an error message
        return jsonify({"error": "Blood indicator not found"}), 404
    
    



if __name__ == '__main__':
    app2.run(debug=True)
