import random, string, requests, os

class HistoricalTransactionModel():

    def generate_journal_number(self, size=6):
        response = requests.get(os.environ.get("HISTORICAL_TRANSACTION_HOST"))
        if response.status_code == 200:
            response_json = response.json()
            return response_json['journal_number']