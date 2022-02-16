from databases.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class H2HLookupDB(Base):
    __tablename__ = "h2h_lookups"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(String, index=True)
    bill_type = Column(String, index=True)
    transaction_type = Column(String, index=True)
    account_number = Column(String, index=True, default="")
    cif_number = Column(String, index=True, default="")
    action = Column(String, index=True)
    status = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow())