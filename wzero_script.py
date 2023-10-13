import json
import os
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from database.models_1 import create_dynamic_model

# Read the configuration from the JSON file
config_file_path = '/home/wzero/modbus/w_script.json'
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

# Get the hostname
hostname = os.uname()[1]

devices = config.get("devices", [])
if devices:
    # Establish a connection to the PostgreSQL server using SQLAlchemy
    postgres_engine = create_engine(
        f"postgresql+psycopg2://{config['remote_db_connection']['user']}:{config['remote_db_connection']['password']}@{config['remote_db_connection']['host']}:{config['remote_db_connection']['port']}/{config['remote_db_connection']['database']}",
        pool_recycle=3600,
        echo=True,
    )

    # Establish a connection to the SQLite database using SQLAlchemy
    # Replace the path with the actual SQLite database file path
    sqlite_db_path = '/home/wzero/modbus/mydatabase.db'  # Update this path
    sqlite_engine = create_engine(f'sqlite:///{sqlite_db_path}', echo=True)

    # Define a declarative base for your tables

    # Base = declarative_base()

    for device in config["devices"]:
        device_name = device.get("edge_device_name", "")
        slave_id = device.get("slave_id", "")
        table_name = f"{hostname}_{slave_id}_{device_name}"

        register_dict = device["register"]
        column_names = []
        for reg in register_dict :
            column_names.append(register_dict[reg])
        print(column_names)

        model = create_dynamic_model(table_name, column_names)
        
        model.__table__.create(sqlite_engine, checkfirst = True)
        model.__table__.create(postgres_engine, checkfirst = True)

        record = model()

        
        # # Define your custom table columns
        # columns = [
        #     Column('id', Integer, primary_key=True, autoincrement=True),
        #     Column('timestamp', TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), nullable=False),
        # ]

        # # Add columns dynamically based on the 'register' dictionary in the configuration
        # for col_name in device.get("register", {}).values():
        #     columns.append(Column(col_name, Integer))

        #     # Add columns for keys based on the 'keys' dictionary in the configuration
        # for key, value in device.get("keys", {}).items():
        #     columns.append(Column(key, String, default=value))

        # metadata = MetaData()
        # table = type(table_name, (Base,), {'__tablename__': table_name, '__table_args__': {'extend_existing': True}, **{column.name: column for column in columns}})

        # # Create the table in SQLite
        # table.metadata.create_all(sqlite_engine)
        # print(f"Table '{table_name}' has been created in SQLite for device '{device_name}'.")

        # # Create the table in PostgreSQL
        # table.metadata.create_all(postgres_engine)
        # print(f"Table '{table_name}' has been created in PostgreSQL for device '{device_name}'.")
        
    # Close the database engine connections
    # postgres_engine.dispose()
    # sqlite_engine.dispose()
else:
    print("No device configurations found in the JSON file.")