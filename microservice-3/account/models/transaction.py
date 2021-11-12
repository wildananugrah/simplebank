import requests, os

class TransactionModel():

    def __init__(self, db):
        self.db = db

    def transfer(self, from_account_number, db_from_account_number, to_account_number, db_to_account_number, journal_number, amount, timestamp):
        
        current_from_account_balance = db_from_account_number.balance - amount
        current_to_account_balance = db_to_account_number.balance + amount
        self.db.commit()
        
        historical_transaction_url = os.environ.get("HISTORICAL_TRANSACTION_HOST")
        response = requests.post(f"{historical_transaction_url}/historical_transaction", json={
            "account_number": from_account_number, 
            "current_account_balance": current_from_account_balance,
            "amount": amount, 
            "action": "DEBIT",
            "transaction_type" : "TRANSFER"
        })

        response = requests.post(f"{historical_transaction_url}/historical_transaction", json={
            "account_number": to_account_number, 
            "current_account_balance": current_to_account_balance, 
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "TRANSFER"
        })
        return True

    def deposit(self, account_number, db_account_number, journal_number, amount, timestamp):

        current_account_balance = db_account_number.balance + amount
        self.db.commit()

        request_json = {
            "account_number": account_number, 
            "current_account_balance": current_account_balance, 
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "DEPOSIT"
        }

        historical_transaction_url = os.environ.get("HISTORICAL_TRANSACTION_HOST")
        response = requests.post(f"{historical_transaction_url}/historical_transaction", json=request_json)

        if response.status_code != 200:
            return False

        return True
