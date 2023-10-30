# import time
# import json
# import os
# import socket
# from sqlalchemy import create_engine, Column, Integer, DateTime, String, text, func
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.exc import IntegrityError
# from database.models_1 import create_dynamic_model

# # Initialize 'config' variable to None
# config = None

# # Read configuration data from a JSON file
# config_file_path = '/home/wzero/Public/modbus/w_script.json'
# if os.path.isfile(config_file_path):
#     with open(config_file_path, 'r') as config_file:
#         config = json.load(config_file)
# else:
#     print(f"Error: '{config_file_path}' not found")
#     # Handle the case where the configuration file is missing (e.g., provide default values or exit).

# # Define paths and create a SQLite database and session
# sqlite_db_path = "/home/wzero/Public/modbus/mydatabase.db"
# sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)
# print("SQLite database connected successfully.")
# Sqlite_Session = sessionmaker(bind=sqlite_engine)
# sqlite_session = Sqlite_Session()

# # Create a PostgreSQL database connection and session
# PostgresSQL_engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/test1')
# print("PostgresSQL database connected successfully.")
# Session = sessionmaker(bind=PostgresSQL_engine)
# PostgresSQL_session = Session()

# # Define the data transfer interval
# interval = 0.5

# # Check if the 'config' variable is defined
# if config is not None:
#     com_port = config["modbus"]["port"]
#     devices = config["devices"]

#     for device in devices:
#         hostname = socket.gethostname()
#         device_name = device.get("edge_device_name", "")
#         slave_id = device.get("slave_id", "")
#         table_name = f"{hostname}_{slave_id}_{device_name}"

#         # Extract register information from the device configuration
#         register_dict = device["register"]
#         column_names = list(register_dict.values())  # Get the column names directly from the values in the register dictionary
#         print(column_names)

#         # Define a table to store the last synchronized index for this device in SQLite
#         Base = declarative_base()

#         class LastSyncIndex(Base):
#             __tablename__ = f'last_sync_index_{table_name}'
#             id = Column(Integer, primary_key=True, autoincrement=True)
#             device_name = Column(String, unique=True)
#             last_index = Column(Integer)
#             created_at = Column(DateTime, server_default=func.now())
#             updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

#         # Create the table in SQLite
#         Base.metadata.create_all(sqlite_engine)

#         # Retrieve the last synchronized index for this device
#         last_sync_index_record = sqlite_session.query(LastSyncIndex).filter_by(device_name=device_name).first()
#         if last_sync_index_record:
#             last_sync_index = last_sync_index_record.last_index
#         else:
#             last_sync_index = 0

#         # Create a dynamic model for the table and create the table in the PostgreSQL database
#         model = create_dynamic_model(table_name, column_names)  # A function 'create_dynamic_model' is assumed here
#         model.__table__.create(PostgresSQL_engine, checkfirst=True)
    
#         try:
#             while True:
#                 # Fetch data from SQLite with an index greater than the last synchronized index
#                 batch_data = sqlite_session.query(model).filter(model.id > last_sync_index).limit(1000).all()

#                 # Check if there is new data to transfer
#                 if batch_data:
#                     # Insert new data into PostgreSQL using SQLAlchemy
#                     for row in batch_data:
#                         try:
#                             postgres_data = model()
#                             for col_name in column_names:
#                                 setattr(postgres_data, col_name, getattr(row, col_name))
#                             postgres_data.timestamp = row.timestamp
#                             PostgresSQL_session.add(postgres_data)
#                         except IntegrityError as e:
#                             # Handle duplicates or other errors as needed
#                             PostgresSQL_session.rollback()

#                     # Commit the changes to PostgreSQL
#                     PostgresSQL_session.commit()

#                     # Update the last synchronized index for this device
#                     last_sync_index = batch_data[-1].id
#                     last_sync_index_record = sqlite_session.query(LastSyncIndex).filter_by(device_name=device_name).first()
#                     if last_sync_index_record:
#                         last_sync_index_record.last_index = last_sync_index
#                     else:
#                         # If no record exists, create one
#                         last_sync_index_record = LastSyncIndex(device_name=device_name, last_index=last_sync_index)
#                         sqlite_session.add(last_sync_index_record)
#                     sqlite_session.commit()

#                 # Sleep for the specified interval
#                 time.sleep(interval)

#         except KeyboardInterrupt:
#             # Close database sessions on keyboard interrupt
#             sqlite_session.close()
#             PostgresSQL_session.close()
#         except Exception as e:
#             print("Error:", e)
# else:
#     # Handle the situation where the 'config' variable is not defined (e.g., provide default values or exit).
#     pass

import time
import json
import os
import socket
import threading
from sqlalchemy import create_engine, Column, Integer, DateTime, String, text, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from database.models_1 import create_dynamic_model
from db import get_sqlite_session, get_postgres_session
from datetime import datetime, timedelta

# Initialize 'config' variable to None
config = None

# Read configuration data from a JSON file
config_file_path = '/home/wzero/Public/modbus/w_script.json'

# Check if the configuration file exists
if os.path.isfile(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
else:
    print(f"Error: '{config_file_path}' not found")
    # Handle the case where the configuration file is missing (e.g., provide default values or exit).

# Define paths and create a SQLite database and session
sqlite_db_path = "/home/wzero/Public/modbus/mydatabase.db"
sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)
print("SQLite database connected successfully")

# Create a PostgreSQL database connection and session
PostgresSQL_engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/test1')
print("PostgresSQL database connected successfully")

# Define the data transfer interval
interval = 0.5

# Define the data retention period in minutes
data_retention_period_minutes = 1

# Check if the 'config' variable is defined
if config is not None:
    com_port = config["modbus"]["port"]
    devices = config["devices"]

    # Define a dictionary to store the last_sync_index for each device
    device_last_sync_index = {}
    device_models = {}  # Dictionary to store dynamic models

    # Create a PostgreSQL session to manage the 'last_sync_index' table
    LastSyncIndexBase = declarative_base()

    class LastSyncIndex(LastSyncIndexBase):
        __tablename__ = 'last_sync_index'
        id = Column(Integer, primary_key=True, autoincrement=True)
        device_name = Column(String, unique=True)
        last_index = Column(Integer)
        last_deleted_at = Column(DateTime, server_default=func.now())  # Store the last time data was deleted
        created_at = Column(DateTime, server_default=func.now())
        updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    LastSyncIndexBase.metadata.create_all(sqlite_engine)

    # Create models and tables for each device during initialization
    for device in devices:
        hostname = socket.gethostname()
        device_name = device.get("edge_device_name", "")
        slave_id = device.get("slave_id", "")
        table_name = f"{hostname}_{slave_id}_{device_name}"
        column_names = list(device["register"].values())

        # Create a dynamic database model for the device data
        model = create_dynamic_model(table_name, column_names)
        model.__table__.create(PostgresSQL_engine, checkfirst=True)

        device_models[device_name] = model

    # Function to synchronize data for a single device
    def synchronize_data(device):
        # Create sessions within the thread
        sqlite_session = get_sqlite_session()
        PostgresSQL_session = get_postgres_session()

        # Get device information
        hostname = socket.gethostname()
        device_name = device.get("edge_device_name", "")
        model = device_models.get(device_name)
        
        if model is not None:
            try:
                while True:
                    # Query data from SQLite database for synchronization
                    last_sync_index_record = sqlite_session.query(LastSyncIndex).filter_by(device_name=device_name).first()

                    if last_sync_index_record:
                        last_sync_index = last_sync_index_record.last_index
                    else:
                        last_sync_index = 0

                    # Query data that needs to be synchronized
                    batch_data = sqlite_session.query(model).filter(model.id > last_sync_index).limit(1000).all()

                    if batch_data:
                        for row in batch_data:
                            try:
                                # Create a corresponding record in the PostgreSQL database
                                postgres_data = model()
                                for col_name in column_names:
                                    setattr(postgres_data, col_name, getattr(row, col_name))
                                postgres_data.timestamp = row.timestamp
                                PostgresSQL_session.add(postgres_data)
                            except IntegrityError as e:
                                PostgresSQL_session.rollback()

                        # Commit the changes to the PostgreSQL database
                        PostgresSQL_session.commit()
                        last_sync_index = batch_data[-1].id

                        # Update the last_sync_index record
                        if last_sync_index_record:
                            last_sync_index_record.last_index = last_sync_index
                        else:
                            last_sync_index_record = LastSyncIndex(device_name=device_name, last_index=last_sync_index)
                            sqlite_session.add(last_sync_index_record)

                        # Commit the SQLite session
                        sqlite_session.commit()
                        
                        # Delete data older than data_retention_period_minutes
                        current_time = datetime.utcnow()
                        data_retention_period = current_time - timedelta(minutes=data_retention_period_minutes)
                        data_delete_frequency = current_time - timedelta(minutes=5)

                        if data_delete_frequency > last_sync_index_record.last_deleted_at:
                            all_delete_data = sqlite_session.query(model).filter(model.timestamp < data_retention_period).all()

                            for del_data in all_delete_data:
                                sqlite_session.delete(del_data)

                            last_sync_index_record.last_deleted_at = current_time  # Update the last_deleted_at timestamp
                            sqlite_session.commit()


                    time.sleep(interval)
            except KeyboardInterrupt:
                # Close database sessions on keyboard interrupt
                sqlite_session.close()
                PostgresSQL_session.close()
            except Exception as e:
                print("Error:", e)

    # Create a separate thread for each device
    for device in devices:
        thread = threading.Thread(target=synchronize_data, args=(device,))
        thread.daemon = True
        thread.start()

    try:
        while True:
            # Main thread continues to run
            time.sleep(60)  # Sleep for one minute
    except KeyboardInterrupt:
        pass
else:
    # Handle the situation where the 'config' variable is not defined (e.g., provide default values or exit).
    pass
