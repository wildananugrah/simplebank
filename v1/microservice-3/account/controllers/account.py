from models.account import AccountModel
from views.account import AccountView
from schemas.account import AccountSchema, AccountUpdateBalanceSchema
from fastapi import HTTPException

import random, string

class AccountController():
    def __init__(self, db):
        self.model = AccountModel(db)
        self.view = AccountView()

    def generate_account_number(self, size=10):
        account_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_account_number = self.select_by_account_number(account_number)
        if db_account_number:
            self.generate_account_number()
        return account_number
    
    def select_by_account_number(self, account_number):
        return self.model.detail(account_number)

    def create(self, account: AccountSchema):
        account_dict = account.dict()
        account_dict['account'] = self.generate_account_number()
        return self.model.create(account_dict)

    def detail(self, account: str):
        db_account = self.select_by_account_number(account)
        if not db_account:
            raise HTTPException(status_code=404, detail="Account Number doesn't exist") 

        return db_account

    def delete(self, account: str):
        db_account = self.select_by_account_number(account)
        if not db_account:
            raise HTTPException(status_code=404, detail="Account Number doesn't exist") 

        return self.model.delete(db_account)

    def all(self, skip: int = 0, limit: int = 100):
        return self.model.all(skip, limit)

    def update_balance(self, request: AccountUpdateBalanceSchema):
        db_account = self.select_by_account_number(request.account)
        if not db_account:
            raise HTTPException(status_code=404, detail="Account Number doesn't exist") 

        if db_account.balance < request.amount and request.action == "DEBIT":
            raise HTTPException(status_code=400, detail="Unsufficient Fund") 

        result = self.model.update_balance(request.account, request.action, request.amount)
        return { 'balance' : result.balance, 'account' : result.account }

    def select_by_cif_number(self, cif_number: str):
        return self.model.select_by_cif_number(cif_number=cif_number)