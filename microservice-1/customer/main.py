from fastapi import FastAPI, Depends, FastAPI, Body, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from databases.db import Base, SessionLocal, engine
from databases.customer import CustomerDB
from controllers.customer import CustomerController
from schemas.customer import CustomerSchema, CustomerUserSchema, CustomerUserLoginSchema

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

# customer
@app.post(
    "/customer",
    tags=["Customers"]
)
def post_customer(
    customer_req: CustomerSchema,
    db: Session = Depends(get_db)
):
    return CustomerController(db).create(customer_req)

@app.put(
    "/customer",
    tags=["Customers"]
)
def update_customer(
    customer_req: CustomerSchema,
    cif_number: str,
    db: Session = Depends(get_db)
):
    return CustomerController(db).update_by_cif(customer_req, cif_number)

@app.put(
    "/customer_user",
    tags=["Customers"]
)
def update_username_password(
    customer_user_req: CustomerUserSchema,
    db: Session = Depends(get_db)
):
    return CustomerController(db).update_username_password(customer_user_req)

@app.post(
    "/customer/login",
    tags=["Customers"]
)
def login(
    customer_login_req: CustomerUserLoginSchema,
    db: Session = Depends(get_db)
):
    return CustomerController(db).customer_user_login(customer_login_req)

@app.get(
    "/customers",
    tags=["Customers"]
)
def all_customer(
    db: Session = Depends(get_db),
    skip: int = 0, limit: int = 100
):
    return CustomerController(db).all(skip, limit)

@app.get(
    "/customer/cif",
    tags=["Customers"]
)
def detail_by_cif_customer(
    cif_number: str,
    db: Session = Depends(get_db)
):
    return CustomerController(db).select_by_cif(cif_number)

@app.get(
    "/customer/id_number",
    tags=["Customers"]
)
def detail_by_id_number_customer(
    id_number: str,
    db: Session = Depends(get_db)
):
    return CustomerController(db).select_by_id_number(id_number)

@app.delete(
    "/customer/cif",
    tags=["Customers"]
)
def delete_by_cif_customer(
    cif_number: str,
    db: Session = Depends(get_db)
):
    return CustomerController(db).delete_by_cif(cif_number)

@app.delete(
    "/customer/id_number",
    tags=["Customers"]
)
def delete_by_cif_customer(
    id_number: str,
    db: Session = Depends(get_db)
):
    return CustomerController(db).delete_by_id_number(id_number)