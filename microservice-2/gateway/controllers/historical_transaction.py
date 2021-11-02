from dotenv import load_dotenv
from fastapi import HTTPException

import requests, os

class HistoricalTransactionController():

    def __init__(self):
        load_dotenv()
        self.historical_transaction_host = os.environ.get("HISTORICAL_TRANSACTION_HOST")

    def all(self, account_number: str, skip: int = 0, limit: int = 100):
        return requests.get(f"{self.historical_transaction_host}/historical_transaction?account_number={account_number}&skip={skip}&limit={limit}")