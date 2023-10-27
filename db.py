from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
import os

# Define the SQLite database file path
sqlite_db_path = "/home/wzero/modbus/mydatabase.db"

# Create a custom event listener to check if the database file exists
@event.listens_for(create_engine(f"sqlite:///{sqlite_db_path}", echo=True), 'connect')
def check_sqlite_db_exists(dbapi_connection, connection_record):
    if not os.path.isfile(sqlite_db_path):
        # If the database file doesn't exist, create it
        open(sqlite_db_path, 'w').close()

# Create the SQLite engine
sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)

# Your PostgreSQL engine creation remains unchanged
# postgres_engine = create_engine('postgresql+psycopg2://postgres:postgres@192.168.1.18:5432/test1')

def get_sqlite_session():
    return Session(sqlite_engine)

def get_postgres_session():
    return Session(postgres_engine)
