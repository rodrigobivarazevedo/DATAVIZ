-- Rename columns that where missed in the data cleaning
ALTER TABLE blood_indicators
RENAME COLUMN lbxsldsi TO "Lactate dehydrogenase (U/L)";

ALTER TABLE blood_indicators
RENAME COLUMN lbdsphsi TO "Phosphorus (mmol/L)";

ALTER TABLE blood_indicators
RENAME COLUMN lbxsksi TO "Potassium (mmol/L)";

ALTER TABLE blood_indicators
RENAME COLUMN lbxsgb TO "Globulin (g/dL)";
