from dataclasses import dataclass
from abc import ABC, abstractmethod
from exception.service_exception import ServiceException
from datetime import datetime

import requests, os

class PaymentAbstract(ABC):

    """ represent base payment """

    @abstractmethod
    def inquiry(self):
        raise NotImplementedError

    @abstractmethod
    def pay(self):
        raise NotImplementedError

class Payment(PaymentAbstract):

    """ represent base payment """

    @abstractmethod
    def inquiry(self):
        raise NotImplementedError

    @abstractmethod
    def pay(self):
        raise NotImplementedError

@dataclass
class EletricalBillPayment(PaymentAbstract):

    """ represent eletrical bill payment entity """

    host: str = os.getenv("SIM_BILLPAYMENT_HOST")
    # host: str = "http://45.113.232.164:3010"
    bill_id: str = None
    journal_number: str = None
    description: str = None

    invalid_status_code = {
        400 : 'Invalid input billId',
        404 : 'Interbank BillId does not exist'
    }

    valid_status_code = [200, 201]

    def inquiry(self, bill_id):

        response = requests.get(f"{self.host}/?bill_id={bill_id}")

        if response and response.status_code in self.valid_status_code:
            return response.json()
        elif response.status_code in self.invalid_status_code:
            return ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke interbank service inquiry.")

    def pay(self):
        data = {
            "bill_id" : self.bill_id,
            "journal_number" : self.journal_number,
            "description" : self.description
        }

        response = requests.post(f"{self.host}/", json=data)

        if response and response.status_code in self.valid_status_code:
            return response.json()
        else:
            raise ServiceException(f"Can not invoke interbank service inquiry.")
