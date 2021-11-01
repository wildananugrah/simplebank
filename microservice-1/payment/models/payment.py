from databases.h2h_lookup import H2HLookupDB
from models.historical_transaction import HistoricalTransactionModel

import os, requests

class Payment():
    def __init__(self, url, db=None):
        self.db = db
        self.url = url
        self.request_message = None

    def debit(self, account_number, amount):
        account_url = os.environ.get("ACCOUNT_HOST")
        response = requests.post(f"{account_url}/account/update_balance", json={
            "account" : account_number,
            "action" : "DEBIT",
            "amount": amount
        })
        
        db_account = response.json()
        journal_number = HistoricalTransactionModel().generate_journal_number()
        
        historical_transaction_url = os.environ.get("HISTORICAL_TRANSACTION_HOST")
        response = requests.post(f"{historical_transaction_url}/historical_transaction", json={
            "account_number": account_number, 
            "current_account_balance": db_account['balance'], 
            "amount": amount, 
            "action": "DEBIT",
            "transaction_type" : "PAYMENT"
        })

        if response.status_code != 200:
            return False

        return True

    def insert_to_h2hlookup(self, bill_id, bill_type, transaction_type, account_number, cif_number, action, status):
        db_h2h_lookup = H2HLookupDB(
            bill_id=bill_id,
            bill_type=bill_type,
            transaction_type=transaction_type, 
            account_number=account_number, 
            cif_number=cif_number,
            action=action, 
            status=status
        )

        self.db.add(db_h2h_lookup)
        self.db.commit()

        return True