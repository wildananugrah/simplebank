from databases.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class AccountDB(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    cif_number = Column(String, index=True)
    account = Column(String, unique=True, index=True)
    currency = Column(String)
    balance = Column(Integer())