from dataclasses import dataclass
from exception.service_exception import ServiceException
from sp_config import *
import requests, os

@dataclass
class Account:

    host: str = ACCOUNT_HOST
    account_number: str = None
    current_balance: int = 0
    
    invalid_status_code = {
        400 : 'Invalid account number number',
        404 : 'Account number does not exist'
    }

    valid_status_code = [200, 201]

    def detail(self, account_number):
        
        response = requests.get(f"{self.host}/account/?account_number={account_number}")

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke detail.")
    
    def update(self, account_number, current_balance):
        
        data = {
            'account_number' : account_number,
            'current_balance' : current_balance
        }

        response = requests.put(f"{self.host}/account/", json=data)

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke update account.")
    
    def update_many(self, documents):

        response = requests.put(f"{self.host}/account/many/", json=documents)

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke update many accounts.")

    def settlement(self, from_account_number, to_account_number, amount):

        data = {
            "from_account_number" : from_account_number,
            "to_account_number" : to_account_number,
            "amount" : amount
        }

        response = requests.post(f"{self.host}/account/settlement/", json=data)

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke settlement account.")
    
    def debit(self, account_number, amount):

        data = {
            "account_number" : account_number,
            "amount" : amount
        }

        response = requests.post(f"{self.host}/account/debit/", json=data)

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke debit account.")
    
    def credit(self, account_number, amount):

        data = {
            "account_number" : account_number,
            "amount" : amount
        }

        response = requests.post(f"{self.host}/account/credit/", json=data)

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke settlement account.")
