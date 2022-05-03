from dataclasses import dataclass
from abc import ABC, abstractmethod
from exception.business_logic_exception import BusinessLogicException
from datetime import datetime
from database import session
from table.historical_transaction import TblHistoricalTransaction

@dataclass
class HistoricalTransaction:

    """ represent historical transaction master entity """

    transaction_type: str = None
    account_number: str = None
    amount: int = 0
    journal_number: str = None
    current_balance: int = 0
    description: str = None
    session = session

    def save(self):
        if self.transaction_type not in ['DEBIT', 'CREDIT', 'REVERSAL']:
            raise BusinessLogicException(f"Invalid transaction_type: {self.transaction_type}")
    
        historical_transaction = TblHistoricalTransaction(
                                        transaction_type=self.transaction_type,
                                        account_number=self.account_number,
                                        amount=self.amount,
                                        journal_number=self.journal_number,
                                        current_balance=self.current_balance,
                                        description=self.description)
        self.session.add(historical_transaction)
        self.session.commit()

        return True

    def list(self, account_number, skip, limit):
        historical_transactions = self.session.query(TblHistoricalTransaction).filter(TblHistoricalTransaction.account_number == account_number).offset(skip).limit(limit).order_by(TblHistoricalTransaction.transaction_datetime.desc())
        
        data = []
        for historical_transaction in historical_transactions:
            data.append({
                "transaction_type" : historical_transaction.transaction_type,
                "account_number" : historical_transaction.account_number,
                "amount" : historical_transaction.amount,
                "journal_number" : historical_transaction.journal_number,
                "current_balance" : historical_transaction.current_balance,
                "description" : historical_transaction.description,
                "transaction_datetime" : historical_transaction.transaction_datetime
            })
        
        return data