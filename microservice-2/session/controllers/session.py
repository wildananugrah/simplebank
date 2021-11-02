from models.session import SessionModel
from fastapi import HTTPException
from schemas.customer import CustomerUserLoginSchema
from models.session import SessionModel

import random, string, base64

class SessionController():
    
    def __init__(self):
        self.model = SessionModel()

    def customer_user_login(self, request: CustomerUserLoginSchema):
        login = self.model.login(request.username, request.password)
        if login == False:
            raise HTTPException(status_code=401, detail="Invalid username/password")
        else:
            return login