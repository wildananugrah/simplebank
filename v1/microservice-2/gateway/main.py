from fastapi import FastAPI, Depends, FastAPI, Body, Request, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from controllers.customer import CustomerController
from controllers.account import AccountController
from controllers.historical_transaction import HistoricalTransactionController
from controllers.transaction import TransactionController
from controllers.payment import PaymentController
from controllers.session import SessionController
from schemas.customer import CustomerSchema, CustomerUserSchema, CustomerUserLoginSchema
from schemas.account import AccountSchema, AccountUpdateBalanceSchema
from schemas.transaction import TransferSchema
from schemas.deposit import DepositSchema
from schemas.payment import TaxInquirySchema, TaxPaymentSchema

import base64

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

tokens = ["admin"]
async def validate_token(token: str = Depends(oauth2_scheme)):
    cif_number = base64.b64decode(token.encode('ascii')).decode('ascii')
    if not CustomerController(db).select_by_cif(cif_number=cif_number):
        raise HTTPException(status_code=404, detail="Invalid Token")
    return cif_number

# customer
@app.post(
    "/customer",
    tags=["Customers"]
)
def post_customer(
    customer_req: CustomerSchema,
    response: Response
):
    _response =  CustomerController().create(customer_req)
    response.status_code = _response.status_code
    return _response.json()

@app.get(
    "/customers",
    tags=["Customers"]
)
def all_customer(
    response: Response,
    skip: int = 0, limit: int = 100,
):
    _response =  CustomerController().all(skip, limit)
    response.status_code = _response.status_code
    return _response.json()

@app.get(
    "/customer/cif",
    tags=["Customers"]
)
def detail_by_cif_customer(
    cif_number: str,
    response: Response
):
    _response =  CustomerController().select_by_cif(cif_number)
    response.status_code = _response.status_code
    return _response.json() 

@app.get(
    "/customer/id_number",
    tags=["Customers"]
)
def detail_by_id_number_customer(
    id_number: str,
    response: Response
):
    _response =  CustomerController().select_by_id_number(id_number)
    response.status_code = _response.status_code
    return _response.json() 

@app.delete(
    "/customer/cif",
    tags=["Customers"]
)
def detail_by_cif_customer(
    cif_number: str,
    response: Response
):
    _response =  CustomerController().delete_by_cif(cif_number)
    response.status_code = _response.status_code
    return _response.json() 

@app.delete(
    "/customer/id_number",
    tags=["Customers"]
)
def detail_by_id_number_customer(
    id_number: str,
    response: Response
):
    _response =  CustomerController().delete_by_id_number(id_number)
    response.status_code = _response.status_code
    return _response.json() 

@app.put(
    "/customer",
    tags=["Customers"]
)
def customer_update(
    customer_req: CustomerSchema,
    cif_number: str,
    response: Response
):
    _response =  CustomerController().update(cif_number, customer_req)
    response.status_code = _response.status_code
    return _response.json()

@app.put(
    "/customer_user",
    tags=["Customers"]
)
def update_customer_user(
    customer_req: CustomerUserSchema,
    response: Response
):
    _response =  CustomerController().update_customer_user(customer_req)
    response.status_code = _response.status_code
    return _response.json()

@app.post(
    "/customer/login",
    tags=["Customers"]
)
def customer_login(
    customer_req: CustomerUserLoginSchema,
    response: Response
):
    _response =  CustomerController().login(customer_req)
    response.status_code = _response.status_code
    return _response.json()

# account
@app.post(
    "/account",
    tags=["Customers"]    
)
def account_create(
    account_req: AccountSchema,
    response: Response
):
    _response =  AccountController().create(account_req)
    response.status_code = _response.status_code
    return _response.json()

@app.get(
    "/accounts",
    tags=["Accounts"]
)
def all_account(
    response: Response,
    skip: int = 0, limit: int = 100,
):
    _response =  AccountController().all(skip, limit)
    response.status_code = _response.status_code
    return _response.json()

@app.get(
    "/accounts/cif_number",
    tags=["Accounts"]
)
def all_account_by_cif_number(
    cif_number: str,
    response: Response,
    skip: int = 0, limit: int = 100
):
    _response =  AccountController().all_by_cif_number(cif_number, skip, limit)
    response.status_code = _response.status_code
    return _response.json()

@app.get(
    "/account",
    tags=["Accounts"]
)
def all_account_by_cif_number(
    account: str,
    response: Response
):
    _response =  AccountController().detail(account)
    response.status_code = _response.status_code
    return _response.json()

@app.delete(
    "/account",
    tags=["Accounts"]
)
def all_account_by_cif_number(
    account: str,
    response: Response
):
    _response =  AccountController().delete(account)
    response.status_code = _response.status_code
    return _response.json()

@app.post(
    "/account/update_balance",
    tags=["Accounts"]
)
def account_update_balance(
    account_req: AccountUpdateBalanceSchema,
    response: Response
):
    _response =  AccountController().update_balance(account_req)
    response.status_code = _response.status_code
    return _response.json()

# historical transaction
@app.get(
    "/historical_transaction",
    tags=["Accounts"]
)
def get_historical_transaction(
    account_number: str,
    response: Response,
    skip: int = 0, limit: int = 100
):
    _response =  HistoricalTransactionController().all(account_number, skip, limit)
    response.status_code = _response.status_code
    return _response.json()

# transactions
@app.post(
    "/transfer",
    tags=["Transactions"]
)
def transfer(transfer_req: TransferSchema, response: Response):
    _response =  TransactionController().transfer(transfer_req)
    response.status_code = _response.status_code
    return _response.json()

@app.post(
    "/deposit",
    tags=["Transactions"]
)
def transfer(deposit_req: DepositSchema, response: Response):
    _response =  TransactionController().deposit(deposit_req)
    response.status_code = _response.status_code
    return _response.json()

# payment
@app.post(
    "/bill/inquiry/tax",
    tags=["Payments"]
)
def bill_inquiry_tax(
    request: TaxInquirySchema,
    response: Response
):
    _response =  PaymentController().inquiry_tax(request)
    response.status_code = _response.status_code
    return _response.json()

@app.post(
    "/bill/payment/tax",
    tags=["Payments"]
)
def bill_payment_tax(
    request: TaxPaymentSchema,
    response: Response
):
    _response =  PaymentController().payment_tax(request)
    response.status_code = _response.status_code
    return _response.json()

# session
@app.post("/token", tags=["Tokens"])
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    _response =  SessionController().customer_user_login(CustomerUserLoginSchema(username=form_data.username, password=form_data.password))
    response.status_code = _response.status_code
    return _response.json()