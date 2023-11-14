from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
import requests
from collections import OrderedDict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/rodrigo/repos/DATAVIZ_project/dataviz_venv/db/blood_tests.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    __tablename__ = 'patients'
    ID = db.Column(db.Integer, primary_key=True)
    FIRST_NAME = db.Column(db.String(50))
    LAST_NAME = db.Column(db.String(50))
    BIRTH_DATE = db.Column(db.Date)
    GENDER = db.Column(db.String(10))
    
    
class BloodIndicator(db.Model):
    __tablename__ = 'blood_indicators'
    ID = db.Column(db.Integer, primary_key=True)
    DATE = db.Column(db.Date)
    Albumin_g_dL = db.Column(db.Integer)
    Albumin_g_L = db.Column(db.Integer)
    Alanine_aminotransferase_ALT_U_L = db.Column(db.Integer)
    Aspartate_aminotransferase_AST_U_L = db.Column(db.Integer)
    Alkaline_phosphatase_U_L = db.Column(db.Integer)
    Blood_urea_nitrogen_mg_dL = db.Column(db.Integer)
    Blood_urea_nitrogen_mmol_L = db.Column(db.Integer)
    Total_calcium_mg_dL = db.Column(db.Integer)
    Total_calcium_mmol_L = db.Column(db.Integer)
    Creatine_Phosphokinase_CPK_IU_L = db.Column(db.Integer)
    Cholesterol_mg_dL = db.Column(db.Integer)
    Cholesterol_mmol_L = db.Column(db.Integer)
    Bicarbonate_mmol_L = db.Column(db.Integer)
    Creatinine_mg_dL = db.Column(db.Integer)
    Creatinine_umol_L = db.Column(db.Integer)
    Gamma_glutamyl_transferase_U_L = db.Column(db.Integer)
    Glucose_serum_mg_dL = db.Column(db.Integer)
    Glucose_serum_mmol_L = db.Column(db.Integer)
    Iron_refrigerated_ug_dL = db.Column(db.Integer)
    Iron_refrigerated_umol_L = db.Column(db.Integer)
    Lactate_dehydrogenase_U_L = db.Column(db.Integer)
    Phosphorus_mg_dL = db.Column(db.Integer)
    Phosphorus_mmol_L = db.Column(db.Integer)
    Total_bilirubin_mg_dL = db.Column(db.Integer)
    Total_bilirubin_umol_L = db.Column(db.Integer)
    Total_protein_g_dL = db.Column(db.Integer)
    Total_protein_g_L = db.Column(db.Integer)
    Uric_acid_mg_dL = db.Column(db.Integer)
    Uric_acid_umol_L = db.Column(db.Integer)
    Sodium_mmol_L = db.Column(db.Integer)
    Potassium_mmol_L = db.Column(db.Integer)
    Chloride_mmol_L = db.Column(db.Integer)
    Osmolality_mmol_Kg = db.Column(db.Integer)
    Globulin_g_dL = db.Column(db.Integer)
    Globulin_g_L = db.Column(db.Integer)
    Triglycerides_mg_dL = db.Column(db.Integer)
    Triglycerides_mmol_L = db.Column(db.Integer)

# Healthy levels for young adults (age 20-39 years) - Reference ranges are approximate and may vary.
healthy_levels_young_adults = {
    "Albumin (g/dL)": {"min": 3.4, "max": 5.4},
    "Albumin (g/L)": {"min": 34, "max": 54},
    "Alanine aminotransferase ALT (U/L)": {"min": 5, "max": 40},
    "Aspartate aminotransferase AST (U/L)": {"min": 8, "max": 48},
    "Alkaline phosphatase (U/L)": {"min": 20, "max": 140},
    "Blood urea nitrogen (mg/dL)": {"min": 8, "max": 25},
    "Blood urea nitrogen (mmol/L)": {"min": 2.9, "max": 8.9},
    "Total calcium (mg/dL)": {"min": 8.6, "max": 10.4},
    "Total calcium (mmol/L)": {"min": 2.1, "max": 2.6},
    "Creatine Phosphokinase (CPK) (IU/L)": {"min": 38, "max": 308},
    "Cholesterol (mg/dL)": {"min": 125, "max": 200},
    "Cholesterol (mmol/L)": {"min": 3.24, "max": 5.18},
    "Bicarbonate (mmol/L)": {"min": 21, "max": 31},
    "Creatinine (mg/dL)": {"min": 0.7, "max": 1.3},
    "Creatinine (umol/L)": {"min": 61.9, "max": 115},
    "Gamma glutamyl transferase (U/L)": {"min": 5, "max": 85},
    "Glucose, serum (mg/dL)": {"min": 70, "max": 100},
    "Glucose, serum (mmol/L)": {"min": 3.9, "max": 5.6},
    "Iron, refrigerated (ug/dL)": {"min": 35, "max": 169},
    "Iron, refrigerated (umol/L)": {"min": 6.26, "max": 30.29},
    "Potassium (mmol/L)": {"min": 3.5, "max": 5.1},  
    "Phosphorus (mg/dL)": {"min": 2.5, "max": 4.9},
    "Phosphorus (mmol/L)": {"min": 0.81, "max": 1.58},  # Calculated from mg/dL
    "Total bilirubin (mg/dL)": {"min": 0.2, "max": 1.2},
    "Total bilirubin (umol/L)": {"min": 3.42, "max": 20.51},
    "Total protein (g/dL)": {"min": 6.6, "max": 8.3},
    "Total protein (g/L)": {"min": 66, "max": 83},
    "Uric acid (mg/dL)": {"min": 2.4, "max": 7.2},
    "Uric acid (umol/L)": {"min": 142, "max": 428},
    "Sodium (mmol/L)": {"min": 135, "max": 146},
    "Lactate Dehydrogenase (U/L)": {"min": 140, "max": 280},  
    "Chloride (mmol/L)": {"min": 96, "max": 106},
    "Osmolality (mmol/Kg)": {"min": 275, "max": 295},
    "Globulin (g/dL)": {"min": 2.3, "max": 3.5},  
    "Globulin (g/L)": {"min": 23, "max": 35},  
    "Triglycerides (mg/dL)": {"min": 30, "max": 150},
    "Triglycerides (mmol/L)": {"min": 0.34, "max": 1.69},
}

# fucntion to get the color correspondent to the blood indicator level
def get_blood_level_color(indicator_name, level, reference_ranges):
    if indicator_name in reference_ranges:
        reference = reference_ranges[indicator_name]
        min_range = reference.get("min")
        max_range = reference.get("max")

        if min_range is not None and max_range is not None:
            if level < min_range or level > max_range:
                return "red"
            elif abs(level - min_range) <= 0.2 * (max_range - min_range) or abs(level - max_range) <= 0.2 * (
                    max_range - min_range):
                return "yellow"
            else:
                return "green"
        else:
            return "Unknown reference range"
    else:
        return "Indicator not found in the reference"

# fucntion to update the dict adding the correspondent color as a key value next to the blood level
def color_mapping(indicators_data, reference_ranges):
    colored_indicators = {}

    for indicator_name, level in indicators_data.items():
        colored_indicators[indicator_name] = [level, get_blood_level_color(indicator_name, level, reference_ranges)]
    return colored_indicators

# fucntion to tranform into FHIR format
def transform_to_fhir_blood_test(data, patient_reference):
    
    fhir_observation = {
        "resourceType": "Observation",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "laboratory",
                        "display": "Laboratory"
                    }
                ],
                "text": "Laboratory"
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "24357-5",
                    "display": "Blood Panel"
                }
            ],
            "text": "Blood Panel"
        },
        "subject": {
            "reference": f"Patient/{patient_reference}"
        },
        
        "component": []
    }

    for test_name, (result_value, color) in data.items():
        unit, unit_code = determine_unit_and_code(test_name)
        interpretation_code = determine_interpretation_code(color)
        component = {
            "code": {
                "text": test_name
            },
            "valueQuantity": {
                "value": result_value,
                "unit": unit,
                "system": "http://unitsofmeasure.org",
                "code": unit_code
            },
            "interpretation": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                        "code": interpretation_code,
                        "display": interpretation_code.capitalize()
                    }
                ]
            }
        }
        fhir_observation["component"].append(component)
        
    # Convert the dictionary to an OrderedDict
    return fhir_observation

    


    

def determine_unit_and_code(test_name):
    # Add logic to determine the unit and unit code based on the test name
    # You might need more sophisticated logic or external reference data
    if "mg/dL" in test_name:
        return "mg/dL", "mg/dL"
    elif "g/dL" in test_name:
        return "g/dL", "g/dL"
    elif "U/L" in test_name:
        return "U/L", "U/L"
    elif "mmol/L" in test_name:
        return "mmol/L", "mmol/L"
    elif "ug/dL" in test_name:
        return "ug/dL", "ug/dL"
    elif "umol/L" in test_name:
        return "umol/L", "umol/L"
    else:
        return "unknown", "unknown"

def determine_interpretation_code(color):
    # Map color to interpretation code based on the provided mapping
    if color.lower() == "green":
        return "N"  # Normal range
    elif color.lower() == "yellow":
        return "R"  # Medium range
    elif color.lower() == "red":
        return "H"  # Extreme range
    else:
        return "unknown"
     
    

@app.route("/")
def patient_data():
    return render_template("index.html")  

@app.route("/views")
def visualization():
    return render_template("views.html") 
    
# Sample raw data endpoint for patient data
@app.route('/<int:patientID>/raw', methods=['GET'])
def get_patient_raw(patientID):
    # Get patient information from the database
    patient = Patient.query.get_or_404(patientID)

    # Construct the data to be returned
    patient_data = {
        'patientID': patient.ID,
        'first_name': patient.FIRST_NAME,
        'last_name': patient.LAST_NAME,
        'birth_date': str(patient.BIRTH_DATE),
        'gender': patient.GENDER,
    }

    return jsonify(patient_data)


# Sample FHIR data endpoint for Patient data
@app.route('/<int:patientID>/fhir', methods=['GET'])
def get_patient_fhir(patientID):
    
    patient = Patient.query.get_or_404(patientID)
    
    fhir_patient = {
        "resourceType": "Patient",
        "id": patient.ID,
        "name": [
            {
                "given": [patient.FIRST_NAME],
                "family": patient.LAST_NAME,
            }
        ],
        "birthDate": str(patient.BIRTH_DATE),
        "gender": patient.GENDER,
        
    }

    # Convert to regular dictionary if needed
    return jsonify(fhir_patient)



@app.route('/blood_tests/fhir/<int:patientID>', methods=['GET'])
def get_blood_tests_fhir(patientID):
    
    # Process blood_tests as needed and return the raw data with colors
    colored_blood_test_data = get_blood_tests_raw_data(patientID)
    
    # Transform each blood test data to FHIR format
    return jsonify([transform_to_fhir_blood_test(blood_test, patientID) for blood_test in colored_blood_test_data])


        
   


# base_url}/blood_tests/{patient_id}?date={date_param}
# Sample FHIR data endpoint for blood test
@app.route('/blood_tests/raw/<int:patientID>', methods=['GET'])
def get_blood_tests_raw(patientID):
    return get_blood_tests_raw_data(patientID)
    

    







def get_blood_tests_raw_data(patientID):
    # Get the date parameter from the request, default to None if not provided
    date_param = request.args.get('date', None)

    # Query based on ID and optionally DATE
    if date_param:
        date_value = datetime.strptime(date_param, "%Y-%m-%d").date()
        blood_tests = BloodIndicator.query.filter(BloodIndicator.ID == patientID, BloodIndicator.DATE == date_value).all()
    else:
        blood_tests = BloodIndicator.query.filter(BloodIndicator.ID == patientID).all()
        
    blood_test_data = []
    for blood_test in blood_tests:
        blood_test_data.append({
            'Albumin (g/dL)': blood_test.Albumin_g_dL,
            'Albumin (g/L)': blood_test.Albumin_g_L,
            'Alanine aminotransferase ALT (U/L)': blood_test.Alanine_aminotransferase_ALT_U_L,
            'Aspartate aminotransferase AST (U/L)': blood_test.Aspartate_aminotransferase_AST_U_L,
            'Alkaline phosphatase (U/L)': blood_test.Alkaline_phosphatase_U_L,
            'Blood urea nitrogen (mg/dL)': blood_test.Blood_urea_nitrogen_mg_dL,
            'Blood urea nitrogen (mmol/L)': blood_test.Blood_urea_nitrogen_mmol_L,
            'Total calcium (mg/dL)': blood_test.Total_calcium_mg_dL,
            'Total calcium (mmol/L)': blood_test.Total_calcium_mmol_L,
            'Creatine Phosphokinase (CPK) (IU/L)': blood_test.Creatine_Phosphokinase_CPK_IU_L,
            'Cholesterol (mg/dL)': blood_test.Cholesterol_mg_dL,
            'Cholesterol (mmol/L)': blood_test.Cholesterol_mmol_L,
            'Bicarbonate (mmol/L)': blood_test.Bicarbonate_mmol_L,
            'Creatinine (mg/dL)': blood_test.Creatinine_mg_dL,
            'Creatinine (umol/L)': blood_test.Creatinine_umol_L,
            'Gamma glutamyl transferase (U/L)': blood_test.Gamma_glutamyl_transferase_U_L,
            'Glucose, serum (mg/dL)': blood_test.Glucose_serum_mg_dL,
            'Glucose, serum (mmol/L)': blood_test.Glucose_serum_mmol_L,
            'Iron, refrigerated (ug/dL)': blood_test.Iron_refrigerated_ug_dL,
            'Iron, refrigerated (umol/L)': blood_test.Iron_refrigerated_umol_L,
            'Lactate Dehydrogenase (U/L)': blood_test.Lactate_dehydrogenase_U_L,
            'Phosphorus (mg/dL)': blood_test.Phosphorus_mg_dL,
            'Phosphorus (mmol/L)': blood_test.Phosphorus_mmol_L,
            'Total bilirubin (mg/dL)': blood_test.Total_bilirubin_mg_dL,
            'Total bilirubin (umol/L)': blood_test.Total_bilirubin_umol_L,
            'Total protein (g/dL)': blood_test.Total_protein_g_dL,
            'Total protein (g/L)': blood_test.Total_protein_g_L,
            'Uric acid (mg/dL)': blood_test.Uric_acid_mg_dL,
            'Uric acid (umol/L)': blood_test.Uric_acid_umol_L,
            'Sodium (mmol/L)': blood_test.Sodium_mmol_L,
            'Potassium (mmol/L)': blood_test.Potassium_mmol_L,
            'Chloride (mmol/L)': blood_test.Chloride_mmol_L,
            'Osmolality (mmol/Kg)': blood_test.Osmolality_mmol_Kg,
            'Globulin (g/dL)': blood_test.Globulin_g_dL,
            'Globulin (g/L)': blood_test.Globulin_g_L,
            'Triglycerides (mg/dL)': blood_test.Triglycerides_mg_dL,
            'Triglycerides (mmol/L)': blood_test.Triglycerides_mmol_L
        })
        
    
    
    colored_blood_test_data = [color_mapping(blood_test, healthy_levels_young_adults) for blood_test in blood_test_data]

    return colored_blood_test_data



if __name__ == '__main__':
    app.run(debug=True)
