from dataclasses import dataclass
from exception.business_logic_exception import BusinessLogicException
from sp_config import *
from db import dbinstance
import requests, os

@dataclass
class Account:

    account_number: str = None
    current_balance: int = 0
    
    db = dbinstance.get_db()

    def detail(self, account_number):
        
        account = self.db.simplebank_db.accounts.find_one({ 'account_number' : account_number }, { '_id' : False })
        if account:
            return account
        else:
            raise BusinessLogicException(f'Can not find account_number: {account_number}')
    
    def update(self, account_number, current_balance):
        
        self.detail(account_number)

        query = { 'account_number' : account_number }
        new_value = { 'balance' : current_balance }

        self.db.simplebank_db.accounts.update_one(query, { '$set' : new_value })

        return self.detail(account_number)
