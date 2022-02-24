from db import dbinstance
from datetime import datetime

import requests, os, json, pika

class TransferModel():
    def __init__(self):
        db_read, db_write = dbinstance.get_db()
        self.db_read = db_read.simplebank_db
        self.db_write = db_write.simplebank_db

    # transfer account
    def transfer_account_number(self, from_account_number, to_account_number, transaction_id, amount, description): 
        pass

    def inquiry_interbank_account_number(self, account_number, bank_code):
        print(f"{os.getenv('SIM_INTERBANK_HOST')}/?account_number={account_number}&bank_code={bank_code}")
        return requests.get(f"{os.getenv('SIM_INTERBANK_HOST')}/?account_number={account_number}&bank_code={bank_code}")

    def save_transfer(self, cif_number, from_account_number, to_account_number, bank_code, amount, transaction_id, description, status = "PENDING"):
        data = {
            'from_account_number': from_account_number, 
            'to_account_number': to_account_number, 
            'bank_code' : bank_code,
            'amount': amount,
            'transaction_datetime' : datetime.today().replace(microsecond=0),
            'transaction_id' : transaction_id,
            'cif_number' : cif_number,
            'description': description, 
            'status' : status
        }
        return self.db_write.transfers.insert_one(data)

    def detail(self, transaction_id):
        return self.db_write.transfers.find_one({ 'transaction_id' : transaction_id }, { '_id' : False })

    def detail_account_number(self, account_number):
        return self.db_read.accounts.find_one({ 'account_number' : account_number }, {'_id' : False})

    def update_account_number_balance(self, account_number, balance):
        query = {'account_number' : account_number}
        newvalues = { 'balance' : balance }

        return self.db_write.transfers.update_one(query, { '$set' : newvalues })
    
    def list(self, cif_number):
        return self.db_write.transfers.find({ 'cif_number' : cif_number }, {'_id' : False}).sort('transaction_datetime', -1)

    def update(self, transaction_id, status):
        return self.db_write.transfers.update_one({ 'transaction_id' : transaction_id }, {'$set' : { 'status' : status }})

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

    def find_journal_number(self, journal_number, account_number):
        hist_trx = self.db_read.historical_transactions.find({ 'account_number' : account_number, 'journal_number' : journal_number }, {'_id': False})

        for hist in hist_trx:
            if hist['transaction_datetime'].date() == datetime.today().date():
                return True
        
        return None

    # TODO: reversal
    def reversal_interbank(self, from_account_number, to_account_number, bank_code, transaction_id, amount, journal_number):
        pass

    def save_account_number(self, cif_number, account_number, bank_code="009"):
        return self.db_write.transfer_accounts.insert_one({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code }).inserted_id

    def delete_account_number(self, cif_number, account_number, bank_code="009"):
        return self.db_write.transfer_accounts.delete_one({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code })
    
    def list_account_number(self, cif_number):
        return self.db_write.transfer_accounts.find({ 'cif_number' : cif_number }, {'_id' :  False})

    def list(self, cif_number):
        return self.db_write.transfers.find({ 'cif_number' : cif_number }, {'_id' :  False}).sort('transaction_datetime', -1)

    def detail_interbank_account_number(self, cif_number, account_number, bank_code="009"):
        return self.db_write.transfer_accounts.find_one({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code }, {'_id' : False })

    def list_account_number(self, cif_number, bank_code="009"):
        return self.db_write.transfer_accounts.find({ 'cif_number' : cif_number }, {'_id' : False})

    def notify_interbank(self, source_account_number, source_bank_code, to_account_number, bank_code, amount, description):
        simulator_request = {
            "account_number" : to_account_number,
            "bank_code" : bank_code,
            "amount" : amount,
            "source_account_number" : source_account_number,
            "source_bank_code" : source_bank_code,
            "transaction_datetime": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "description": description
        }

        return requests.post(f"{os.getenv('SIM_INTERBANK_HOST')}/settlement", json=simulator_request)

    def find_transaction_id(self, transaction_id, account_number):
        return self.db_write.transfers.find_one({'transaction_id' : transaction_id, 'account_number' : account_number}, {'_id': False})
