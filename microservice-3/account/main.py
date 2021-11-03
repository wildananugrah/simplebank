from fastapi import FastAPI, Depends, FastAPI, Body, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from databases.db import Base, SessionLocal, engine
from controllers.account import AccountController
from schemas.account import AccountSchema, AccountUpdateBalanceSchema

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

# accounts
@app.post(
    "/account",
    tags=["Accounts"]
)
def post_account(
    account_req: AccountSchema,
    db: Session = Depends(get_db)
):
    return AccountController(db).create(account_req)

@app.get(
    "/accounts",
    tags=["Accounts"]
)
def all_account(
    db: Session = Depends(get_db),
    skip: int = 0, limit: int = 100
):
    return AccountController(db).all(skip, limit)

@app.get(
    "/accounts/cif_number",
    tags=["Accounts"]
)
def all_account(
    cif_number: str,
    db: Session = Depends(get_db),
    skip: int = 0, limit: int = 100
):
    return AccountController(db).select_by_cif_number(cif_number)

@app.get(
    "/account",
    tags=["Accounts"]
)
def detail_account(
    account: str,
    db: Session = Depends(get_db)
):
    return AccountController(db).detail(account)

@app.delete(
    "/account",
    tags=["Accounts"]
)
def delete_account(
    account: str,
    db: Session = Depends(get_db)
):
    return AccountController(db).delete(account)

@app.post(
    "/account/update_balance",
    tags=["Accounts"]
)
def update_balance(
    request: AccountUpdateBalanceSchema, 
    db: Session = Depends(get_db)
):
    return AccountController(db).update_balance(request)

# payments
@app.post(
    "/bill/inquiry/tax",
    tags=["Payments"]
)
def bill_inquiry_tax(
    request: TaxInquirySchema,
    db: Session = Depends(get_db),
):
    return PaymentController(db).tax_inquiry(request)

@app.post(
    "/bill/payment/tax",
    tags=["Payments"]
)
def bill_payment_tax(
    request: TaxPaymentSchema,
    db: Session = Depends(get_db),
):
    return PaymentController(db).tax_payment(request)

# transfer
@app.post(
    "/transfer",
    tags=["Transactions"]
)
def transfer(
    transfer_req: TransferSchema,
    db: Session = Depends(get_db)
):
    return TransactionController(db).transfer(transfer_req)

@app.post(
    "/deposit",
    tags=["Transactions"]
)
def deposit(
    deposit_req: DepositSchema,
    db: Session = Depends(get_db)
):
    return TransactionController(db).deposit(deposit_req)

@app.get(
    "/historical_transaction",
    tags=["Transactions"]
)
def historical_transaction(
    account_number: str, 
    db: Session = Depends(get_db),
    skip: int = 0, limit: int = 100
):
    return TransactionController(db).historical_transaction(account_number, skip, limit)