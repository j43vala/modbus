from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///mydatabase.db", echo=True) 

def get_session():
    return Session(engine)