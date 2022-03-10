from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from uuid import uuid4
from datetime import datetime
from service.transaction import Transaction
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
    db = dbinstance.get_db().simplebank_db
    payment: EBPService = EBPService()
    transaction: Transaction = Transaction()
    transaction_type: str = "ELETRICAL_BILLPAYMENT"

    def generate_transaction_id(self, size=10):
        transaction_id = ''.join(random.choice(string.digits) for _ in range(size))
        db_transaction_id = self.db.payments.find_one({ 'transaction_id' : transaction_id }, {'_id' : False})
        if db_transaction_id:
            self.generate_transaction_id(account_number)
        return transaction_id

    def save(self, data):
        try:
            self.db.payments.insert_one(data)
            return True
        except Exception as error:
            Exception(f"Internal server error: {str(error)}")
    
    def detail(self, transaction_id):
        return self.db.payments.find_one({ 'transaction_id' : transaction_id }, { '_id' : False })

    def update(self, transaction_id, update_value):
        try:
            self.db.interbank_transfers.update_one({ 'transaction_id' : transaction_id }, { '$set' : update_value })
        except Exception as error:
            Exception(f"Internal server error: {str(error)}")

    def inquiry(self, bill_id):
        return self.payment.inquiry(bill_id)

    def notify(self):
        try:
            payment = self.detail(self.transaction_id)

            # invoke eletrical payment service
            self.payment.bill_id = payment['bill_id']
            self.payment.journal_number = self.journal_number
            self.payment.description = payment['description']
            response = self.payment.pay()

        except ServiceException as error:
            self.transaction.from_account_number = self.from_account_number
            self.transaction.amount = self.amount
            self.transaction.journal_number = self.journal_number
            journal_number = self.transaction.reversal()['journal_number']

            self.update(self.transaction_id, {
                "journal_number" : self.journal_number,
                "message" : "Notify failed",
                "status" : "REVERSED",
                "response" : {}
            })
            raise ServiceException(f"Can not invoke eletrical payment service. detail: {error}")

        except Exception as error:
            print(error)
            raise Exception("Internal server error.")

    def pay(self):
        try:
            transaction_datetime = datetime.now().strftime("%d-%m-%Y %H:%I%S")
            
            # invoke transaction to retrieve journal number.
            self.transaction.from_account_number = self.from_account_number
            self.transaction.transaction_type = self.transaction_type
            self.transaction.cif_number = self.cif_number
            self.transaction.amount = self.amount
            self.transaction.description = self.description
            self.transaction_id = self.generate_transaction_id()
            self.journal_number = self.transaction.debit()

            # save transaction
            self.save({
                'transaction_id' : self.transaction_id,
                'bill_id' : self.bill_id,
                'from_account_number' : self.from_account_number,
                "amount" : self.amount,
                "journal_number" : self.journal_number,
                "transaction_type": self.transaction_type,
                "transaction_datetime" : transaction_datetime,
                "description" : self.description,
                "message" : "",
                "status" : "DONE",
                "response" : response
            })

            return self.journal_number

        except Exception as error:
            print(error)
            raise Exception("Internal server error.")