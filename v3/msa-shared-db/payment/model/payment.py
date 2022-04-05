from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from uuid import uuid4
from datetime import datetime
from service.transaction import DebitTransaction
from service.billpayment import EletricalBillPayment as EBPService

class PaymentAbstract(ABC):

    @abstractmethod
    def inquiry(self):
        raise NotImplementedError

    @abstractmethod
    def pay(self):
        raise NotImplementedError
    
    @abstractmethod
    def save(self):
        raise NotImplementedError

@dataclass
class EletricalBillPayment(PaymentAbstract):

    """ represent eletrical bill payment entity """

    bill_id: str = None
    amount: int = 0
    description: str = None
    from_account_number: str = None
    cif_number: str = None
    payment: EBPService = EBPService()
    transaction: DebitTransaction = DebitTransaction()
    transaction_type: str = "ELETRICAL_BILLPAYMENT"
    
    db = dbinstance.get_db()
    journal_number: str = None
    
    def save(self, data):
        try:
            self.db.simplebank_db.payments.insert_one(data)
            return True
        except Exception as error:
            Exception(f"Internal server error: {str(error)}")

    def inquiry(self, bill_id):
        return self.payment.inquiry(bill_id)

    def pay(self):
        try:
            transaction_datetime = datetime.now().strftime("%d-%m-%Y %H:%I%S")
                
            # invoke transaction to retrieve journal number.
            self.transaction.from_account_number = self.from_account_number
            self.transaction.transaction_type = self.transaction_type
            self.transaction.cif_number = self.cif_number
            self.transaction.amount = self.amount
            self.transaction.description = self.description
            self.journal_number = self.transaction.debit()

            # invoke eletrical payment service
            self.payment.bill_id = self.bill_id
            self.payment.journal_number = self.journal_number
            self.payment.description = self.description
            response = self.payment.pay()

            # save transaction
            self.save({
                'from_account_number' : self.from_account_number,
                "amount" : self.amount,
                "journal_number" : self.journal_number,
                "transaction_type": self.transaction_type,
                "transaction_datetime" : transaction_datetime,
                "description" : self.description,
                "status" : "DONE",
                "response" : response
            })

            return self.journal_number

        except ServiceException as error:
            self.transaction.from_account_number = self.from_account_number
            self.transaction.amount = self.amount
            self.transaction.journal_number = self.journal_number
            self.journal_number = self.transaction.reversal()

            self.save({
                'from_account_number' : self.from_account_number,
                "amount" : self.amount,
                "journal_number" : self.journal_number,
                "transaction_type": self.transaction_type,
                "transaction_datetime" : transaction_datetime,
                "description" : self.description,
                "status" : "REVERSED",
                "response" : {}
            })
            raise ServiceException(f"Can not invoke eletrical payment service. detail: {error}")

        except Exception as error:
            raise Exception(f"Internal server error. {error}")