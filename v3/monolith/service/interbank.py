from dataclasses import dataclass
from abc import ABC, abstractmethod
from exception.service_exception import ServiceException
from datetime import datetime

import requests, os

class InterbankAbstract(ABC):
    """ represent base interbank service """

    @abstractmethod
    def inquiry(self, account_number):
        pass

    @abstractmethod
    def notify(self, acccount_number, amount, journal_number, transaction_id, transaction_datetime):
        pass

@dataclass
class Interbank(InterbankAbstract):

    host: str = os.getenv("SIM_INTERBANK_HOST")
    # host: str = "http://45.113.232.164:3000"
    from_account_number: str = None
    from_bank_code: str = None 
    acccount_number: str = None 
    bank_code: str = None 
    amount: int = 0 
    journal_number: str = None 
    transaction_id: str = None 
    transaction_datetime: datetime = datetime.now()
    description: str = None

    invalid_status_code = {
        400 : 'Invalid input account number',
        404 : 'Interbank account number does not exist'
    }

    valid_status_code = [200, 201]

    def inquiry(self, account_number, bank_code):
        
        response = requests.get(f"{self.host}/?account_number={account_number}&bank_code={bank_code}")

        if response and response.status_code in self.valid_status_code:
            return response.json()
        elif response.status_code in self.invalid_status_code:
            return ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke interbank service inquiry.")

    
    def notify(self):

        data = {
            "account_number" : self.acccount_number,
            "bank_code" : self.bank_code,
            "amount" : self.amount,
            "source_account_number" : self.from_account_number,
            "source_bank_code" : self.from_bank_code,
            "transaction_datetime": self.transaction_datetime,
            "description": self.description
        }

        response = requests.post(f"{self.host}/", json=data)

        if response and response.status_code in self.valid_status_code:
            return response.json()
        else:
            raise ServiceException(f"Can not invoke interbank service notify.")