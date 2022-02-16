from dotenv import load_dotenv
from fastapi import HTTPException
from schemas.payment import TaxInquirySchema, TaxPaymentSchema

import requests, os

class PaymentController():

    def __init__(self):
        load_dotenv()
        self.payment_host = os.environ.get("PAYMENT_HOST")

    def inquiry_tax(self, request: TaxInquirySchema):
        return requests.post(f"{self.payment_host}/bill/inquiry/tax", json=request.dict())

    def payment_tax(self, request: TaxPaymentSchema):
        return requests.post(f"{self.payment_host}/bill/payment/tax", json=request.dict())