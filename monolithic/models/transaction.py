from databases.historical_transaction import HistoricalTransactionDB

class TransactionModel():
    def __init__(self, db=None):
        self.db = db

    def transfer(self, from_account_number, db_from_account_number, to_account_number, db_to_account_number, journal_number, amount, timestamp):
        
        current_from_account_balance = db_from_account_number.balance - amount
        current_to_account_balance = db_to_account_number.balance + amount

        # insert historical transaction from ccount number
        from_current_account_historical = HistoricalTransactionDB(
            account_number=from_account_number,
            transaction_type="TRANSFER",
            action="DEBIT",
            amount=amount,
            balance=current_from_account_balance,
            journal_number=journal_number
        )
        self.db.add(from_current_account_historical)

        # insert historical transaction to account number
        to_current_account_historical = HistoricalTransactionDB(
            account_number=to_account_number,
            transaction_type="TRANSFER",
            action="CREDIT",
            amount=amount,
            balance=current_to_account_balance,
            journal_number=journal_number
        )
        self.db.add(to_current_account_historical)
        
        # update balance
        db_from_account_number.balance = current_from_account_balance
        db_to_account_number.balnace = current_to_account_balance

        self.db.commit()

        return True

    def deposit(self, account_number, db_account_number, journal_number, amount, timestamp):
        current_account_balance = db_account_number.balance + amount

        # insert historical transaction to account number
        current_account_historical = HistoricalTransactionDB(
            account_number=account_number,
            transaction_type="DEPOSIT",
            action="CREDIT",
            amount=amount,
            balance=current_account_balance,
            journal_number=journal_number
        )
        self.db.add(current_account_historical)
        
        # update balance
        db_account_number.balance = current_account_balance

        self.db.commit()

        return True
