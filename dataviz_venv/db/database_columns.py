import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('blood_tests.db')

# Create a cursor object
cursor = conn.cursor()

# Execute the PRAGMA query to get table information
cursor.execute("PRAGMA table_info(blood_indicators)")

# Fetch all the rows
columns_info = cursor.fetchall()

# Extract column names
column_names = [column[1] for column in columns_info]

# Print the column names
print(column_names)

# Close the connection
conn.close()
