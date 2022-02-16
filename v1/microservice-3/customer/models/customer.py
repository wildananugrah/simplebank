from databases.customer import CustomerDB
from sqlalchemy import and_

class CustomerModel():
    def __init__(self, db=None):
        self.db = db

    def create(self, customer_dict):
        db_customer = CustomerDB(**customer_dict)
        self.db.add(db_customer)
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def select_by_cif(self, cif_number):
        return self.db.query(CustomerDB).filter(CustomerDB.cif_number == cif_number).first()

    def select_by_id_number(self, id_number):
        return self.db.query(CustomerDB).filter(CustomerDB.id_number == id_number).first()

    def select_by_username(self, username):
        return self.db.query(CustomerDB).filter(CustomerDB.username == username).first()

    def delete(self, db_customer):
        self.db.delete(db_customer)
        self.db.commit()
        return True

    def all(self, skip: int = 0, limit: int = 100):
        return self.db.query(CustomerDB).offset(skip).limit(limit).all()

    def update(self, db_customer, customer):
        db_customer.name = customer.name
        db_customer.email = customer.email
        db_customer.id_number = customer.id_number
        self.db.commit()
        self.db.refresh(db_customer)

        return db_customer

    def update_username_password(self, db_customer, username, password):
        db_customer.username = username
        db_customer.password = password
        self.db.commit()
        self.db.refresh(db_customer)
        return db_customer

    def login(self, username, password):
        return self.db.query(CustomerDB).filter(and_(CustomerDB.username == username, CustomerDB.password == password)).first()