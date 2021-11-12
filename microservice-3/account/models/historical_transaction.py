from random import randint
import string, requests, os

class HistoricalTransactionModel():

    def generate_journal_number(self, size=6):
        return str(randint(100000, 999999))