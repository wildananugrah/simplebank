from databases.historical_transaction import HistoricalTransactionDB
from sqlalchemy import and_
from datetime import timedelta, datetime
import random, string

class HistoricalTransactionModel():
    
    def __init__(self, db):
        self.db = db

    def generate_journal_number(self, size=6):
        journal_number = ''.join(random.choice(string.digits) for _ in range(size))
        db_journal_number = self.select_by_journal_number(journal_number)
        if db_journal_number:
            self.generate_journal_number()
        return journal_number

    def select_by_journal_number(self, journal_number):
        return self.db.query(HistoricalTransactionDB).filter(and_((HistoricalTransactionDB.timestamp + timedelta(days=1)) > datetime.now(), HistoricalTransactionDB.journal_number == journal_number)).first()

    def historical_transaction(self, account_number, skip: int = 0, limit: int = 100):
        return self.db.query(HistoricalTransactionDB).filter(HistoricalTransactionDB.account_number == account_number).order_by(HistoricalTransactionDB.timestamp.desc()).offset(skip).limit(limit).all()
    
    def add(self, account_number, current_account_balance, amount, action, transaction_type):
        
        # insert historical transaction to account number
        current_account_historical = HistoricalTransactionDB(
            account_number=account_number,
            transaction_type=transaction_type,
            action=action,
            amount=amount,
            balance=current_account_balance,
            timestamp=datetime.utcnow(),
            journal_number=self.generate_journal_number()
        )

        self.db.add(current_account_historical)
        self.db.commit()

        return current_account_historical