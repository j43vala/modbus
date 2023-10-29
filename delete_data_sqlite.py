# Import necessary libraries
from datetime import datetime, timedelta
from sqlalchemy import text
from db import get_sqlite_session
from database.models_1 import create_dynamic_model
import os
import json
import socket

# Initialize the 'config' variable to None
config = None

# Specify the path to the configuration JSON file
config_file_path = '/home/wzero/Public/modbus/w_script.json'

# Check if the configuration file exists
if os.path.isfile(config_file_path):
    # If it exists, open and read the JSON configuration
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
else:
    print(f"Error: '{config_file_path}' not found")
    # You may want to handle this situation, such as providing default values or exiting the script.

# Dictionary to store dynamic tables
tables_dict = {}

if config is not None:
    # Get the communication port and device information from the configuration
    com_port = config["modbus"]["port"]
    devices = config["devices"]

    # Iterate through devices defined in the configuration
    for device in devices:
        hostname = socket.gethostname()
        device_name = device.get("edge_device_name", "")
        slave_id = device.get("slave_id", "")
        table_name = f"{hostname}_{slave_id}_{device_name}"

        # Create a list of column names for the dynamic table
        register_dict = device["register"]
        column_names = []
        for reg in register_dict:
            column_names.append(register_dict[reg])

        # Store the dynamic table name and column names in the 'tables_dict'
        tables_dict[table_name] = column_names

# Function to delete data from dynamic tables
def delete_data_from_dynamic_table(minutes=1):
    try:
        # Get a SQLite session
        Session = get_sqlite_session()

        for table_name, column_names in tables_dict.items():
            # Create a dynamic SQLAlchemy table model
            model = create_dynamic_model(table_name, column_names)
            
            # Calculate the datetime from which data should be deleted
            end_datetime = datetime.utcnow()
            start_datetime = end_datetime - timedelta(minutes=minutes)

            with Session as session:
                # Define the SQL query to delete data within the specified time range
                delete_query = text(f"DELETE FROM {model.__table__.name} WHERE timestamp >= :start_datetime AND timestamp <= :end_datetime")

                # Execute the SQL query to delete data
                session.execute(delete_query, {"start_datetime": start_datetime, "end_datetime": end_datetime})

                session.commit()
                print(f"Data deleted successfully from the dynamic table '{table_name}' for the last {hours} hours")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
delete_data_from_dynamic_table(minutes=1)
