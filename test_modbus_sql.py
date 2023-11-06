import time
from db import get_sqlite_session, sqlite_engine
from datetime import datetime
import pytz
import json
import os
import random
from database.models_1 import create_dynamic_model

# Initialize the 'config' variable to None
config = None

# Specify the path to the configuration JSON file
script_path = os.path.abspath(__file__)
dir_path = os.path.dirname(script_path)

config_file_path = os.path.join(dir_path, "config.json")

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

modbus_config = config.get("modbus")

com_port = modbus_config.get("port")
method = modbus_config.get("method", "rtu")
parity = modbus_config.get("parity", "N")
baudrate = modbus_config.get("baudrate", 9600)
stopbits = modbus_config.get("stopbits", 1)
bytesize = modbus_config.get("bytesize", 8)

# client = ModbusClient(method=method, port=com_port, stopbits=stopbits, bytesize=bytesize, parity=parity, baudrate=baudrate)

# Connect to the Modbus server
# client.connect()
# Check if the configuration is available
if config is not None:
    # Get the communication port and device information from the configuration
    com_port = config["modbus"]["port"]
    devices = config["devices"]

    hostname = os.uname()[1]

    # Iterate through devices defined in the configuration
    for device in devices:
        device_name = device.get("device_name", "")
        # print("\ndevice_name : ", device_name)
        slave_id = device.get("slave_id", "")
        table_name = f"{hostname}_{slave_id}_{device_name}"
        # print("table_name : ", table_name)
        register_list = device.get("registers")

        # Create a dynamic SQLAlchemy table model
        model = create_dynamic_model(table_name, register_list)
        # Create the physical table in the SQLite database if it doesn't exist
        model.__table__.create(sqlite_engine, checkfirst=True)

        # Store the model in the dictionary for later use
        tables_dict[device_name] = model

    # Continuous data acquisition loop
    while True:
        for device in devices:

            function_code = 3
            register_list = device.get("registers")  # Use the addresses from the JSON file

            # Open a session to interact with the SQLite database
            # try:
            session = get_sqlite_session()
            device_name = device.get("device_name", "")
            print("\ndevice_name : ", device_name)
            slave_id = device.get("slave_id", "")
            model = tables_dict[device_name]

            # Create a new record and populate it with data
            record = model()

            for register in register_list:
                reg_address = register.get("address")
                column_name = register.get("column_name")
                reg_type = register.get("type")

                data = None  # Initialize data variable

                if reg_type == "integer":
                    # Generate a random integer value between 0 and 100
                    data = random.randint(0, 100)
                    print('integer > ', reg_address, ":", data)
                elif reg_type == "double":
                    # Generate a random double value
                    data = random.uniform(0.0, 100.0)  # Adjust the range as needed
                    print('double > ', reg_address, ":", data)
                elif reg_type == "float":
                    # Generate a random float value
                    data = random.uniform(0.0, 100.0)  # Adjust the range as needed
                    print('float > ', reg_address, ":", data)
                else:
                    print(f"Unsupported reg_type '{reg_type}' for register {reg_address}")

                if column_name:
                    setattr(record, column_name, data)
                else:
                    print(f"Attribute name is missing in the specification for register {column_name}")

                # Add the record to the session and commit it to the database
                session.add(record)
            session.commit()
            time.sleep(1)

# Handle the situation where the 'config' variable is not defined (e.g., provide default values or exit).
else:
    # Handle the situation where the 'config' variable is not defined (e.g., provide default values or exit).
    pass
