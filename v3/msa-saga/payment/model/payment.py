from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from uuid import uuid4
from datetime import datetime
from service.transaction import Transaction
from service.billpayment import EletricalBillPayment as EBPService
import string, random

class Payment:
    
    db = dbinstance.get_db().simplebank_db

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

    def list(self, cif_number):
        return list(self.db.payments.find({ 'cif_number' : cif_number }, { '_id' : False }).sort('transaction_datetime', -1))

    def update(self, transaction_id, update_value):
        try:
            self.db.payments.update_one({ 'transaction_id' : transaction_id }, { '$set' : update_value })
        except Exception as error:
            raise Exception(f"Internal server error: {str(error)}")

@dataclass
class EletricalBillPayment(Payment):

    """ represent eletrical bill payment entity """

    bill_id: str = None
    amount: int = 0
    description: str = None
    from_account_number: str = None
    cif_number: str = None
    payment: EBPService = EBPService()
    transaction: Transaction = Transaction()
    transaction_type: str = "ELECTRICAL_BILLPAYMENT"
    journal_number: str = None

    def inquiry(self, bill_id):
        return self.payment.inquiry(bill_id)

    def notify(self, transaction_id, update_value):
        try:
            payment = self.detail(transaction_id)

            self.update(transaction_id, update_value)

            # invoke eletrical payment service
            self.payment.bill_id = payment['bill_id']
            self.payment.journal_number = update_value['journal_number']
            self.payment.description = payment['description']
            response = self.payment.pay()

        except ServiceException as error:
            self.transaction.from_account_number = payment['from_account_number']
            self.transaction.amount = payment['amount']
            self.transaction.journal_number = update_value['journal_number']
            self.journal_number = self.transaction.reversal()

            print(f"transaction_id: {transaction_id}")

            self.update(transaction_id, {
                "journal_number" : update_value['journal_number'],
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
            self.transaction.transaction_id = self.generate_transaction_id()
            self.journal_number = self.transaction.debit()

            # save transaction
            self.save({
                'transaction_id' : self.transaction.transaction_id,
                'bill_id' : self.bill_id,
                'cif_number' :self.cif_number, 
                'from_account_number' : self.from_account_number,
                "amount" : self.amount,
                "journal_number" : self.journal_number,
                "transaction_type": self.transaction_type,
                "transaction_datetime" : transaction_datetime,
                "description" : self.description,
                "message" : "transaction in progress",
                "status" : "PROGRESS",
                "response" : {}
            })

            return self.transaction.transaction_id

        except Exception as error:
            raise Exception("Internal server error.")