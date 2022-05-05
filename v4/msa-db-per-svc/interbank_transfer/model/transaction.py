from dataclasses import dataclass
from abc import ABC, abstractmethod
from exception.business_logic_exception import BusinessLogicException
from uuid import uuid4
from datetime import datetime
from service.account import Account
from service.historical_transaction import HistoricalTransaction
from service.interbank import Interbank
from service.transaction import Transaction as ServiceTransaction

import random, string

@dataclass
class Transaction:

    """ represent transaction master entity """

    account: Account = Account()
    historical_transaction: HistoricalTransaction = HistoricalTransaction()
    
    def store_to_historical_transaction(self, transaction_type, account_number, amount, journal_number, current_balance, description = ""):
        self.historical_transaction.transaction_type = transaction_type
        self.historical_transaction.account_number = account_number
        self.historical_transaction.amount = amount
        self.historical_transaction.journal_number = journal_number
        self.historical_transaction.current_balance = current_balance
        self.historical_transaction.description = description
        self.historical_transaction.save()
        return True

@dataclass
class TransferInterbank(Transaction):

    """ represent transaction in other bank system entity """
    
    from_account_number: str = None
    to_account_number: str = None
    to_bank_code: str = None
    amount: int = 0
    description: str = None
    cif_number: str = None
    transaction: ServiceTransaction = ServiceTransaction()

    def inquiry(self, to_account_number, to_bank_code):
        return Interbank().inquiry(to_account_number, to_bank_code)

    def transfer(self):
        db_from_account_number = self.account.detail(self.from_account_number)

        self.transaction.from_account_number = self.from_account_number
        self.transaction.transaction_type = "INTERBANK"
        self.transaction.cif_number = self.cif_number
        self.transaction.amount = self.amount
        self.transaction.description = self.description
        journal_number = self.transaction.debit()['journal_number']

        # request notify to interbank 
        interbank = Interbank(acccount_number=self.from_account_number, 
                        amount=self.amount, 
                        bank_code=self.to_bank_code, 
                        description=self.description, 
                        journal_number=journal_number,
                        transaction_datetime=datetime.now().strftime("%d-%m-%Y %H:%I%S"))
        
        response = interbank.notify()

        return journal_number