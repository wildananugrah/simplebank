from databases.historical_transaction import HistoricalTransactionDB
import requests, os

class TransactionModel():
    def __init__(self, db=None):
        self.db = db

    def transfer(self, from_account_number, db_from_account_number, to_account_number, db_to_account_number, journal_number, amount, timestamp):
        
        current_from_account_balance = db_from_account_number.balance - amount
        current_to_account_balance = db_to_account_number.balance + amount

        response = requests.post(os.environ.get("HISTORICAL_TRANSACTION_HOST"), json={
            "account_number": from_account_number, 
            "current_account_balance": current_from_account_balance, 
            "amount": amount, 
            "action": "DEBIT",
            "transaction_type" : "TRANSFER"
        })

        response = requests.post(os.environ.get("HISTORICAL_TRANSACTION_HOST"), json={
            "account_number": to_account_number, 
            "current_account_balance": current_to_account_balance, 
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "TRANSFER"
        })
        
        # update balance
        db_from_account_number.balance = current_from_account_balance
        db_to_account_number.balnace = current_to_account_balance

        self.db.commit()

        return True

    def deposit(self, account_number, db_account_number, journal_number, amount, timestamp):
        current_account_balance = db_account_number.balance + amount

        request_json = {
            "account_number": account_number, 
            "current_account_balance": current_account_balance, 
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "DEPOSIT"
        }

        response = requests.post(os.environ.get("HISTORICAL_TRANSACTION_HOST"), json=request_json)

        if response.status_code != 200:
            return False
        
        # update balance
        db_account_number.balance = current_account_balance

        self.db.commit()

        return True
