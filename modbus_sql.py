
import minimalmodbus
import time
from db import get_sqlite_session, sqlite_engine
from datetime import datetime
import pytz
import json
import os

from database.models_1 import create_dynamic_model

# Initialize the 'config' variable to None
config = None

# Read configuration from JSON file
config_file_path = '/home/wzero/modbus/w_script.json'

if os.path.isfile(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
else:
    print(f"Error: '{config_file_path}' not found")
    # You may want to handle this situation, such as providing default values or exiting the script.

tables_dict = {}
if config is not None:
    com_port = config["modbus"]["port"]
    devices = config["devices"]

    for device in devices:
        hostname = os.uname()[1]
        device_name = device.get("edge_device_name", "")
        slave_id = device.get("slave_id", "")
        table_name = f"{hostname}_{slave_id}_{device_name}"

        register_dict = device["register"]
        column_names = []
        for reg in register_dict:
            column_names.append(register_dict[reg])
        print(column_names)

        model = create_dynamic_model(table_name, column_names)
        model.__table__.create(sqlite_engine, checkfirst=True)

        tables_dict[device_name] = model

    # print("tables_dict: ", tables_dict)

    while 1:
        for device in devices:
            # print("device ", device)
            instrument = minimalmodbus.Instrument(com_port, device.get("slave_id"))
            instrument.serial.baudrate = 9600
            instrument.serial.bytesize = 8
            instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
            instrument.serial.stopbits = 2

            function_code = 3
            register_dict = device.get("register")  # Use the addresses from the JSON file
            number_of_registers = len(register_dict)

            previous_data = None
            # indian_timezone = pytz.timezone('Asia/Kolkata')

            try:
                session = get_sqlite_session()
                device_name = device.get("edge_device_name", "")
                slave_id = device.get("slave_id", "")
                model = tables_dict[device_name]

                record = model()
                for register_key in register_dict:
                    data = instrument.read_register(int(register_key), functioncode=function_code)
                    column_name = register_dict[register_key]
                    setattr(record, column_name, data)
                    # print(device_name, "\ncol_name:", column_name, getattr(record, column_name))

                session.add(record)
                session.commit()
                time.sleep(1)

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                if session is not None:
                    session.close()
else:
    # Handle the situation where the 'config' variable is not defined (e.g., provide default values or exit).
    pass
