import requests
import json

# Your FHIR Bundle JSON data
cmp_fhir = {
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1742-6",
              "display": "Alanine aminotransferase ALT"
            }
          ],
          "text": "Alanine aminotransferase ALT"
        },
        "valueQuantity": {
          "value": 30,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1751-7",
              "display": "Albumin"
            }
          ],
          "text": "Albumin"
        },
        "valueQuantity": {
          "value": 4.2,
          "unit": "g/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "6768-6",
              "display": "Alkaline phosphatase"
            }
          ],
          "text": "Alkaline phosphatase"
        },
        "valueQuantity": {
          "value": 75,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1920-8",
              "display": "Aspartate aminotransferase AST"
            }
          ],
          "text": "Aspartate aminotransferase AST"
        },
        "valueQuantity": {
          "value": 25,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1963-8",
              "display": "Bicarbonate"
            }
          ],
          "text": "Bicarbonate"
        },
        "valueQuantity": {
          "value": 24,
          "unit": "mmol/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "3094-0",
              "display": "Blood urea nitrogen"
            }
          ],
          "text": "Blood urea nitrogen"
        },
        "valueQuantity": {
          "value": 15,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2069-3",
              "display": "Chloride"
            }
          ],
          "text": "Chloride"
        },
        "valueQuantity": {
          "value": 102,
          "unit": "mmol/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2093-3",
              "display": "Cholesterol"
            }
          ],
          "text": "Cholesterol"
        },
        "valueQuantity": {
          "value": 180,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2157-6",
              "display": "Creatine Phosphokinase (CPK)"
            }
          ],
          "text": "Creatine Phosphokinase (CPK)"
        },
        "valueQuantity": {
          "value": 100,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "38483-4",
              "display": "Creatinine"
            }
          ],
          "text": "Creatinine"
        },
        "valueQuantity": {
          "value": 0.9,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2276-4",
              "display": "Gamma glutamyl transferase"
            }
          ],
          "text": "Gamma glutamyl transferase"
        },
        "valueQuantity": {
          "value": 40,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "24575-8",
              "display": "Globulin"
            }
          ],
          "text": "Globulin"
        },
        "valueQuantity": {
          "value": 2.5,
          "unit": "g/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2339-0",
              "display": "Glucose, serum"
            }
          ],
          "text": "Glucose, serum"
        },
        "valueQuantity": {
          "value": 110,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "preliminary",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "25835-0",
              "display": "Iron, refrigerated"
            }
          ],
          "text": "Iron, refrigerated"
        },
        "valueQuantity": {
          "value": 90,
          "unit": "µg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2532-0",
              "display": "Lactate Dehydrogenase"
            }
          ],
          "text": "Lactate Dehydrogenase"
        },
        "valueQuantity": {
          "value": 200,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "preliminary",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "56838-1",
              "display": "Osmolality"
            }
          ],
          "text": "Osmolality"
        },
        "valueQuantity": {
          "value": 290,
          "unit": "mOsm/kg"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2836-2",
              "display": "Phosphorus"
            }
          ],
          "text": "Phosphorus"
        },
        "valueQuantity": {
          "value": 3.5,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2823-3",
              "display": "Potassium"
            }
          ],
          "text": "Potassium"
        },
        "valueQuantity": {
          "value": 4.0,
          "unit": "mmol/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2951-2",
              "display": "Sodium"
            }
          ],
          "text": "Sodium"
        },
        "valueQuantity": {
          "value": 138,
          "unit": "mmol/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1975-2",
              "display": "Total bilirubin"
            }
          ],
          "text": "Total bilirubin"
        },
        "valueQuantity": {
          "value": 1.0,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "preliminary",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2000-8",
              "display": "Total calcium"
            }
          ],
          "text": "Total calcium"
        },
        "valueQuantity": {
          "value": 9.5,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "preliminary",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2885-2",
              "display": "Total protein"
            }
          ],
          "text": "Total protein"
        },
        "valueQuantity": {
          "value": 7.0,
          "unit": "g/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2885-2",
              "display": "Total protein"
            }
          ],
          "text": "Total protein"
        },
        "valueQuantity": {
          "value": 7.0,
          "unit": "g/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2571-8",
              "display": "Triglycerides"
            }
          ],
          "text": "Triglycerides"
        },
        "valueQuantity": {
          "value": 150,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "3084-1",
              "display": "Uric acid"
            }
          ],
          "text": "Uric acid"
        },
        "valueQuantity": {
          "value": 6.0,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    }
  ]
}

  


# Flask endpoint URL
url = "http://127.0.0.1:5000/process_cmp"

# Make a POST request with JSON payload
response = requests.post(url, json=cmp_fhir)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Request was successful!")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)  # Print the response content for debugging



fhir_bundle = {
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "example",
        "text": {
          "status": "generated",
          "div": "<div xmlns=\"http://www.w3.org/1999/xhtml\">John Doe (MRN: 12345)</div>"
        },
        "identifier": [
          {
            "system": "http://example.org/fhir/sid/us-ssn",
            "value": "123-45-6789"
          }
        ],
        "active": "true",
        "name": [
          {
            "use": "official",
            "family": "Doe",
            "given": [
              "John"
            ]
          }
        ],
        "gender": "male",
        "birthDate": "1970-01-01",
        "address": [
          {
            "use": "home",
            "line": [
              "123 Main St"
            ],
            "city": "Anytown",
            "state": "CA",
            "postalCode": "12345"
          }
        ]
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1742-6",
              "display": "Alanine aminotransferase ALT"
            }
          ],
          "text": "Alanine aminotransferase ALT"
        },
        "valueQuantity": {
          "value": 30,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1751-7",
              "display": "Albumin"
            }
          ],
          "text": "Albumin"
        },
        "valueQuantity": {
          "value": 4.2,
          "unit": "g/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "6768-6",
              "display": "Alkaline phosphatase"
            }
          ],
          "text": "Alkaline phosphatase"
        },
        "valueQuantity": {
          "value": 75,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1920-8",
              "display": "Aspartate aminotransferase AST"
            }
          ],
          "text": "Aspartate aminotransferase AST"
        },
        "valueQuantity": {
          "value": 25,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1963-8",
              "display": "Bicarbonate"
            }
          ],
          "text": "Bicarbonate"
        },
        "valueQuantity": {
          "value": 24,
          "unit": "mmol/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "3094-0",
              "display": "Blood urea nitrogen"
            }
          ],
          "text": "Blood urea nitrogen"
        },
        "valueQuantity": {
          "value": 15,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2069-3",
              "display": "Chloride"
            }
          ],
          "text": "Chloride"
        },
        "valueQuantity": {
          "value": 102,
          "unit": "mmol/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2093-3",
              "display": "Cholesterol"
            }
          ],
          "text": "Cholesterol"
        },
        "valueQuantity": {
          "value": 180,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2157-6",
              "display": "Creatine Phosphokinase (CPK)"
            }
          ],
          "text": "Creatine Phosphokinase (CPK)"
        },
        "valueQuantity": {
          "value": 100,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "38483-4",
              "display": "Creatinine"
            }
          ],
          "text": "Creatinine"
        },
        "valueQuantity": {
          "value": 0.9,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2276-4",
              "display": "Gamma glutamyl transferase"
            }
          ],
          "text": "Gamma glutamyl transferase"
        },
        "valueQuantity": {
          "value": 40,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "24575-8",
              "display": "Globulin"
            }
          ],
          "text": "Globulin"
        },
        "valueQuantity": {
          "value": 2.5,
          "unit": "g/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2339-0",
              "display": "Glucose, serum"
            }
          ],
          "text": "Glucose, serum"
        },
        "valueQuantity": {
          "value": 110,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "preliminary",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "25835-0",
              "display": "Iron, refrigerated"
            }
          ],
          "text": "Iron, refrigerated"
        },
        "valueQuantity": {
          "value": 90,
          "unit": "µg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2532-0",
              "display": "Lactate Dehydrogenase"
            }
          ],
          "text": "Lactate Dehydrogenase"
        },
        "valueQuantity": {
          "value": 200,
          "unit": "U/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "preliminary",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "56838-1",
              "display": "Osmolality"
            }
          ],
          "text": "Osmolality"
        },
        "valueQuantity": {
          "value": 290,
          "unit": "mOsm/kg"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2836-2",
              "display": "Phosphorus"
            }
          ],
          "text": "Phosphorus"
        },
        "valueQuantity": {
          "value": 3.5,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2823-3",
              "display": "Potassium"
            }
          ],
          "text": "Potassium"
        },
        "valueQuantity": {
          "value": 4.0,
          "unit": "mmol/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2951-2",
              "display": "Sodium"
            }
          ],
          "text": "Sodium"
        },
        "valueQuantity": {
          "value": 138,
          "unit": "mmol/L"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "1975-2",
              "display": "Total bilirubin"
            }
          ],
          "text": "Total bilirubin"
        },
        "valueQuantity": {
          "value": 1.0,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "preliminary",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2000-8",
              "display": "Total calcium"
            }
          ],
          "text": "Total calcium"
        },
        "valueQuantity": {
          "value": 9.5,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "preliminary",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2885-2",
              "display": "Total protein"
            }
          ],
          "text": "Total protein"
        },
        "valueQuantity": {
          "value": 7.0,
          "unit": "g/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2885-2",
              "display": "Total protein"
            }
          ],
          "text": "Total protein"
        },
        "valueQuantity": {
          "value": 7.0,
          "unit": "g/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "2571-8",
              "display": "Triglycerides"
            }
          ],
          "text": "Triglycerides"
        },
        "valueQuantity": {
          "value": 150,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    },
    {
      "resource": {
        "resourceType": "Observation",
        "status": "final",
        "code": {
          "coding": [
            {
              "system": "http://loinc.org",
              "code": "3084-1",
              "display": "Uric acid"
            }
          ],
          "text": "Uric acid"
        },
        "valueQuantity": {
          "value": 6.0,
          "unit": "mg/dL"
        },
        "effectiveDateTime": "2022-01-04T08:00:00Z"
      }
    }
  ]
}



# Flask endpoint URL
url = "http://127.0.0.1:5000/fhir_bundle"

# Make a POST request with JSON payload
response = requests.post(url, json=fhir_bundle)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Request was successful!")
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)  # Print the response content for debugging