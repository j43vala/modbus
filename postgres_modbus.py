
# import dataclasses
# import time
# import json
# import os
# import socket
# import threading
# from sqlalchemy import create_engine, Column, Integer, DateTime, String, text, func
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.exc import IntegrityError
# from database.models_1 import create_dynamic_model
# from db import get_sqlite_session, get_postgres_session, postgres_engine
# from datetime import datetime, timedelta
# from sqlalchemy.exc import OperationalError
# # from write_functions import create_commit_postgres_data
# from write_functions import publish_mqtt_data,mqtt_config,mqtt_broker_host,mqtt_broker_port,mqtt_topic



# # Initialize 'config' variable to None
# config = None

# # Specify the path to the configuration JSON file
# script_path = os.path.abspath(__file__)
# dir_path = os.path.dirname(script_path)

# config_file_path = os.path.join(dir_path, "config.json")
# sqlite_db_path = os.path.join(dir_path, "local.db")

# # Check if the configuration file exists
# if os.path.isfile(config_file_path):
#     with open(config_file_path, 'r') as config_file:
#         config = json.load(config_file)
# else:
#     print(f"Error: '{config_file_path}' not found")
#     # Handle the case where the configuration file is missing (e.g., provide default values or exit).

# # Define the SQLite database file path
# sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)
# print("SQLite database connected successfully")

# postgres_host = config["remote_db_connection"]["host"]
# try:
#     # Create a PostgreSQL database connection and session
#     PostgresSQL_engine = create_engine(f'postgresql+psycopg2://postgres:postgres@{postgres_host}/test1')
#     # print("PostgresSQL database connected successfully")
# except Exception as e:
#     print(str(e))

# # Define the data transfer interval
# interval = 0.5

# # Define the data retention period in minutes
# data_retention_period_minutes = 5
# data_delete_frequency_minutes = 1

# non_written_data_retention_period_days = 5
# non_written_data_delete_frequency_days = 1

# # Check if the 'config' variable is defined
# if config is not None:
#     com_port = config["modbus"]["port"]
#     devices = config["devices"]
    
#     # Create a PostgreSQL session to manage the 'last_sync_index' table
#     LastSyncIndexBase = declarative_base()

#     class LastSyncIndex(LastSyncIndexBase):
#         __tablename__ = 'last_sync_index'
#         id = Column(Integer, primary_key=True, autoincrement=True)
#         device_name = Column(String, unique=True)
#         last_index = Column(Integer)
#         last_deleted_at = Column(DateTime, server_default=func.now())  # Store the last time data was deleted
#         created_at = Column(DateTime, server_default=func.now())
#         updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

#     LastSyncIndexBase.metadata.create_all(sqlite_engine)

#     # Create models and tables for each device during initialization
#     device_models = {}  # Dictionary to store dynamic models

#     for device in devices:
#         device_name = device.get("device_name", "")
#         slave_id = device.get("slave_id", "")
#         table_name = f"{socket.gethostname()}_{slave_id}_{device_name}"
#         register_list = device.get("registers", "")

#         # Create a dynamic database model for the device data
#         model = create_dynamic_model(table_name, register_list)
#         # while True:
#         try:
#             model.__table__.create(PostgresSQL_engine, checkfirst=True)
#         except OperationalError:
#             print("We're trying to connect with the database")

#         device_models[device_name] = model

#     # Function to synchronize data for a single device
#     def synchronize_data(device):
#         print("thread created....")
#         # Create sessions within the thread
#         sqlite_session = get_sqlite_session()
#         PostgresSQL_session = get_postgres_session()

#         # device = next((device for device in devices if device.get("device_name", "") == device_name), None)
#         device_name = device.get("device_name")
#         if device is not None:
#             hostname = socket.gethostname()
#             print(device_models)
#             model = device_models[device_name]

#             try:
#                 while True:
#                     # Query data from SQLite database for synchronization
#                     last_sync_index_record = sqlite_session.query(LastSyncIndex).filter_by(device_name=device_name).first()

#                     if last_sync_index_record:
#                         last_sync_index = last_sync_index_record.last_index
#                     else:
#                         last_sync_index = 0

#                     # Query data that needs to be synchronized
#                     batch_data = sqlite_session.query(model).filter(model.id > last_sync_index).limit(1000).all()

#                     if batch_data:
#                         #------------------------------------------ 
#                         # create_commit_postgres_data(batch_data=batch_data, model=model, device=device, pg_session=PostgresSQL_session)
#                         #------------------------------------------ 
#                         data_to_publish = []

#                         for data_item in batch_data:
#                             data_to_publish.append({
#                                 'timestamp': data_item.timestamp,
                                
#                             })
#                         publish_mqtt_data(data, mqtt_broker_host,  mqtt_broker_port, mqtt_topic)
                        
                        
#                         last_sync_index = batch_data[-1].id
#                         # print('last_sync_index: ', last_sync_index)

#                         # Update the last_sync_index record
#                         if last_sync_index_record:
#                             last_sync_index_record.last_index = last_sync_index
#                         else:
#                             last_sync_index_record = LastSyncIndex(device_name=device_name, last_index=last_sync_index)
#                             sqlite_session.add(last_sync_index_record)

#                         # Commit the SQLite session
#                         sqlite_session.commit()

#                         # Delete data older than data_retention_period_minutes
#                         current_time = datetime.utcnow()
#                         data_retention_period = current_time - timedelta(minutes=data_retention_period_minutes)
#                         data_delete_frequency = current_time - timedelta(minutes=data_delete_frequency_minutes)

#                         if data_delete_frequency > last_sync_index_record.last_deleted_at:
#                             all_delete_data = sqlite_session.query(model).filter(model.timestamp < data_retention_period).all()

#                             for del_data in all_delete_data:
#                                 sqlite_session.delete(del_data)

#                             last_sync_index_record.last_deleted_at = current_time  # Update the last_deleted_at timestamp
#                             sqlite_session.commit()

#                     time.sleep(interval)
#             except KeyboardInterrupt:
#                 # Close database sessions on keyboard interrupt
#                 sqlite_session.close()
#                 PostgresSQL_session.close()
#             except Exception as e:
#                 current_time = datetime.utcnow()
#                 data_retention_period = current_time - timedelta(minutes=non_written_data_retention_period_days)
#                 data_delete_frequency = current_time - timedelta(minutes=non_written_data_delete_frequency_days)

#                 if data_delete_frequency > last_sync_index_record.last_deleted_at:
#                     all_delete_data = sqlite_session.query(model).filter(model.timestamp < data_retention_period).all()

#                     for del_data in all_delete_data:
#                         sqlite_session.delete(del_data)

#                     last_sync_index_record.last_deleted_at = current_time  # Update the last_deleted_at timestamp
#                     sqlite_session.commit()
#                 print("Error:", e)

#     # Create a separate thread for each device
#     for device in devices:
#         device_name = device.get("device_name", "")
#         print(device_name)
#         thread = threading.Thread(target=synchronize_data, args=(device,))
#         thread.daemon = True
#         thread.start()

#     try:
#         while True:
#             # Main thread continues to run
#             time.sleep(60)  # Sleep for one minute
#     except KeyboardInterrupt:
#         pass
# else:
#     # Handle the situation where the 'config' variable is not defined (e.g., provide default values or exit).
#     pass

import dataclasses
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
from db import get_sqlite_session, get_postgres_session, postgres_engine
from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError

# Initialize 'config' variable to None
config = None

# Specify the path to the configuration JSON file
script_path = os.path.abspath(__file__)
dir_path = os.path.dirname(script_path)
print(script_path)
config_file_path = os.path.join(dir_path, "config.json")
sqlite_db_path = os.path.join(dir_path, "local.db")

# Check if the configuration file exists
if os.path.isfile(config_file_path):
    with open(config_file_path, 'r') as config_file:
        config = json.load(config_file)
else:
    print(f"Error: '{config_file_path}' not found")
    # Handle the case where the configuration file is missing (e.g., provide default values or exit).

# Define the SQLite database file path
sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)
print("SQLite database connected successfully")

postgres_host = config["remote_db_connection"]["host"]
try:
    # Create a PostgreSQL database connection and session
    PostgresSQL_engine = create_engine(f'postgresql+psycopg2://postgres:postgres@{postgres_host}/test1')
    # print("PostgresSQL database connected successfully")
except Exception as e:
    print(str(e))

# Define the data transfer interval
interval = 0.5

# Define the data retention period in minutes
data_retention_period_minutes = 5
data_delete_frequency_minutes = 1

non_written_data_retention_period_days = 5
non_written_data_delete_frequency_days = 1


mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker_host, mqtt_broker_port)

# Check if the 'config' variable is defined
if config is not None:
    com_port = config["modbus"]["port"]
    devices = config["devices"]

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
    device_models = {}  # Dictionary to store dynamic models

    for device in devices:
        device_name = device.get("device_name", "")
        slave_id = device.get("slave_id", "")
        table_name = f"{socket.gethostname()}_{slave_id}_{device_name}"
        register_list = device.get("registers", "")

        # Create a dynamic database model for the device data
        model = create_dynamic_model(table_name, register_list)
        # while True:
        try:
            model.__table__.create(PostgresSQL_engine, checkfirst=True)
        except OperationalError:
            print("We're trying to connect with the database")

        device_models[device_name] = model

    # Function to synchronize data for a single device
    def synchronize_data(device):
        print("thread created....")
        # Create sessions within the thread
        sqlite_session = get_sqlite_session()
        PostgresSQL_session = get_postgres_session()

        # device = next((device for device in devices if device.get("device_name", "") == device_name), None)
        device_name = device.get("device_name")
        if device is not None:
            hostname = socket.gethostname()
            print(device_models)
            model = device_models[device_name]

            try:
                
                    # Query data from SQLite database for synchronization
                    last_sync_index_record = sqlite_session.query(LastSyncIndex).filter_by(device_name=device_name).first()

                    if last_sync_index_record:
                        last_sync_index = last_sync_index_record.last_index
                    else:
                        last_sync_index = 0

                    # Query data that needs to be synchronized
                    batch_data = sqlite_session.query(model).filter(model.id > last_sync_index).limit(1000).all()

                    if batch_data:
                        data_to_publish = []

                        for data_item in batch_data:
                            data_to_publish.append({
                                'timestamp': data_item.timestamp,
                            })

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
                        data_delete_frequency = current_time - timedelta(minutes=data_delete_frequency_minutes)

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
                current_time = datetime.utcnow()
                data_retention_period = current_time - timedelta(minutes=non_written_data_retention_period_days)
                data_delete_frequency = current_time - timedelta(minutes=non_written_data_delete_frequency_days)

                if data_delete_frequency > last_sync_index_record.last_deleted_at:
                    all_delete_data = sqlite_session.query(model).filter(model.timestamp < data_retention_period).all()

                    for del_data in all_delete_data:
                        sqlite_session.delete(del_data)

                    last_sync_index_record.last_deleted_at = current_time  # Update the last_deleted_at timestamp
                    sqlite_session.commit()
                print("Error:", e)

    # Create a separate thread for each device
    for device in devices:
        device_name = device.get("device_name", "")
        print(device_name)
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
