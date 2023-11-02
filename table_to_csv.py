import sqlite3
import csv
# Define your SQLite database file
db_file = '/home/wzero/modbus_to_db/local.db'
# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
# Specify the table you want to export as CSV
table_name = 'w01_1_energy_meter'
# Define the CSV file to export to
csv_file = 'w01_1_energy_meter_new.csv'
# Create and execute an SQL query to select all rows from the table
query = f'SELECT * FROM {table_name}'
cursor.execute(query)
# Fetch all the rows from the result set
rows = cursor.fetchall()
# Get the column names from the table
column_names = [description[0] for description in cursor.description]
# Write the data to a CSV file
with open(csv_file, 'w', newline='') as file:
    csv_writer = csv.writer(file)
    # Write the header (column names) to the CSV file
    csv_writer.writerow(column_names)
    # Write the rows of data to the CSV file
    csv_writer.writerows(rows)
# Close the database connection
conn.close()
print(f'Data from table "{table_name}" has been exported to "{csv_file}"')