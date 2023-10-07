import sqlite3
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database.models import DataRegister


# Connect to SQLite and PostgreSQL databases
try:
    # sqlite_conn = sqlite3.connect('/home/wzero/modbus/mydatabase.db')  # Replace 'test.db' with your database file path
    sqlite_db_path = "/home/wzero/modbus/mydatabase.db"
    sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)
    print("SQLite database connected successfully.")
    Sqlite_Session = sessionmaker(bind=sqlite_engine)
    sqlite_session = Sqlite_Session()

    # Create a SQLAlchemy engine for PostgreSQL
    postgres_engine = create_engine('postgresql://postgres:postgres@192.168.1.18:5432/test1')
    print("PostgreSQL database connected successfully.")

    # Create a session to interact with PostgreSQL
    Session = sessionmaker(bind=postgres_engine)
    postgres_session = Session()

    # Define the interval (0.5 seconds in this case)
    interval = 0.5

    while True:
        # Read data from SQLite
        # sqlite_cursor = sqlite_conn.cursor()
        # sqlite_cursor.execute("SELECT timestamp, reg_no, value FROM data_register")  # Include 'reg_no' in the query
        # data = sqlite_cursor.fetchall()
        data = sqlite_session.query(DataRegister).all()

        # Insert data into PostgreSQL using SQLAlchemy
        for row in data:
            # timestamp_str, reg_no, value = row
            # timestamp = datetime.fromisoformat(timestamp_str)

            # timestamp_str = row.timestamp


            postgres_data = DataRegister(timestamp=row.timestamp, reg_no=row.reg_no, value=row.value)  # Create an instance of the model
            postgres_session.add(postgres_data)  # Add the instance to the session

        # Commit the changes to PostgreSQL
        postgres_session.commit()

        # Delete successfully transferred data from SQLite
        for row in data:
            # timestamp_str, _, _ = row
            # sqlite_cursor.execute("DELETE FROM data_register WHERE timestamp = ?", (timestamp_str,))

            sqlite_session.delete(row)
        sqlite_session.commit()

        # Sleep for the specified interval
        time.sleep(interval)

except KeyboardInterrupt:
    # Close connections on keyboard interrupt (Ctrl+C)
    sqlite_conn.close()
    postgres_session.close()
except sqlite3.Error as e:
    print("SQLite database connection error:", e)
    # Handle the SQLite error here, e.g., log it or exit the program
except Exception as e:
    print("Error:", e)
    # Handle other errors here