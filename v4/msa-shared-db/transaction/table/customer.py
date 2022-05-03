from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class TblCustomer(Base):
   __tablename__ = 'customers'
   id = Column(Integer, primary_key=True)
   username = Column(String)
   password = Column(String)
   email = Column(String)
   cif_number = Column(String, unique=True, index=True)
   id_number = Column(String)
   name = Column(String)
   is_login = Column(Boolean)
   session_id = Column(String, default="")

   accounts = relationship("TblAccount", back_populates="customer")