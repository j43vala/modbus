from sqlalchemy import create_engine, MetaData, Table, Column, DateTime, Integer, String, Float, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

def create_dynamic_model(table_name, column_names):
    class_name = table_name
    class_attributes = {
        "__tablename__": table_name,
        "id": Column(Integer, primary_key=True, autoincrement=True),
        "timestamp": Column(DateTime, default=datetime.utcnow, nullable=False),
    }
    for col_name in column_names:
        class_attributes[col_name] = Column(Float)
   
    DynamicModel = type(class_name, (Base,), class_attributes)
    # Define columns dynamically based on the input dictionary
    # for col_name in column_names:
    #     setattr(DynamicModel, col_name, Column(Float))
    return DynamicModel