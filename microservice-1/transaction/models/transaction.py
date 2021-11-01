from databases.historical_transaction import HistoricalTransactionDB
import requests, os

class TransactionModel():
    def __init__(self, db=None):
        self.db = db

    def transfer(self, from_account_number, to_account_number, journal_number, amount, timestamp):
        
        account_url = os.environ.get("ACCOUNT_HOST")
        response_from_account = requests.post(f"{account_url}/account/update_balance", json={
            "account" : from_account_number,
            "action" : "DEBIT",
            "amount": amount
        })

        response_to_account = requests.post(f"{account_url}/account/update_balance", json={
            "account" : to_account_number,
            "action" : "CREDIT",
            "amount": amount
        })

        historical_transaction_url = os.environ.get("HISTORICAL_TRANSACTION_HOST")
        response = requests.post(f"{historical_transaction_url}/historical_transaction", json={
            "account_number": from_account_number, 
            "current_account_balance": response_from_account.json()['balance'], 
            "amount": amount, 
            "action": "DEBIT",
            "transaction_type" : "TRANSFER"
        })

        response = requests.post(f"{historical_transaction_url}/historical_transaction", json={
            "account_number": to_account_number, 
            "current_account_balance": response_to_account.json()['balance'], 
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "TRANSFER"
        })
        return True

    def deposit(self, account_number, journal_number, amount, timestamp):

        account_url = os.environ.get("ACCOUNT_HOST")
        response = requests.post(f"{account_url}/account/update_balance", json={
            "account" : account_number,
            "action" : "CREDIT",
            "amount": amount
        })

        response = requests.get(f"{account_url}/account?account={account_number}")
        response_json = response.json()

        request_json = {
            "account_number": account_number, 
            "current_account_balance": response_json['balance'], 
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "DEPOSIT"
        }

        historical_transaction_url = os.environ.get("HISTORICAL_TRANSACTION_HOST")
        response = requests.post(f"{historical_transaction_url}/historical_transaction", json=request_json)

        if response.status_code != 200:
            return False

        return True
