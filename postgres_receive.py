# import sqlite3
# import time
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from datetime import datetime
# from database.models import DataRegister


# # Connect to SQLite and PostgreSQL databases
# try:
#     # sqlite_conn = sqlite3.connect('/home/wzero/modbus/mydatabase.db')  # Replace 'test.db' with your database file path
#     sqlite_db_path = "/home/wzero/modbus/mydatabase.db"
#     sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)
#     print("SQLite database connected successfully.")
#     Sqlite_Session = sessionmaker(bind=sqlite_engine)
#     sqlite_session = Sqlite_Session()

#     # Create a SQLAlchemy engine for PostgreSQL
#     PostgresSQL_engine = create_engine('postgresql://postgres:postgres@192.168.1.18:5432/test1')
#     print("PostgreSQL database connected successfully.")

#     # Create a session to interact with PostgreSQL
#     Session = sessionmaker(bind=PostgresSQL_engine)
#     PostgresSQL_session = Session()

#     # Define the interval (0.5 seconds in this case)
#     interval = 0.5

#     while True:
#         # Read data from SQLite
#         # sqlite_cursor = sqlite_conn.cursor()
#         # sqlite_cursor.execute("SELECT timestamp, reg_no, value FROM data_register")  # Include 'reg_no' in the query
#         # data = sqlite_cursor.fetchall()
#         data = sqlite_session.query(DataRegister).all()

#         # Insert data into PostgreSQL using SQLAlchemy
#         for row in data:
#             # timestamp_str, reg_no, value = row
#             # timestamp = datetime.fromisoformat(timestamp_str)

#             # timestamp_str = row.timestamp


#             PostgresSQL_data = DataRegister(timestamp=row.timestamp, reg_no=row.reg_no, value=row.value)  # Create an instance of the model
#             PostgresSQL_session.add(PostgresSQL_data)  # Add the instance to the session

#         # Commit the changes to PostgreSQL
#         PostgresSQL_session.commit()

#         # Delete successfully transferred data from SQLite
#         for row in data:
#             # timestamp_str, _, _ = row
#             # sqlite_cursor.execute("DELETE FROM data_register WHERE timestamp = ?", (timestamp_str,))

#             sqlite_session.delete(row)
#         sqlite_session.commit()

#         # Sleep for the specified interval
#         time.sleep(interval)

# except KeyboardInterrupt:
#     # Close connections on keyboard interrupt (Ctrl+C)
#     sqlite_conn.close()
#     PostgresSQL_session.close()
# except sqlite3.Error as e:
#     print("SQLite database connection error:", e)
#     # Handle the SQLite error here, e.g., log it or exit the program
# except Exception as e:
#     print("Error:", e)
#     # Handle other errors here


import sqlite3
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
# from database.models import DataRegister
from wzero_script import CustomDeviceTable

# Function to fetch data in batches
def fetch_data_in_batches(session, batch_size):
    offset = 0
    while True:
        data = session.query(CustomDeviceTable).limit(batch_size).offset(offset).all()
        if not data:
            break
        offset += batch_size
        yield data

# Connect to SQLite and PostgresSQL databases
try:
    sqlite_db_path = "/home/wzero/modbus/mydatabase.db"
    sqlite_engine = create_engine(f"sqlite:///{sqlite_db_path}", echo=True)
    print("SQLite database connected successfully.")
    Sqlite_Session = sessionmaker(bind=sqlite_engine)
    sqlite_session = Sqlite_Session()

    PostgresSQL_engine = create_engine('postgresql+psycopg2://postgres:postgres@192.168.1.18:5432/test1')
    print("PostgresSQL database connected successfully.")
    Session = sessionmaker(bind=PostgresSQL_engine)
    PostgresSQL_session = Session()

    interval = 0.5

    while True:
        # Fetch data from SQLite in batches of 1000
        for batch_data in fetch_data_in_batches(sqlite_session, 1000):
            # Insert data into PostgresSQL using SQLAlchemy
            for row in batch_data:
                PostgresSQL_data = CustomDeviceTable(timestamp=row.timestamp, reg_no=row.reg_no, value=row.value)
                PostgresSQL_session.add(PostgresSQL_data)

            # Commit the changes to PostgresSQL
            PostgresSQL_session.commit()

            # Delete successfully transferred data from SQLite
            for row in batch_data:
                sqlite_session.delete(row)
            sqlite_session.commit()

        # Sleep for the specified interval
        time.sleep(interval)

except KeyboardInterrupt:
    sqlite_session.close()
    PostgresSQL_session.close()
except sqlite3.Error as e:
    print("SQLite database connection error:", e)
except Exception as e:
    print("Error:", e)
