from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
import json

# engine = create_engine("postgresql+psycopg2://simplebankdb_user:simplebankdb_password@45.113.234.254:3000/simplebankdb") # monolith
engine = create_engine("postgresql+psycopg2://simplebankdb_user:simplebankdb_password@45.113.234.254:5000/simplebankdb") # other
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

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

#    accounts = relationship("TblAccount", back_populates="customer")

Base.metadata.create_all(engine)

FILENAME = "data/customer_1000.json"

with open(FILENAME) as f:
    counter = 0
    for line in f:
        customer = json.loads(line)
        # _customer.append((customer['username'], customer['password'], customer['email']))
        db_customer = TblCustomer(
            username=customer['username'],
            password=customer['password'],
            email=customer['email'],
            cif_number=customer['cif_number'],
            id_number=customer['id_number'],
            name=customer['name'],
            is_login=False,
        )
        session.add(db_customer)
        session.commit()
        counter += 1
        print(f"counter: {counter}")

print("DONE.")