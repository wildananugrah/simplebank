from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from uuid import uuid4
from datetime import datetime
from service.transaction import Transaction
from service.interbank import Interbank
import string, random

@dataclass
class InterbankTransfer:

    """ represent transaction in other bank system entity """
    
    from_account_number: str = None
    from_bank_code: str = "009"
    to_account_number: str = None
    to_bank_code: str = None
    amount: int = 0
    description: str = None
    cif_number: str = None
    interbank: Interbank = Interbank()
    transaction: Transaction = Transaction()
    db = dbinstance.get_db().simplebank_db
    journal_number: str = None
    transaction_id: str = None

    def generate_transaction_id(self, size=10):
        transaction_id = ''.join(random.choice(string.digits) for _ in range(size))
        db_transaction_id = self.db.interbank_transfers.find_one({ 'transaction_id' : transaction_id }, {'_id' : False})
        if db_transaction_id:
            self.generate_transaction_id(account_number)
        return transaction_id

    def save(self, data):
        try:
            self.db.interbank_transfers.insert_one(data)
            return True
        except Exception as error:
            Exception(f"Internal server error: {str(error)}")

    def list(self, cif_number):
        print(f"cif_number: {cif_number}")
        return list(self.db.interbank_transfers.find({ 'cif_number' : cif_number }, { '_id' : False }).sort('transaction_datetime', -1))

    def detail(self, transaction_id):
        return self.db.interbank_transfers.find_one({ 'transaction_id' : transaction_id }, { '_id' : False })
    
    def update(self, transaction_id, update_value):
        try:
            self.db.interbank_transfers.update_one({ 'transaction_id' : transaction_id }, { '$set' : update_value })
        except Exception as error:
            raise Exception(f"Internal server error: {str(error)}")

    def inquiry(self, to_account_number, to_bank_code):
        return self.interbank.inquiry(to_account_number, to_bank_code)

    def notify(self, transaction_id, update_value):
        
        transaction = self.detail(transaction_id)

        self.update(transaction_id, update_value)

        try:

            # request notify to interbank. 
            self.interbank.from_account_number = transaction['from_account_number']
            self.interbank.from_bank_code =  transaction['from_bank_code']
            self.interbank.acccount_number = transaction['to_account_number'] 
            self.interbank.bank_code = transaction['to_bank_code']
            self.interbank.amount = transaction['amount']
            self.interbank.journal_number = update_value['journal_number']
            self.interbank.transaction_datetime = transaction['transaction_datetime']
            self.interbank.description = transaction['description']  
            response = self.interbank.notify()

            return update_value['journal_number']

        except ServiceException as error:
            self.transaction.from_account_number = transaction['from_account_number']
            self.transaction.amount = transaction['amount']
            self.transaction.journal_number = update_value['journal_number']
            journal_number = self.transaction.reversal()

            self.update(transaction_id, {
                "journal_number" : update_value['journal_number'],
                "status" : "REVERSED",
                "message" : "Notify Failed",
                "response" : {}
            })

            raise ServiceException(f"Can not invoke interbank service. detail: {error}")
        except Exception as error:
            print(error)
            raise Exception("Internal server error.")

    def transfer(self):

        transaction_datetime = datetime.now().strftime("%d-%m-%Y %H:%I%S")
        
        # invoke transaction to retrieve journal number.
        self.transaction.transaction_id = self.generate_transaction_id()
        self.transaction.from_account_number = self.from_account_number
        self.transaction.transaction_type = "INTERBANK"
        self.transaction.cif_number = self.cif_number
        self.transaction.amount = self.amount
        self.transaction.description = self.description
        self.journal_number = self.transaction.debit()

        self.save({
            'transaction_id': self.transaction.transaction_id,
            'from_account_number' : self.from_account_number,
            "from_bank_code" : self.from_bank_code,
            "to_account_number" : self.to_account_number,
            "to_bank_code" : self.to_bank_code,
            "amount" : self.amount,
            "journal_number" : "NONE",
            "cif_number" : self.cif_number,
            "transaction_datetime" : transaction_datetime,
            "description" : self.description,
            "status" : "PROGRESS",
            "message": "Transaction in progress",
            "response" : {}
        })

        return self.transaction.transaction_id