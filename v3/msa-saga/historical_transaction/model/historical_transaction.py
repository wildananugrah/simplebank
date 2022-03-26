from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from datetime import datetime

@dataclass
class HistoricalTransaction:

    """ represent historical transaction master entity """

    transaction_type: str = None
    account_number: str = None
    amount: int = 0
    journal_number: str = None
    current_balance: int = 0
    description: str = None

    db = dbinstance.get_db().simplebank_db

    def find_journal_number(self, journal_number):
        return self.db.historical_transaction.find_one({ 'journal_number' : journal_number })

    def save(self):
        try:
            if self.transaction_type not in ['DEBIT', 'CREDIT', 'REVERSAL']:
                raise BusinessLogicException(f"Invalid transaction_type: {self.transaction_type}")

            if self.find_journal_number(self.journal_number):
                raise BusinessLogicException(f"Duplicate journal_number: {self.journal_number}")

            data = {
                    'transaction_type': self.transaction_type,
                    'account_number': self.account_number, 
                    'amount': self.amount,
                    'journal_number' : self.journal_number,
                    'current_balance': self.current_balance,
                    'description': self.description,
                    'transaction_datetime' : datetime.today().replace(microsecond=0)
                }

            result = self.db.historical_transactions.insert_one(data)

            return True
        except Exception as error:
            print(error)
            Exception(f"Database failure. {str(error)}")

    def list(self, account_number, skip, limit):
        return list(self.db.historical_transactions.find({ 'account_number' : account_number }, { '_id' : False }).skip(int(skip)).limit(int(limit)).sort("transaction_datetime", -1)) # descending