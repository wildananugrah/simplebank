from models.tax import TaxPayment
from models.account import AccountModel
from schemas.payment import TaxInquirySchema, TaxPaymentSchema
from fastapi import HTTPException
from datetime import datetime
from dotenv import load_dotenv
import random, string, os

HOST = os.environ.get("SIMULATOR_HOST")
TAX_URL = f"{HOST}/tax"
load_dotenv()

class PaymentController():
    def __init__(self, db):
        self.db = db

    def tax_inquiry(self, request: TaxInquirySchema):
        start = datetime.now()
        print(TAX_URL)
        response = TaxPayment(TAX_URL, self.db).inquiry(bill_id=request.bill_id)
        print(response)
        if response.status_code == 200:
            return {
                'status' : 'SUCCESS',
                'response_time' : datetime.now() - start,
                'host_response' : response.json()
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid Inquiry Tax") 

    def tax_payment(self, request: TaxPaymentSchema):
        start = datetime.now()
        
        account_model = AccountModel(self.db)
        db_account = account_model.detail(account=request.account_number)

        if not db_account:
            raise HTTPException(status_code=400, detail="Invalid Account Number") 

        if db_account['balance'] < request.amount:
            raise HTTPException(status_code=400, detail="Unsufficient fund") 

        response = TaxPayment(TAX_URL, self.db).payment(bill_id=request.bill_id, account_number=request.account_number, cif_number=db_account['cif_number'], amount=request.amount)
        if response.status_code == 200:
            return {
                'status' : 'SUCCESS',
                'response_time' : datetime.now() - start,
                'host_response' : response.json()
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid Inquiry Tax")