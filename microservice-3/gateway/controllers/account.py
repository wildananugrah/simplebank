
from schemas.account import AccountSchema, AccountUpdateBalanceSchema
from dotenv import load_dotenv
from fastapi import HTTPException

import requests, os

class AccountController():

    def __init__(self):
        load_dotenv()
        self.customer_host = os.environ.get("ACCOUNT_HOST")

    def create(self, account: AccountSchema):
        return requests.post(f"{self.customer_host}/account", json=account.dict())

    def all(self, skip: int = 0, limit: int = 100):
        return requests.get(f"{self.customer_host}/accounts?skip={skip}&limit={limit}")
    
    def all_by_cif_number(self, cif_number: str, skip: int = 0, limit: int = 100):
        return requests.get(f"{self.customer_host}/accounts/cif_number?cif_number={cif_number}&skip={skip}&limit={limit}")

    def detail(self, account_number: str):
        return requests.get(f"{self.customer_host}/account?account={account_number}")
    
    def delete(self, account_number: str):
        return requests.delete(f"{self.customer_host}/account?account={account_number}")

    def update_balance(self, account: AccountUpdateBalanceSchema):
        return requests.post(f"{self.customer_host}/account/update_balance", json=account.dict())