from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from datetime import datetime

class HistoricalTransactionAbstract(ABC):

    """ represent base historical transaction """

    @abstractmethod
    def save(self):
        raise NotImplementedError

    @abstractmethod
    def list(self, account_number):
        raise NotImplementedError

@dataclass
class HistoricalTransaction(HistoricalTransactionAbstract):

    """ represent historical transaction master entity """

    transaction_type: str = None
    account_number: str = None
    amount: str = None
    journal_number: str = None
    current_balance: int = 0
    description: str = None

    db = dbinstance.get_db().simplebank_db

    def save(self):
        if self.transaction_type not in ['DEBIT', 'CREDIT', 'REVERSAL']:
            raise BusinessLogicException(f"Invalid transaction_type: {self.transaction_type}")
    
        data = {
                'transaction_type': self.transaction_type,
                'account_number': self.account_number, 
                'amount': self.amount,
                'journal_number' : self.journal_number,
                'current_balance': self.current_balance,
                'description': self.description,
                'transaction_datetime' : datetime.today().replace(microsecond=0)
            }

        self.db.historical_transactions.insert_one(data)

        return True

    def list(self, account_number):
        print(account_number)
        return list(self.db.historical_transactions.find({ 'account_number' : account_number }, { '_id' : False }).sort("transaction_datetime", -1)) # descending