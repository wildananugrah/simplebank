from db import dbinstance
from datetime import datetime
from account.controller.account import *
import requests

class PaymentModel():
    
    def __init__(self):
        self.db = dbinstance.get_db().simplebank_db
        self.collection = self.db.payments
        self.account_controller = AccountController()

    def save_payment(self, account_number, bill_id, biller_name, amount, transaction_id, cif_number, outgoing_request):
        data = {
            'account_number' : account_number,
            'bill_id' : bill_id,
            'biller_name' : biller_name,
            'amount' : amount,
            'transaction_datetime' : datetime.today().replace(microsecond=0),
            'transaction_id' : transaction_id,
            'cif_number' : cif_number,
            'status' : 'PENDING',
            'outgoing_request' : outgoing_request,
            'incoming_response' : {}
        }
        self.collection.insert_one(data)
        return self.detail_payment(transaction_id)

    def update_payment(self, transaction_id, status, incoming_response = {}):
        query = { 'transaction_id' : transaction_id }
        newvalues = { 'status' : status, 'incoming_response': incoming_response }

        return self.collection.update_one( query, { '$set' : newvalues } )

    def detail_payment(self, transaction_id):
        return self.collection.find_one( { 'transaction_id' : transaction_id } , { '_id' : False } )

    def find_account_number(self, account_number):
        return self.account_controller.detail(account_number)

    def debit(self, account_number, amount, description, transaction_id):
        data = {
            'account_number' : account_number,
            'amount' : amount,
            'description' : description,
            'transaction_id' : transaction_id,
        }
        return self.account_controller.debit(data)

    def find_transaction_id(self,cif_number, transaction_id):
        return self.collection.find_one({ "cif_number" : cif_number, 'transaction_id' : transaction_id }, { '_id' : False })

    def list(self, cif_number):
        return self.collection.find({ 'cif_number' : cif_number }, { '_id' : False }).sort('transaction_datetime', -1)

    def inquiry_billers(self, bill_id):
        return requests.get(f"http://localhost:9010?bill_id={bill_id}")

    def notify_billers(self, message):
        return requests.post("http://localhost:9010/", json=message)

