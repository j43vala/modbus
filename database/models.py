# from typing import List
# from typing import Optional
# from sqlalchemy import  Column, ForeignKey,Float, Integer, DateTime, String
# from sqlalchemy import String
# import sqlalchemy
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from datetime import datetime

# Base = declarative_base()

# class DataRegister(Base):
#     __tablename__ = "data_register"

#     id = Column(Integer, primary_key=True)
#     reg_no = Column(Integer)
#     value = Column(Integer)



from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Float, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class DataRegister(Base):
    __tablename__ = "data_register"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    reg_no = Column(Integer)
    value = Column(Integer)
