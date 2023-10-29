import sqlite3

# Create or connect to the SQLite database
conn = sqlite3.connect('blood_tests.db')
cursor = conn.cursor()

# Create the "blood_indicators" table with the specified columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS blood_indicators (
        column1 INTEGER,
        column2 DATE,
        column3 INTEGER,
        column4 INTEGER,
        column5 INTEGER,
        column6 INTEGER,
        column7 INTEGER,
        column8 INTEGER,
        column9 INTEGER,
        column10 INTEGER,
        column11 INTEGER,
        column12 INTEGER,
        column13 INTEGER,
        column14 INTEGER,
        column15 INTEGER,
        column16 INTEGER,
        column17 INTEGER,
        column18 INTEGER,
        column19 INTEGER,
        column20 INTEGER,
        column21 INTEGER,
        column22 INTEGER,
        column23 INTEGER,
        column24 INTEGER,
        column25 INTEGER,
        column26 INTEGER,
        column27 INTEGER,
        column28 INTEGER,
        column29 INTEGER,
        column30 INTEGER,
        column31 INTEGER,
        column32 INTEGER,
        column33 INTEGER,
        column34 INTEGER,
        column35 INTEGER,
        column36 INTEGER,
        column37 INTEGER,
        column38 INTEGER,
        column39 INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        column1 INTEGER,
        column2 TEXT,
        column3 TEXT,
        column4 DATE,
        column5 TEXT
    )
''')

# Commit the changes and close the database connection
conn.commit()
conn.close()