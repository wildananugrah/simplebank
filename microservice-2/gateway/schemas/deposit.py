from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class DepositSchema(BaseModel):
    account_number: str
    amount: int

class DepositOKSchema(BaseModel):
    account_number: str
    balance: int
    timestamp: datetime
    journal_number: str