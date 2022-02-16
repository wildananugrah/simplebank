from databases.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class CustomerDB(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    id_number = Column(String, unique=True, index=True)
    cif_number = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String)
    username = Column(String, index=True, default="")
    password = Column(String, index=True, default="")