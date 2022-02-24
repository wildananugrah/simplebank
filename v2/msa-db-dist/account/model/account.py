from db import dbinstance
from datetime import datetime

import pika, os, json

class AccountModel():
    def __init__(self):
        db_read, db_write = dbinstance.get_db()
        self.db_read = db_read.simplebank_db
        self.db_write = db_write.simplebank_db

    def create(self, account_number, cif_number, currency, balance):
        data = {
            'account_number' : account_number,
            'cif_number' : cif_number,
            'currency' : currency,
            'balance' : int(balance)
        }
        self.db_write.accounts.insert_one(data)
        return self.detail(account_number)

    def delete(self, account_number):
        query = { 'account_number' : account_number }
        self.db_write.accounts.delete_one(query)
        return True

    def detail(self, account_number):
        query = { 'account_number' : account_number }
        return self.db_write.accounts.find_one(query, {'_id': False})

    def list(self, cif_number):
        query = { 'cif_number' : cif_number }
        return self.db_read.accounts.find(query, {'_id': False})

    def historical_transaction(self, account_number):
        query = { 'account_number' : account_number }
        return self.db_read.historical_transactions.find(query, {'_id' : False}).sort("transaction_datetime", -1) # descending

    def update_balance(self, account_number, current_balance):
        query = { 'account_number' : account_number }
        newvalues = { '$set' : { 'balance' : int(current_balance) } }
        return self.db_write.accounts.update_one(query, newvalues)

    def find_journal_number(self, journal_number, account_number):
        hist_trx = self.db_read.historical_transactions.find({ 'account_number' : account_number, 'journal_number' : journal_number }, {'_id': False})

        for hist in hist_trx:
            if hist['transaction_datetime'].date() == datetime.today().date():
                return True
        
        return None

    def add_historical_transaction(self, account_number, amount, action, journal_number, transaction_id, transaction_type, description):
        datetime_today = datetime.today().replace(microsecond=0)
        data = {
            'account_number' : account_number,
            'amount' : amount, 
            'action' : action, 
            'journal_number' : journal_number,
            'transaction_id' : transaction_id,
            'transaction_type' : transaction_type,
            'transaction_datetime': datetime_today,
            'description' : description
        }
        self.db_write.historical_transactions.insert_one(data)
        return True