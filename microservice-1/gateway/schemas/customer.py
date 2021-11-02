from typing import List, Optional
from pydantic import BaseModel

class CustomerSchema(BaseModel):
    name: str
    id_number: str
    email: str

class CustomerUserSchema(BaseModel):
    username: str
    password: str
    cif_number: str

class CustomerUserLoginSchema(BaseModel):
    username: str
    password: str