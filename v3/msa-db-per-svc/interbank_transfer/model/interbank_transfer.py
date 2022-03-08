from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from uuid import uuid4
from datetime import datetime
from service.transaction import Transaction
from service.interbank import Interbank

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

    def save(self, data):
        try:
            self.db.interbank_transfers.insert_one(data)
            return True
        except Exception as error:
            Exception(f"Internal server error: {str(error)}")

    def inquiry(self, to_account_number, to_bank_code):
        return self.interbank.inquiry(to_account_number, to_bank_code)

    def transfer(self):

        try:
            transaction_datetime = datetime.now().strftime("%d-%m-%Y %H:%I%S")
            
            # invoke transaction to retrieve journal number.
            self.transaction.from_account_number = self.from_account_number
            self.transaction.transaction_type = "INTERBANK"
            self.transaction.cif_number = self.cif_number
            self.transaction.amount = self.amount
            self.transaction.description = self.description
            self.journal_number = self.transaction.debit()['journal_number']
            
            # request notify to interbank. 
            self.interbank.from_account_number = self.from_account_number
            self.interbank.from_bank_code =  self.from_bank_code
            self.interbank.acccount_number = self.to_account_number 
            self.interbank.bank_code = self.to_bank_code
            self.interbank.amount = self.amount
            self.interbank.journal_number = self.journal_number
            self.interbank.transaction_datetime = transaction_datetime
            self.interbank.description = self.description       
            response = self.interbank.notify()

            # save transaction
            self.save({
                'from_account_number' : self.from_account_number,
                "from_bank_code" : self.from_bank_code,
                "to_account_number" : self.to_account_number,
                "to_bank_code" : self.to_bank_code,
                "amount" : self.amount,
                "journal_number" : self.journal_number,
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
            journal_number = self.transaction.reversal()['journal_number']

            self.save({
                'from_account_number' : self.from_account_number,
                "from_bank_code" : self.from_bank_code,
                "to_account_number" : self.to_account_number,
                "to_bank_code" : self.to_bank_code,
                "amount" : self.amount,
                "journal_number" : self.journal_number,
                "transaction_datetime" : transaction_datetime,
                "description" : self.description,
                "status" : "REVERSED",
                "response" : {}
            })
            raise ServiceException(f"Can not invoke interbank service. detail: {error}")

        except Exception as error:
            print(error)
            raise Exception("Internal server error.")