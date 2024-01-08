from flask import Flask, request, jsonify, render_template, url_for
from datetime import datetime
import requests
from cs50 import SQL
from healthy_levels import healthy_levels_young_adults, older_adults_reference_ranges, older_elderly_reference_ranges
from blood_functions import color_mapping, transform_to_fhir_blood_test
from summary_stats import summary_stats
from fhir.resources.bundle import Bundle
import json
import traceback
from apiflask import APIFlask
import os

app = APIFlask(__name__, title="Blood Visualization app", version="2.0")


# Get the base directory of the application
base_dir = os.path.abspath(os.path.dirname(__file__))

# Construct the path to the database file (assuming db is outside the app folder)
db_path = os.path.join(base_dir, "..", "db", "blood_tests.db")

# Initialize the SQL object with the correct path
db = SQL(f"sqlite:///{db_path}")

@app.route("/fhir")
def fhir():
    return render_template("fhir.html") 

@app.route('/process_cmp', methods=['POST'])
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
                effective_date = entry.resource.effectiveDateTime  # Extract effective date
                # Store blood indicator and value in the dictionary
                blood_results[code_display] = {"value": value_quantity, "unit": unit}
        
        return jsonify(blood_results), 200

    except KeyError as ke:
        return jsonify({"error": f"KeyError: {str(ke)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


   
@app.route('/fhir_bundle', methods=['POST'])
def process_fhir_bundle():
    try:
        # Get the FHIR Bundle from the request
        fhir_bundle = Bundle.parse_obj(request.json)

        # Initialize dictionaries to store patient and blood results
        patient_info = {}
        blood_results = {}

        # Iterate through entries in the Bundle
         # Iterate through entries in the Bundle
        for entry in fhir_bundle.entry:
            if entry.resource.resource_type == "Observation":
                # Extract blood indicator and value from Observation
                code_display = entry.resource.code.text
                value_quantity = float(entry.resource.valueQuantity.value)  # Convert Decimal to float
                unit = entry.resource.valueQuantity.unit
                effective_date = entry.resource.effectiveDateTime  # Extract effective date
                # Store blood indicator and value in the dictionary
                blood_results[code_display] = {"value": value_quantity, "unit": unit, "effective_date": effective_date.strftime('%Y-%m-%d')}

          
            elif entry.resource.resource_type == "Patient":
                # Extract patient information
                patient = entry.resource
                first_name = patient.name[0].given[0] if patient.name and patient.name[0].given else ""
                last_name = patient.name[0].family if patient.name and patient.name[0].family else ""
                gender = patient.gender
                birth_date = patient.birthDate

                # Store patient information in the dictionary
                patient_info["first_name"] = first_name
                patient_info["last_name"] = last_name
                patient_info['birthDate'] = birth_date.strftime('%Y-%m-%d')
                patient_info['gender'] = gender
                
        if patient_info and blood_results:
            # Check if the patient exists in the database
            selected_patient = db.execute("""
                SELECT * FROM patients_new
                WHERE FIRST_NAME = ? AND LAST_NAME = ? AND BIRTH_DATE = ? AND GENDER = ?
            """, patient_info["first_name"], patient_info["last_name"], patient_info['birthDate'], patient_info['gender'])

        
            if not selected_patient:
                # Insert patient information into the 'patients' table
                db.execute("INSERT INTO patients_new (FIRST_NAME, LAST_NAME, BIRTH_DATE, GENDER) VALUES (?, ?, ?, ?)",
                        patient_info["first_name"], patient_info["last_name"], patient_info['birthDate'], patient_info['gender'])
                patient_id = db.execute("SELECT last_insert_rowid()")[0]['last_insert_rowid()']   
                existing_data = ""    
            
            else: 
                patient_id = selected_patient[0]['ID']

                # Check if blood results for the same patient and effective date already exist
                existing_data = db.execute("""
                    SELECT * FROM blood_indicators
                    WHERE ID = ? AND DATE = ?
                """, patient_id, blood_results['Albumin']['effective_date'])

            if not existing_data:
                # Insert blood test results into the 'blood_indicators' table
                db.execute("""
                            INSERT INTO blood_indicators (
                            ID, 
                            DATE, 
                            Albumin_g_dL,  
                            Alanine_aminotransferase_ALT_U_L, 
                            Aspartate_aminotransferase_AST_U_L, 
                            Alkaline_phosphatase_U_L, 
                            Blood_urea_nitrogen_mg_dL,  
                            Total_calcium_mg_dL, 
                            Creatine_Phosphokinase_CPK_IU_L, 
                            Cholesterol_mg_dL, 
                            Bicarbonate_mmol_L, 
                            Creatinine_mg_dL, 
                            Gamma_glutamyl_transferase_U_L, 
                            Glucose_serum_mg_dL,  
                            Iron_refrigerated_ug_dL,  
                            Lactate_dehydrogenase_U_L, 
                            Phosphorus_mg_dL, 
                            Total_bilirubin_mg_dL, 
                            Total_protein_g_dL, 
                            Uric_acid_mg_dL,  
                            Sodium_mmol_L, 
                            Potassium_mmol_L, 
                            Chloride_mmol_L, 
                            Osmolality_mmol_Kg, 
                            Globulin_g_dL, 
                            Triglycerides_mg_dL
                            ) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            patient_id, 
                            blood_results['Albumin']['effective_date'],
                            blood_results['Albumin']["value"],
                            blood_results['Alanine aminotransferase ALT']["value"],
                            blood_results['Aspartate aminotransferase AST']["value"],
                            blood_results['Alkaline phosphatase']["value"],
                            blood_results['Blood urea nitrogen']["value"], 
                            blood_results['Total calcium']["value"], 
                            blood_results['Creatine Phosphokinase (CPK)']["value"], 
                            blood_results['Cholesterol']["value"],
                            blood_results['Bicarbonate']["value"],
                            blood_results['Creatinine']["value"],
                            blood_results['Gamma glutamyl transferase']["value"], 
                            blood_results['Glucose, serum']["value"],
                            blood_results['Iron, refrigerated']["value"],
                            blood_results['Lactate Dehydrogenase']["value"],
                            blood_results['Phosphorus']["value"], 
                            blood_results['Total bilirubin']["value"], 
                            blood_results['Total protein']["value"],
                            blood_results['Uric acid']["value"], 
                            blood_results['Sodium']["value"], 
                            blood_results['Potassium']["value"],
                            blood_results['Chloride']["value"], 
                            blood_results['Osmolality']["value"],
                            blood_results['Globulin']["value"], 
                            blood_results['Triglycerides']["value"])
                    

                return jsonify({"message": "Data stored successfully","patient_id": patient_id, "patient_info": patient_info, "blood_results": blood_results}), 200
            else:
                return jsonify({"message": "Blood results for this patient and date already exist", "patient_id": patient_id, "patient_info": patient_info, "blood_results": existing_data}), 400
        else:
            return jsonify({"message": "problems receiving data"}), 500
    except Exception as e:
        
        traceback_str = traceback.format_exc()
        return jsonify({"error": str(e), "traceback": traceback_str}), 500
    
 
    
@app.route("/")
def patient_data():
    return render_template("views2.html")  
   
# Sample raw data endpoint for patient data
@app.route('/<int:patientID>/raw', methods=["POST"])
def get_patient_raw(patientID):
    # Get patient information from the database
    patient_data = db.execute("SELECT * FROM patients_new WHERE ID = ?", patientID)
    # date_of_birth is in the format 'YYYY-MM-DD'
    birth_date = datetime.strptime(patient_data[0]["BIRTH_DATE"], '%Y-%m-%d')
    current_date = datetime.now()
    
    # Calculate the difference in years
    age = current_date.year - birth_date.year - ((current_date.month, current_date.day) < (birth_date.month, birth_date.day))
    # Add the "AGE" key to the dictionary
    patient_data[0]["AGE"] = age
    return patient_data 

# Sample FHIR data endpoint for Patient data
@app.route('/<int:patientID>/fhir', methods=["GET"])
def get_patient_fhir(patientID):
    
    patient_data = db.execute("SELECT * FROM patients_new WHERE ID = ?", patientID)
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



@app.route('/blood_tests/fhir/<int:patientID>', methods=['GET'])
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

@app.route("/blood_dates")
def dates():
    q = request.args.get("q")
    if q:
        dates = db.execute("SELECT DATE FROM blood_indicators WHERE ID = ?", q)
    else:
        dates = []
    return dates
    
        
# base_url}/blood_tests/{patient_id}?date={date_param}
# Sample FHIR data endpoint for blood test
@app.route('/blood_tests/raw/<int:patientID>', methods=['GET'])
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

@app.route('/blood_tests_references/raw/<int:patientID>', methods=['GET'])
def get_blood_tests_references(patientID):
    
    patient_age = get_patient_raw(patientID)[0]["AGE"]
    
    if 20 <= patient_age <= 39:
        reference_ranges = healthy_levels_young_adults
        
    elif 40 <= patient_age < 65:
        reference_ranges = older_adults_reference_ranges
        
    elif patient_age >= 65:
        reference_ranges = older_elderly_reference_ranges
    
    return reference_ranges


@app.route('/all_blood_tests/raw/<int:patientID>', methods=['GET'])
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

@app.route('/statistics/<string:blood_indicator>', methods=['GET'])
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
    app.run(debug=True)
