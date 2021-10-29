from databases.historical_transaction import HistoricalTransactionDB
import requests, os

class TransactionModel():
    def __init__(self, db=None):
        self.db = db

    def transfer(self, from_account_number, to_account_number, journal_number, amount, timestamp):
        
        response = requests.post(os.environ.get("ACCOUNT_HOST"), json={
            "account" : from_account_number,
            "action" : "DEBIT",
            "amount": amount
        })

        response = requests.post(os.environ.get("ACCOUNT_HOST"), json={
            "account" : to_account_number,
            "action" : "CREDIT",
            "amount": amount
        })

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
        return True

    def deposit(self, account_number, journal_number, amount, timestamp):

        response = requests.post(os.environ.get("ACCOUNT_HOST"), json={
            "account" : account_number,
            "action" : "CREDIT",
            "amount": amount
        })

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

        return True
