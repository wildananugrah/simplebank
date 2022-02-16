from schemas.customer import CustomerSchema, CustomerUserSchema, CustomerUserLoginSchema
from dotenv import load_dotenv
from fastapi import HTTPException

import requests, os

class CustomerController():

    def __init__(self):
        load_dotenv()
        self.customer_host = os.environ.get("CUSTOMER_HOST")

    def create(self, customer: CustomerSchema):
        return requests.post(f"{self.customer_host}/customer", json=customer.dict())

    def all(self, skip: int = 0, limit: int = 100):
        return requests.get(f"{self.customer_host}/customers?skip={skip}&limit={limit}")
    
    def select_by_cif(self, cif_number: str):
        return requests.get(f"{self.customer_host}/customer/cif?cif_number={cif_number}")
    
    def select_by_id_number(self, id_number: str):
        return requests.get(f"{self.customer_host}/customer/id_number?id_number={id_number}")

    def delete_by_cif(self, cif_number: str):
        return requests.delete(f"{self.customer_host}/customer/cif?cif_number={cif_number}")
    
    def delete_by_id_number(self, id_number: str):
        return requests.delete(f"{self.customer_host}/customer/id_number?id_number={id_number}")

    def update(self, cif_number: str, customer: CustomerSchema):
        return requests.put(f"{self.customer_host}/customer?cif_number={cif_number}", json=customer.dict())
    
    def update_customer_user(self, customer: CustomerUserSchema):
        return requests.put(f"{self.customer_host}/customer_user", json=customer.dict())
    
    def login(self, customer: CustomerUserLoginSchema):
        return requests.post(f"{self.customer_host}/customer/login", json=customer.dict())