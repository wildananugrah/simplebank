from sqlalchemy import Column, Integer, String, DateTime 
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class TblInterbankTransfer(Base):
    __tablename__ = "interbank_transfers"

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String)
    from_account_number = Column(String)
    from_bank_code = Column(String)
    to_account_number = Column(String)
    to_bank_code = Column(String)
    amount = Column(Integer)
    journal_number = Column(String, default="")
    cif_number = Column(String)
    transaction_datetime = Column(DateTime, default=datetime.utcnow)
    description = Column(String, default="")
    status = Column(String, default="DONE")
    message = Column(String, default="Transaction in progress")