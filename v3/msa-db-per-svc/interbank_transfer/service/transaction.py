from dataclasses import dataclass
from exception.service_exception import ServiceException
from sp_config import *
import requests, os

@dataclass
class Transaction:

    host: str = TRANSACTION_HOST
    from_account_number: str = None
    transaction_type: str = None
    cif_number: str = None
    amount: int = 0
    journal_number: str = None
    description: str = None
    
    invalid_status_code = {
        400 : 'Invalid cif number number',
        404 : 'Interbank cif number does not exist'
    }

    valid_status_code = [200, 201]

    def debit(self):
        data = {
            "from_account_number": self.from_account_number,
            "transaction_type": self.transaction_type,
            "cif_number": self.cif_number,
            "amount": self.amount,
            "description": self.description
        }
        response = requests.post(f"{self.host}/transaction/debit/", json=data)

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            print(response.status_code)
            raise ServiceException(f"Can not invoke interbank service inquiry.")
    
    def reversal(self):
        data = {
            "account_number": self.from_account_number,
            "amount": self.amount,
            "journal_number": self.journal_number
        }
        response = requests.post(f"{self.host}/transaction/reversal/", json=data)

        if response and response.status_code in self.valid_status_code:
            return response.json()['data']
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke interbank service inquiry.")
