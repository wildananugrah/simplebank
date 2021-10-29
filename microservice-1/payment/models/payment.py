from databases.h2h_lookup import H2HLookupDB
from models.account import AccountModel
from models.historical_transaction import HistoricalTransactionModel
from databases.historical_transaction import HistoricalTransactionDB

import os, requests

class Payment():
    def __init__(self, url, db=None):
        self.db = db
        self.url = url
        self.request_message = None

    def debit(self, account_number, amount):
        db_account = AccountModel(self.db).detail(account_number)
        db_account.balance = db_account.balance - amount
        journal_number = HistoricalTransactionModel(self.db).generate_journal_number()

        response = requests.post(os.environ.get("HISTORICAL_TRANSACTION_HOST"), json={
            "account_number": account_number, 
            "current_account_balance": db_account.balance, 
            "amount": amount, 
            "action": "DEBIT",
            "transaction_type" : "TRANSFER"
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