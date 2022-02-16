from fastapi import FastAPI, Depends, FastAPI, Body, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from databases.db import Base, SessionLocal, engine
from controllers.session import SessionController
from schemas.customer import CustomerUserLoginSchema

import base64

app = FastAPI()

Base.metadata.create_all(bind=engine)
db = SessionLocal()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

tokens = ["admin"]
async def validate_token(token: str = Depends(oauth2_scheme)):
    cif_number = base64.b64decode(token.encode('ascii')).decode('ascii')
    if not SessionController().select_by_cif(cif_number=cif_number):
        raise HTTPException(status_code=404, detail="Invalid Token")
    return cif_number

# token
@app.post("/token", tags=["Tokens"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return SessionController().customer_user_login(CustomerUserLoginSchema(username=form_data.username, password=form_data.password))