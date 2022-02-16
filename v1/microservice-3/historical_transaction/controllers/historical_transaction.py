from models.historical_transaction import HistoricalTransactionModel
from schemas.historical_transaction import AddHistoricalTransactionSchema
from datetime import datetime

import random, string

class HistoricalTransactionController():
    def __init__(self, db):
        self.model = HistoricalTransactionModel(db)
        self.view = None
        self.db = db

    def historical_transaction(self, account_number: str, skip: int, limit: int):
        return self.model.historical_transaction(account_number, skip, limit)

    def generate_journal_number(self):
        return { "journal_number" : self.model.generate_journal_number() }

    def add(self, request: AddHistoricalTransactionSchema):
        return self.model.add(request.account_number, request.current_account_balance, request.amount, request.action, request.transaction_type)