from databases.historical_transaction import HistoricalTransactionDB
from sqlalchemy import and_
from datetime import timedelta, datetime
import random, string, requests, os

class HistoricalTransactionModel():
    
    def __init__(self, db):
        self.db = db

    def generate_journal_number(self, size=6):
        response = requests.get(os.environ.get("HISTORICAL_TRANSACTION_HOST"))
        if response.status_code == 200:
            response_json = response.json()
            return response_json['journal_number']