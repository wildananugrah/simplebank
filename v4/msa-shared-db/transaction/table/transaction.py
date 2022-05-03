from sqlalchemy import Column, Integer, String, DateTime 
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class TblTransaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    transaction_type = Column(String)
    journal_number = Column(String)
    from_account_number = Column(String)
    to_account_number = Column(String)
    bank_code = Column(String)
    amount = Column(Integer)
    transaction_datetime = Column(DateTime, default=datetime.utcnow)
    cif_number = Column(String)
    status = Column(String)
    description = Column(String, default="")