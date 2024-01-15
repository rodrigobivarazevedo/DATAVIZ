# The App

### JSON Rest API

The app provides raw json data via the routes:

- /patientID/raw/   
- /Blood_tests/raw/patientID 

The app provides FHIR data via the routes:

- /patientID/fhir/   
- /Blood_tests/fhir/patientID

The app stores or reads sent FHIR data via the routes: 

- /process_cmp  (read values from a comprehensive metabolic panel test encoded in FHIR)
- /fhir_bundle  (process a FHIR bundle containing patient resource and collection of blood observations resources)


### The HTML views

- / (Heatmap View from a specific blood test of a Patient)
- red = outside normal range
- yellow = close to outside range
- green = normal range
  
![Alt Text](heatmap3.png)
