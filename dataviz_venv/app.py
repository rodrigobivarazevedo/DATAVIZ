from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_tests.db'
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

   
    
    
    
# Sample raw data endpoint for patient data
@app.route('/<int:patientID>/raw')
def get_patient_raw_data(patientID):
    # Get patient information from the database
    patient = Patient.query.get_or_404(patientID)

    # Construct the data to be returned
    data = {
        'patientID': patient.ID,
        'first_name': patient.FIRST_NAME,
        'last_name': patient.LAST_NAME,
        'birth_date': str(patient.BIRTH_DATE),
        'gender': patient.GENDER,
    }

    return jsonify(data)

# Sample FHIR data endpoint for Patient data
@app.route('/<int:patientID>/fhir')
def get_patient_fhir_data(patientID):
    
    data = {
        'patientID': patient.ID,
        'first_name': patient.FIRST_NAME,
        'last_name': patient.LAST_NAME,
        'birth_date': str(patient.BIRTH_DATE),
        'gender': patient.GENDER,     
    }
    
    return transform_to_fhir_blood_test(patient_data)



# Sample FHIR data endpoint for blood test
@app.route('/<int:patientID>/<date:date>/fhir')
def get_blood_test_fhir_data(patientID):
    
    blood_test_data = {
        'ID': BloodIndicator.ID,
        'DATE': BloodIndicator.DATE,
        'Albumin (g/dL)': BloodIndicator.Albumin_g_dL,
        'Albumin (g/L)': BloodIndicator.Albumin_g_L,
        'Alanine aminotransferase ALT (U/L)': BloodIndicator.Alanine_aminotransferase_ALT_U_L,
        'Aspartate aminotransferase AST (U/L)': BloodIndicator.Aspartate_aminotransferase_AST_U_L,
        'Alkaline phosphatase (U/L)': BloodIndicator.Alkaline_phosphatase_U_L,
        'Blood urea nitrogen (mg/dL)': BloodIndicator.Blood_urea_nitrogen_mg_dL,
        'Blood urea nitrogen (mmol/L)': BloodIndicator.Blood_urea_nitrogen_mmol_L,
        'Total calcium (mg/dL)': BloodIndicator.Total_calcium_mg_dL,
        'Total calcium (mmol/L)': BloodIndicator.Total_calcium_mmol_L,
        'Creatine Phosphokinase (CPK) (IU/L)': BloodIndicator.Creatine_Phosphokinase_CPK_IU_L,
        'Cholesterol (mg/dL)': BloodIndicator.Cholesterol_mg_dL,
        'Cholesterol (mmol/L)': BloodIndicator.Cholesterol_mmol_L,
        'Bicarbonate (mmol/L)': BloodIndicator.Bicarbonate_mmol_L,
        'Creatinine (mg/dL)': BloodIndicator.Creatinine_mg_dL,
        'Creatinine (umol/L)': BloodIndicator.Creatinine_umol_L,
        'Gamma glutamyl transferase (U/L)': BloodIndicator.Gamma_glutamyl_transferase_U_L,
        'Glucose, serum (mg/dL)': BloodIndicator.Glucose_serum_mg_dL,
        'Glucose, serum (mmol/L)': BloodIndicator.Glucose_serum_mmol_L,
        'Iron, refrigerated (ug/dL)': BloodIndicator.Iron_refrigerated_ug_dL,
        'Iron, refrigerated (umol/L)': BloodIndicator.Iron_refrigerated_umol_L,
        'Lactate Dehydrogenase (U/L)': BloodIndicator.Lactate_dehydrogenase_U_L,
        'Phosphorus (mg/dL)': BloodIndicator.Phosphorus_mg_dL,
        'Phosphorus (mmol/L)': BloodIndicator.Phosphorus_mmol_L,
        'Total bilirubin (mg/dL)': BloodIndicator.Total_bilirubin_mg_dL,
        'Total bilirubin (umol/L)': BloodIndicator.Total_bilirubin_umol_L,
        'Total protein (g/dL)': BloodIndicator.Total_protein_g_dL,
        'Total protein (g/L)': BloodIndicator.Total_protein_g_L,
        'Uric acid (mg/dL)': BloodIndicator.Uric_acid_mg_dL,
        'Uric acid (umol/L)': BloodIndicator.Uric_acid_umol_L,
        'Sodium (mmol/L)': BloodIndicator.Sodium_mmol_L,
        'Potassium (mmol/L)': BloodIndicator.Potassium_mmol_L,
        'Chloride (mmol/L)': BloodIndicator.Chloride_mmol_L,
        'Osmolality (mmol/Kg)': BloodIndicator.Osmolality_mmol_Kg,
        'Globulin (g/dL)': BloodIndicator.Globulin_g_dL,
        'Globulin (g/L)': BloodIndicator.Globulin_g_L,
        'Triglycerides (mg/dL)': BloodIndicator.Triglycerides_mg_dL,
        'Triglycerides (mmol/L)': BloodIndicator.Triglycerides_mmol_L
}

    return transform_to_fhir_blood_test(blood_test_data)

# base_url}/blood_tests/{patient_id}?date={date_param}
# Sample FHIR data endpoint for blood test
@app.route('/blood_tests/<int:patientID>', methods=['GET'])
def get_blood_tests(patientID):
    # Get the date parameter from the request, default to None if not provided
    date_param = request.args.get('date', None)

    # Query based on ID and optionally DATE
    if date_param:
        date_value = datetime.strptime(date_param, "%Y-%m-%d").date()
        blood_tests = BloodIndicator.query.filter_by(ID=patientID, DATE=date_value).all()
    else:
        blood_tests = BloodIndicator.query.filter_by(ID=patientID).all()

    
    blood_test_data = [
    {
        'ID': BloodIndicator.ID,
        'DATE': BloodIndicator.DATE,
        'Albumin (g/dL)': BloodIndicator.Albumin_g_dL,
        'Albumin (g/L)': BloodIndicator.Albumin_g_L,
        'Alanine aminotransferase ALT (U/L)': BloodIndicator.Alanine_aminotransferase_ALT_U_L,
        'Aspartate aminotransferase AST (U/L)': BloodIndicator.Aspartate_aminotransferase_AST_U_L,
        'Alkaline phosphatase (U/L)': BloodIndicator.Alkaline_phosphatase_U_L,
        'Blood urea nitrogen (mg/dL)': BloodIndicator.Blood_urea_nitrogen_mg_dL,
        'Blood urea nitrogen (mmol/L)': BloodIndicator.Blood_urea_nitrogen_mmol_L,
        'Total calcium (mg/dL)': BloodIndicator.Total_calcium_mg_dL,
        'Total calcium (mmol/L)': BloodIndicator.Total_calcium_mmol_L,
        'Creatine Phosphokinase (CPK) (IU/L)': BloodIndicator.Creatine_Phosphokinase_CPK_IU_L,
        'Cholesterol (mg/dL)': BloodIndicator.Cholesterol_mg_dL,
        'Cholesterol (mmol/L)': BloodIndicator.Cholesterol_mmol_L,
        'Bicarbonate (mmol/L)': BloodIndicator.Bicarbonate_mmol_L,
        'Creatinine (mg/dL)': BloodIndicator.Creatinine_mg_dL,
        'Creatinine (umol/L)': BloodIndicator.Creatinine_umol_L,
        'Gamma glutamyl transferase (U/L)': BloodIndicator.Gamma_glutamyl_transferase_U_L,
        'Glucose, serum (mg/dL)': BloodIndicator.Glucose_serum_mg_dL,
        'Glucose, serum (mmol/L)': BloodIndicator.Glucose_serum_mmol_L,
        'Iron, refrigerated (ug/dL)': BloodIndicator.Iron_refrigerated_ug_dL,
        'Iron, refrigerated (umol/L)': BloodIndicator.Iron_refrigerated_umol_L,
        'Lactate Dehydrogenase (U/L)': BloodIndicator.Lactate_dehydrogenase_U_L,
        'Phosphorus (mg/dL)': BloodIndicator.Phosphorus_mg_dL,
        'Phosphorus (mmol/L)': BloodIndicator.Phosphorus_mmol_L,
        'Total bilirubin (mg/dL)': BloodIndicator.Total_bilirubin_mg_dL,
        'Total bilirubin (umol/L)': BloodIndicator.Total_bilirubin_umol_L,
        'Total protein (g/dL)': BloodIndicator.Total_protein_g_dL,
        'Total protein (g/L)': BloodIndicator.Total_protein_g_L,
        'Uric acid (mg/dL)': BloodIndicator.Uric_acid_mg_dL,
        'Uric acid (umol/L)': BloodIndicator.Uric_acid_umol_L,
        'Sodium (mmol/L)': BloodIndicator.Sodium_mmol_L,
        'Potassium (mmol/L)': BloodIndicator.Potassium_mmol_L,
        'Chloride (mmol/L)': BloodIndicator.Chloride_mmol_L,
        'Osmolality (mmol/Kg)': BloodIndicator.Osmolality_mmol_Kg,
        'Globulin (g/dL)': BloodIndicator.Globulin_g_dL,
        'Globulin (g/L)': BloodIndicator.Globulin_g_L,
        'Triglycerides (mg/dL)': BloodIndicator.Triglycerides_mg_dL,
        'Triglycerides (mmol/L)': BloodIndicator.Triglycerides_mmol_L
        }
    for blood_test in blood_tests
    ]

    return jsonify(blood_test_data)






    

def transform_to_fhir_blood_test(data, patient_reference="Patient/12345"):
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
            "reference": patient_reference
        },
        "effectiveDateTime": datetime.now().isoformat(),
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

    return json.dumps(fhir_observation, indent=2)




def patient_to_fhir(patient):
    # Create a FHIR Patient resource
    fhir_patient = {
        "resourceType": "Patient",
        "id": str(patient.ID),
        "name": [
            {
                "given": [patient.FIRST_NAME],
                "family": patient.LAST_NAME,
            }
        ],
        "birthDate": str(patient.BIRTH_DATE),
        "gender": patient.GENDER,
        # Add more attributes as needed
    }

    return jsonify(fhir_data)

if __name__ == '__main__':
    app.run(debug=True)
