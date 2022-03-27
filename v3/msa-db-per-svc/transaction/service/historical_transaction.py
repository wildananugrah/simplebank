from dataclasses import dataclass
from exception.service_exception import ServiceException
from sp_config import *
from datetime import datetime
import requests, os

@dataclass
class HistoricalTransaction:

    host: str = HISTORICAL_TRANSACTION_HOST
    transaction_type: str = None
    account_number: str = None
    amount: int = 0
    journal_number: str = str
    current_balance: int = 0
    description: str = None
    
    invalid_status_code = {
        400 : 'Invalid cif number number',
        404 : 'Interbank cif number does not exist'
    }

    valid_status_code = [200, 201]

    def save(self):
        
        data = {
            'transaction_type': self.transaction_type,
            'account_number': self.account_number,
            'amount': self.amount,
            'journal_number': self.journal_number,
            'current_balance': self.current_balance,
            'description': self.description
        }

        response = requests.post(f"{self.host}/historical_transaction/", json=data)

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke historical transaction save.")

        # return True
    
    def save_many(self, documents):
        response = requests.post(f"{self.host}/historical_transaction/many/", json=documents)

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke historical transaction save many.")
