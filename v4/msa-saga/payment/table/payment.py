from sqlalchemy import Column, Integer, String, DateTime 
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class TblPayment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, default="")
    bill_id = Column(String)
    cif_number = Column(String)
    from_account_number = Column(String)
    amount = Column(Integer)
    journal_number = Column(String, default="")
    transaction_type = Column(String)
    transaction_datetime = Column(DateTime, default=datetime.utcnow)
    description = Column(String)
    message = Column(String, default="Transaction in progress")
    status = Column(String, default="IN_PROGRESS")
    