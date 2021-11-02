from dotenv import load_dotenv
from schemas.customer import CustomerUserLoginSchema
from fastapi import HTTPException

import requests, os

class SessionController():

    def __init__(self):
        load_dotenv()
        self.host = os.environ.get("CUSTOMER_HOST")

    def customer_user_login(self, request: CustomerUserLoginSchema):
        return requests.post(f"{self.host}/customer/login", json=request.dict())