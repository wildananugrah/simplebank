from dotenv import load_dotenv
from schemas.deposit import DepositSchema
from schemas.transaction import TransferSchema
from fastapi import HTTPException

import requests, os

class TransactionController():

    def __init__(self):
        load_dotenv()
        self.transaction_host = os.environ.get("TRANSACTION_HOST")

    def deposit(self, deposit: DepositSchema):
        return requests.post(f"{self.transaction_host}/deposit", json=deposit.dict())
    
    def transfer(self, transfer: TransferSchema):
        return requests.post(f"{self.transaction_host}/transfer", json=transfer.dict())