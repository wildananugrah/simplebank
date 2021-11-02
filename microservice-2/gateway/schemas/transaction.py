from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class TransferSchema(BaseModel):
    to_account_number: str
    from_account_number: str
    amount: int

class TransferOKSchema(BaseModel):
    from_account_number: str
    to_account_number: str
    amount: int
    timestamp: datetime
    journal_number: str