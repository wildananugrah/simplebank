from dataclasses import dataclass
from exception.business_logic_exception import BusinessLogicException
from sp_config import *
from db import dbinstance
import requests, os

@dataclass
class HistoricalTransaction:

    transaction_type: str = None
    account_number: str = None
    amount: int = 0
    journal_number: str = str
    current_balance: int = 0
    description: str = None
    
    db_read, db_write = dbinstance.get_db()

    def save(self):
        
        try:
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

            result = self.db_write.simplebank_db.historical_transactions.insert_one(data)

            return True
        except Exception as error:
            Exception(f"Database failure. {str(error)}")
