from typing import List, Optional
from pydantic import BaseModel

class AddHistoricalTransactionSchema(BaseModel):
    account_number: str 
    current_account_balance: int 
    amount: int 
    action: str 
    transaction_type: str