from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class TaxInquirySchema(BaseModel):
    bill_id: str

class TaxPaymentSchema(BaseModel):
    bill_id: str
    account_number: str
    amount: int