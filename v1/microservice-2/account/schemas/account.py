from typing import List, Optional
from pydantic import BaseModel

class AccountSchema(BaseModel):
    cif_number: str
    currency: str
    balance: int

class AccountUpdateBalanceSchema(BaseModel):
    amount: int
    account: str
    action: str