from sqlalchemy import Column, Integer, String, DateTime 
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class TblHistoricalTransaction(Base):
    __tablename__ = "historical_transactions"

    id = Column(Integer, primary_key=True)
    transaction_type = Column(String)
    account_number = Column(String)
    amount = Column(Integer)
    journal_number = Column(String)
    current_balance = Column(Integer)
    description = Column(String)
    transaction_datetime = Column(DateTime, default=datetime.utcnow)