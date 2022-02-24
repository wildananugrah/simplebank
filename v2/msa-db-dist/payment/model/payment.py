from db import dbinstance
from datetime import datetime
import requests, os, pika, json

class PaymentModel():
    
    def __init__(self):
        db_read, db_write = dbinstance.get_db()
        self.db_read = db_read.simplebank_db
        self.db_write = db_write.simplebank_db

    def save_payment(self, account_number, bill_id, biller_name, amount, transaction_id, cif_number, outgoing_request, status):
        data = {
            'account_number' : account_number,
            'bill_id' : bill_id,
            'biller_name' : biller_name,
            'amount' : amount,
            'transaction_datetime' : datetime.today().replace(microsecond=0),
            'transaction_id' : transaction_id,
            'cif_number' : cif_number,
            'status' : status,
            'outgoing_request' : outgoing_request,
        }
        self.db_write.payments.insert_one(data)
        return self.detail(transaction_id)

    def detail_account_number(self, account_number):
        return self.db_read.accounts.find_one({ 'account_number' : account_number }, {'_id' : False})

    # def update_payment(self, transaction_id, status, incoming_response = {}):
    #     query = { 'transaction_id' : transaction_id }
    #     newvalues = { 'status' : status, 'incoming_response': incoming_response }

    #     return self.db_write.payments.update_one( query, { '$set' : newvalues } )

    def detail(self, transaction_id):
        return self.db_write.payments.find_one( { 'transaction_id' : transaction_id } , { '_id' : False } )

    def find_transaction_id(self,cif_number, transaction_id):
        return self.db_read.payments.find_one({ "cif_number" : cif_number, 'transaction_id' : transaction_id }, { '_id' : False })

    def list(self, cif_number):
        return self.db_read.payments.find({ 'cif_number' : cif_number }, { '_id' : False }).sort('transaction_datetime', -1)

    def inquiry_billers(self, bill_id):
        return requests.get(f"{os.getenv('SIM_BILLPAYMENT_HOST')}?bill_id={bill_id}")

    def notify_billers(self, message):
        return requests.post(f"{os.getenv('SIM_BILLPAYMENT_HOST')}/", json=message)

    def find_journal_number(self, journal_number, account_number):
        hist_trx = self.db_read.historical_transactions.find({ 'account_number' : account_number, 'journal_number' : journal_number }, {'_id': False})

        for hist in hist_trx:
            if hist['transaction_datetime'].date() == datetime.today().date():
                return True
        
        return None
    
    def update_account_number_balance(self, account_number, balance):
        query = {'account_number' : account_number}
        newvalues = { 'balance' : balance }

        return self.db_write.transfers.update_one(query, { '$set' : newvalues })
    
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

