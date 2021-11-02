import random, string, requests, os

class HistoricalTransactionModel():

    def generate_journal_number(self, size=6):
        historical_transaction_url = os.environ.get("HISTORICAL_TRANSACTION_HOST")
        response = requests.get(f"{historical_transaction_url}/generate_journal_number")
        if response.status_code == 200:
            response_json = response.json()
            return response_json['journal_number']