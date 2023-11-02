# from sqlalchemy import create_engine, MetaData, Table, Column, DateTime, Integer, String, Float, text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime

# Base = declarative_base()

# def create_dynamic_model(table_name, column_names):
#     class_name = table_name
#     class_attributes = {
#         "__tablename__": table_name,
#         "id": Column(Integer, primary_key=True, autoincrement=True),
#         "timestamp": Column(DateTime, default=datetime.utcnow, nullable=False),
#     }
#     DynamicModel = type(class_name, (Base,), class_attributes)
#     # Define columns dynamically based on the input dictionary
#     for col_name in column_names:
#         setattr(DynamicModel, col_name, Column(Float))
#     return DynamicModel

from sqlalchemy import create_engine, Table, Column, Integer, String, Float, text, DateTime, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import os

Base = declarative_base()

def create_dynamic_model(table_name, column_specifications):
    class_name = table_name
    class_attributes = {
        "__tablename__": table_name,
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "timestamp": Column(DateTime, default=datetime.utcnow, nullable=False),
    }

    # Define columns dynamically based on the JSON specification
    for register in column_specifications:
        # for register_address, register_info in device_spec.get("register", {}).items():
            col_name = register.get("column_name")
            col_type = register.get("type")

            if col_name is None:
                raise ValueError("Column name is missing in the specification.")

            if col_type is None:
                raise ValueError(f"Column type is missing for column {col_name} in the specification.")

            if col_type == "integer":
                col_class = Integer
            elif col_type == "double":
                col_class = Double
            elif col_type == "float":
                col_class = Float
            else:
                raise ValueError(f"Unsupported column type '{col_type}' for column {col_name}.")

            class_attributes[col_name] = Column(col_class)

    DynamicModel = type(class_name, (Base,), class_attributes)
    return DynamicModel

# config_file_path = '/home/wzero/modbus/w_script.json'

# # Check if the configuration file exists
# if os.path.isfile(config_file_path):
#     # Load the column specifications from the JSON file
#     with open(config_file_path, "r") as json_file:
#         data = json.load(json_file)
#         # Assuming your JSON data structure is under "devices"
#         column_specifications = data.get("devices", [])
# else:
#     # Handle the case when the configuration file does not exist
#     raise FileNotFoundError(f"Configuration file not found at path: {config_file_path}")

# # Create the DynamicModel based on the JSON specification
# DynamicModel = create_dynamic_model("YourTableName", column_specifications)
