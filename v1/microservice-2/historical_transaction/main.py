from fastapi import FastAPI, Depends, FastAPI, Body, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from databases.db import Base, SessionLocal, engine
from controllers.historical_transaction import HistoricalTransactionController
from schemas.historical_transaction import AddHistoricalTransactionSchema

import base64

app = FastAPI()

Base.metadata.create_all(bind=engine)
db = SessionLocal()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

tokens = ["admin"]
async def validate_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    cif_number = base64.b64decode(token.encode('ascii')).decode('ascii')
    if not CustomerController(db).select_by_cif(cif_number=cif_number):
        raise HTTPException(status_code=404, detail="Invalid Token")
    return cif_number

# token
@app.post("/token", tags=["Tokens"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return CustomerController(db).customer_user_login(CustomerUserLoginSchema(username=form_data.username, password=form_data.password))

@app.get(
    "/historical_transaction",
    tags=["Transactions"]
)
def historical_transaction(
    account_number: str, 
    db: Session = Depends(get_db),
    skip: int = 0, limit: int = 100
):
    return HistoricalTransactionController(db).historical_transaction(account_number, skip, limit)

@app.post(
    "/historical_transaction",
    tags=["Transaction"]
)
def add_historical_transaction(
    request: AddHistoricalTransactionSchema, 
    db: Session = Depends(get_db),
):
    return HistoricalTransactionController(db).add(request)

@app.get(
    "/generate_journal_number",
    tags=["Transactions"]
)
def generate_journal_number(
    db: Session = Depends(get_db)
):
    return HistoricalTransactionController(db).generate_journal_number()