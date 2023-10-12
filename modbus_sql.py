
import minimalmodbus
import time
from database.models import DataRegister, Base
from db import get_sqlite_session, sqlite_engine
from datetime import datetime
from wzero_script import CustomDeviceTable
import pytz  # Import the pytz library for time zone conversion

# Base.metadata.create_all(sqlite_engine)
Base.metadata.create_all(sqlite_engine)

# Define the COM port (adjust the port name as needed, e.g., 'COM1', 'COM2', etc.)
com_port = '/dev/ttyUSB0'

# Define the Modbus slave address (typically 1 for the first device)
slave_address = 1

# Create a Modbus instrument instance for your device
instrument = minimalmodbus.Instrument(com_port, slave_address)

# Set the Modbus serial communication parameters (baudrate, parity, etc.)
instrument.serial.baudrate = 9600  # Adjust to match your device's settings
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 2

# Define the Modbus function code and register address to read from
function_code = 3  # Read Holding Registers
register_addresses = [1, 2, 3, 4, 5, 6, 7]

# Define the number of registers to read
number_of_registers = len(register_addresses)  # Adjust based on your requirements

# Initialize the previous data
previous_data = None

# Define the Indian Standard Time (IST) time zone
indian_timezone = pytz.timezone('Asia/Kolkata')

while True:
    session = None  # Initialize session outside of the try block
    try:
        session = get_sqlite_session()
        data = instrument.read_registers(register_addresses[0], number_of_registers, functioncode=function_code)

        if data != previous_data:
            print("Updated data:")
            for i in range(len(data)):
                print(i)

                ist_timestamp = datetime.now(indian_timezone)

                custom_device_data = CustomDeviceTable(reg_no=register_addresses[i], value=data[i], timestamp=ist_timestamp)
                session.add(custom_device_data)

                try:
                    session.commit()
                    print("Data written to SQLite")
                except Exception as e:
                    print("Data write to SQLite failed:", e)

                print(f"Read data from register {register_addresses[i]}: {data[i]}")

        previous_data = data
        time.sleep(5)  # Sleep for 5 seconds

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if session is not None:
            session.close()





# import minimalmodbus
# import time
# from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import SQLAlchemyError
# from wzero_script import CustomDeviceTable
# from datetime import datetime
# import pytz
# import sqlite3

# # Define the COM port (adjust the port name as needed, e.g., 'COM1', 'COM2', etc.)
# com_port = '/dev/ttyUSB0'

# # Define the Modbus slave address (typically 1 for the first device)
# slave_address = 1

# # Create a Modbus instrument instance for your device
# instrument = minimalmodbus.Instrument(com_port, slave_address)

# # Set the Modbus serial communication parameters
# instrument.serial.baudrate = 9600
# instrument.serial.bytesize = 8
# instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
# instrument.serial.stopbits = 2

# # Define the Modbus function code and register address to read from
# function_code = 3
# register_addresses = [1, 2, 3, 4, 5, 6, 7]
# number_of_registers = len(register_addresses)

# # Initialize the previous data
# previous_data = None

# # Define the Indian Standard Time (IST) time zone
# indian_timezone = pytz.timezone('Asia/Kolkata')

# # SQLite database setup
# sqlite_conn = sqlite3.connect('mydata.db')
# sqlite_cursor = sqlite_conn.cursor()
# sqlite_cursor.execute('''CREATE TABLE IF NOT EXISTS modbus_data (
#                             id INTEGER PRIMARY KEY AUTOINCREMENT,
#                             reg_no INTEGER,
#                             value INTEGER,
#                             timestamp TIMESTAMP
#                         )''')
# sqlite_conn.commit()

# while True:
#     try:
#         # Read data from the Modbus device
#         data = instrument.read_registers(register_addresses[0], number_of_registers, functioncode=function_code)

#         # Check if the data has changed
#         if data != previous_data:
#             print("Updated data:")
#             for i in range(len(data)):
#                 print(f"Read data from register {register_addresses[i]}: {data[i]}")

#                 # Get the current IST timestamp
#                 ist_timestamp = datetime.now(indian_timezone)

#                 # Insert data into SQLite
#                 sqlite_cursor.execute('''
#                     INSERT INTO modbus_data (reg_no, value, timestamp) 
#                     VALUES (?, ?, ?)
#                 ''', (register_addresses[i], data[i], ist_timestamp))
#                 sqlite_conn.commit()
#                 print("Data written to SQLite")

#                 # Transfer data to PostgreSQL
#                 engine = create_engine("postgresql+psycopg2://postgres:postgres@192.168.1.18:5432/test1")
#                 Session = sessionmaker(bind=engine)
#                 session = Session()

#                 try:
#                     custom_device_data = CustomDeviceTable(reg_no=register_addresses[i], value=data[i], timestamp=ist_timestamp)
#                     session.add(custom_device_data)
#                     session.commit()
#                     print("Data written to PostgreSQL")
#                 except SQLAlchemyError as e:
#                     print(f"Data write to PostgreSQL failed: {e}")
#                     session.rollback()
#                 finally:
#                     session.close()

#         # Update the previous data
#         previous_data = data

#         # Wait for 5 seconds before reading again
#         time.sleep(5)
#     except Exception as e:
#         print(f"An error occurred: {e}")

#     finally:
#         # Close the serial connection
#         instrument.serial.close()

# # Close the SQLite connection
# sqlite_conn.close()
