from models.customer import CustomerModel
from views.customer import CustomerView
from schemas.customer import CustomerSchema, CustomerUserSchema, CustomerUserLoginSchema
from fastapi import HTTPException

import random, string, base64

class CustomerController():
    def __init__(self, db):
        self.model = CustomerModel(db)
        self.view = CustomerView()

    def generate_cif_number(self, size=10):
        cif_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_cif_number = self.select_by_cif(cif_number)
        if db_cif_number:
            self.generate_cif_number()
        return cif_number

    def select_by_cif(self, cif_number):
        return self.model.select_by_cif(cif_number)

    def select_by_id_number(self, id_number):
        return self.model.select_by_id_number(id_number)

    def select_by_username(self, username):
        return self.model.select_by_username(username)

    def detail_cif(self, cif_number):
        db_customer = self.select_by_cif(cif_number)
        if db_customer:
            return db_customer
        else:
            raise HTTPException(status_code=404, detail="ID Number not found!")

    def detail_id_number(self, id_number):
        db_customer = self.select_by_id_number(id_number)
        if db_customer:
            return db_customer
        else:
            raise HTTPException(status_code=404, detail="ID Number not found!") 

    def create(self, customer: CustomerSchema):
        customer_dict = customer.dict()
        customer_dict['cif_number'] = self.generate_cif_number()

        if self.select_by_id_number(customer_dict['id_number']):
            raise HTTPException(status_code=400, detail="ID Number already registered") 

        return self.model.create(customer_dict)

    def delete_by_cif(self, cif_number):
        db_customer = self.select_by_cif(cif_number)
        if not db_customer:
            raise HTTPException(status_code=400, detail="CIF Number doesn't exist")

        return self.model.delete(db_customer)

    def delete_by_id_number(self, id_number):
        db_customer = self.select_by_id_number(id_number)
        if not db_customer:
            raise HTTPException(status_code=400, detail="ID Number doesn't exist")
        
        return self.model.delete(db_customer)

    def update_by_cif(self, customer: CustomerSchema, cif_number: str):
        db_customer = self.select_by_cif(cif_number)
        if not db_customer:
            raise HTTPException(status_code=400, detail="CIF Number doesn't exist")
        
        return self.model.update(db_customer, customer)
    
    def all(self, skip: int = 0, limit: int = 100):
        return self.model.all(skip, limit)

    def update_username_password(self, customer: CustomerUserSchema):
        db_customer = self.select_by_cif(customer.cif_number)
        
        if not db_customer:
            raise HTTPException(status_code=400, detail="CIF Number doesn't exist")

        db_customer_2 = self.select_by_username(customer.username)
        if db_customer_2:
            raise HTTPException(status_code=400, detail="Username is not available")

        return self.model.update_username_password(db_customer, customer.username, customer.password)

    def customer_user_login(self, customer: CustomerUserLoginSchema):
        db_customer = self.model.login(username=customer.username, password=customer.password)
        if not db_customer:
            raise HTTPException(status_code=404, detail="Invalid username/password")
        return {"access_token": base64.b64encode(db_customer.cif_number.encode('ascii')), "token_type": "bearer"}