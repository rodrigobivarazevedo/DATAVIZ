import sqlite3
import csv

# Create or connect to the SQLite database
conn = sqlite3.connect('blood_tests.db')
cursor = conn.cursor()

# Load data from the "blood_indicators.csv" CSV file into the "blood_indicators" table
with open('blood_indicators.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        cursor.execute("INSERT INTO blood_indicators (column1, column2, column3, column4, column5, column6, column7, column8, column9, column10, column11, column12, column13, column14, column15, column16, column17, column18, column19, column20, column21, column22, column23, column24, column25, column26, column27, column28, column29, column30, column31, column32, column33, column34, column35, column36, column37, column38, column39) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)


with open('patients.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        cursor.execute("INSERT INTO patients (column1, column2, column3, column4, column5) VALUES (?, ?, ?, ?, ?)", row)
        
# Commit the changes and close the database connection
conn.commit()
conn.close()
