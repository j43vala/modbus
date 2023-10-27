import minimalmodbus
import time
from db import get_sqlite_session, sqlite_engine
from datetime import datetime
import pytz
import json
import os
import struct  # Import the struct module for float conversion
from pymodbus.client import ModbusSerialClient as ModbusClient
from database.models_1 import create_dynamic_model

# Initialize the 'config' variable to None
config = None

# Specify the path to the configuration JSON file
config_file_path = '/home/wzero/modbus/w_script.json'

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


client = ModbusClient(method=method, port=com_port, stopbits=stopbits, bytesize=bytesize, parity=parity, baudrate=baudrate)

# Connect to the Modbus server
client.connect()
# Check if the configuration is available
if config is not None:
    # Get the communication port and device information from the configuration
    com_port = config["modbus"]["port"]
    devices = config["devices"]

    hostname = os.uname()[1]
    
    # Iterate through devices defined in the configuration
    for device in devices:
        device_name = device.get("device_name", "")
        slave_id = device.get("slave_id", "")
        table_name = f"{hostname}_{slave_id}_{device_name}"
        register_list = device.get("registers")

        # Create a list of column names for the dynamic table
        # column_names = list(register_list.values())  # Use values from the dictionary

        # print(column_names)

        # Create a dynamic SQLAlchemy table model
        model = create_dynamic_model(table_name, register_list)
        # Create the physical table in the SQLite database if it doesn't exist
        model.__table__.create(sqlite_engine, checkfirst=True)

        # Store the model in the dictionary for later use
        tables_dict[device_name] = model

    # Continuous data acquisition loop
    while True:
        for device in devices:
            # Initialize the Modbus instrument for communication
            instrument = minimalmodbus.Instrument(com_port, device.get("slave_id"))
            instrument.serial.baudrate = 9600
            instrument.serial.bytesize = 8
            instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
            instrument.serial.stopbits = 2

            function_code = 3
            register_list = device.get("registers")  # Use the addresses from the JSON file

            # Open a session to interact with the SQLite database
            # try:
            session = get_sqlite_session()
            device_name = device.get("device_name", "")
            slave_id = device.get("slave_id", "")
            model = tables_dict[device_name]

            # Create a new record and populate it with data from Modbus
            record = model()

            for register in register_list:
                reg_address = register.get("address")
                column_name = register.get("column_name")
                reg_type = register.get("type")

                data = None  # Initialize data variable


              
                if reg_type == "integer":
                    result = client.read_holding_registers(reg_address, 1, slave=slave_id)
                    if result.isError():
                        print(f"Error reading Modbus data: {result}")
                        continue
                    else:
                        data = result.registers[0]
                    # data = instrument.read_register(reg_address, functioncode=function_code)
                    print('dataqwerrtuioplkkjhfdsa: ', data)
                elif reg_type == "float":
                    # reg_1, reg_2 = client.read_holding_registers(reg_address, 2, slave=slave_id)
                    result = client.read_holding_registers(reg_address, 2, slave=slave_id)
                    if result.isError():
                        print(f"Error reading Modbus data: {result}")
                        continue
                    else:
                        reg_1, reg_2 = result.registers
                        
                    # Logic for float conversion
                    float_value = struct.unpack('<f', struct.pack('<HH', reg_1, reg_2))[0]
                    print('float_value: ', float_value)
                    data = float_value
                else:
                    print(f"Unsupported reg_type '{reg_type}' for register key {register_key}")
                
                if column_name:
                    setattr(record, column_name, data)
                else:
                    print(f"Attribute name is missing in the specification for register key {register_key}")
                # Add the record to the session and commit it to the database
                session.add(record)
            session.commit()
            time.sleep(1)

            # except Exception as e:
            #     print(f"An error occurred: {e}")

            # finally:
            #     if session is not None:
            #         session.close()
else:
    # Handle the situation where the 'config' variable is not defined (e.g., provide default values or exit).
    pass

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# import minimalmodbus
# import time
# from db import get_sqlite_session, sqlite_engine
# from datetime import datetime
# import pytz
# import json
# import os
# import struct
# from sqlalchemy import create_engine, MetaData, Table, Column, Float
# from database.models_1 import create_dynamic_model

# # Initialize the 'config' variable to None
# config = None

# # Specify the path to the configuration JSON file
# config_file_path = '/home/wzero/modbus/w_script.json'

# # Check if the configuration file exists
# if os.path.isfile(config_file_path):
#     # If it exists, open and read the JSON configuration
#     with open(config_file_path, 'r') as config_file:
#         config = json.load(config_file)
# else:
#     print(f"Error: '{config_file_path}' not found")
#     # You may want to handle this situation, such as providing default values or exiting the script.

# # Function to create a dynamic SQLAlchemy table model
# def create_dynamic_model(table_name, column_names):
#     metadata = MetaData()
#     dynamic_table = Table(table_name, metadata)

#     for col_name in column_names:
#         dynamic_table.append_column(Column(col_name, Float))

#     return dynamic_table

# # Dictionary to store dynamic tables
# tables_dict = {}

# # Check if the configuration is available
# if config is not None:
#     # Get the communication port and device information from the configuration
#     com_port = config["modbus"]["port"]
#     devices = config["devices"]

#     # Iterate through devices defined in the configuration
#     for device in devices:
#         hostname = os.uname()[1]
#         device_name = device.get("device_name", "")
#         slave_id = device.get("slave_id", "")
#         table_name = f"{hostname}_{slave_id}_{device_name}"
#         register_dict = device.get("register")

#         # Create a list of column names for the dynamic table
#         column_names = [register_info["name"] for register_info in register_dict.values()]

#         # Create a dynamic SQLAlchemy table model
#         model = create_dynamic_model(table_name, column_names)

#         # Create the physical table in the SQLite database if it doesn't exist
#         model.create(bind=sqlite_engine, checkfirst=True)

#         # Store the model in the dictionary for later use
#         tables_dict[device_name] = model

#     # Continuous data acquisition loop
#     while 1:
#         for device in devices:
#             # Initialize the Modbus instrument for communication
#             instrument = minimalmodbus.Instrument(com_port, device.get("slave_id"))
#             instrument.serial.baudrate = 9600
#             instrument.serial.bytesize = 8
#             instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
#             instrument.serial.stopbits = 2

#             function_code = 3
#             register_dict = device.get("register")  # Use the addresses from the JSON file
#             number_of_registers = len(register_dict)

#             previous_data = None

#             # Open a session to interact with the SQLite database
#             try:
#                 session = get_sqlite_session()
#                 device_name = device.get("device_name", "")
#                 slave_id = device.get("slave_id", "")
#                 model = tables_dict[device_name]

#                 # Create a new record and populate it with data from Modbus
#                 record = model()
#                 for register_key, register_info in register_dict.items():
#                     reg_type = register_info.get("type", "integer")

#                     if reg_type == "integer":
#                         data = instrument.read_register(reg_address, functioncode=function_code)
#                     elif reg_type == "float":
#                         reg_1, reg_2 = instrument.read_registers(reg_address, number_of_registers=2, functioncode=function_code)
#                         # Logic for float conversion
#                         float_value = struct.unpack('<f', struct.pack('<HH', reg_1, reg_2))[0]

#                         data = float_value

#                     column_name = register_info.get("name", "")
#                     setattr(record, column_name, data)

#                 # Add the record to the session and commit it to the database
#                 session.add(record)
#                 session.commit()
#                 time.sleep(1)

#             except Exception as e:
#                 print(f"An error occurred: {e}")

#             finally:
#                 if session is not None:
#                     session.close()
# else:
#     # Handle the situation where the 'config' variable is not defined (e.g., provide default values or exit).
#     pass
