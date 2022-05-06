from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class TblAccount(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    cif_number = Column(String)
    account_number = Column(String)
    currency = Column(String)
    balance = Column(Integer)