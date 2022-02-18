from db import dbinstance
from account.controller.account import AccountController
from datetime import datetime

import requests

class TransferModel():
    def __init__(self):
        self.db = dbinstance.get_db().simplebank_db
        self.collection = self.db.transfers
        self.account_collection = self.db.transfer_accounts
        self.account_controller = AccountController()

    def own_accounts_inquiry(self, cif_number):
        return self.account_controller.list({ "cif_number" : cif_number })

    def account_inquiry(self, account_number):
        return self.account_controller.detail(account_number)

    def transfer(self, from_account_number, to_account_number, transaction_id, amount, description):
        data = {
            'from_account_number' : from_account_number,
            'to_account_number': to_account_number,
            'transaction_id': transaction_id,
            'amount': amount,
            'description' : description
        }
        return self.account_controller.transfer(data)

    def account_interbank_inquiry(self, account_number, bank_code):
        return requests.get(f"http://localhost:9000/?account_number={account_number}&bank_code={bank_code}")

    def save_transfer(self, cif_number, from_account_number, to_account_number, bank_code, amount, transaction_id):
        data = {
            'from_account_number': from_account_number, 
            'to_account_number': to_account_number, 
            'bank_code' : bank_code,
            'amount': amount,
            'transaction_datetime' : datetime.today().replace(microsecond=0),
            'transaction_id' : transaction_id,
            'cif_number' : cif_number,
            'status' : 'PENDING'
        }
        return self.collection.insert_one(data)

    def transfer_detail(self, transaction_id):
        return self.collection.find_one({ 'transaction_id' : transaction_id }, { '_id' : False })
    
    def transfer_list(self, cif_number):
        return self.collection.find({ 'cif_number' : cif_number }, {'_id' : False}).sort('transaction_datetime', -1)

    def update_transfer(self, transaction_id, status):
        return self.collection.update_one({ 'transaction_id' : transaction_id }, {'$set' : { 'status' : status }})

    def settlement_account(self, from_account_number, to_account_number, bank_code, transaction_id, amount):
        data = { 
            'account_number' : from_account_number,
            'transaction_id' : transaction_id,
            'amount' : amount, 
            'description' : f'TRF {bank_code} {to_account_number}',
            'transaction_type': "INTERBANK_TRANSFER"
        }

        return self.account_controller.debit(data)

    def save_account(self, cif_number, account_number, bank_code="009"):
        self.account_collection.insert_one({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code })
        return self.detail_account(cif_number, account_number, bank_code)

    def delete_account(self, cif_number, account_number, bank_code="009"):
        return self.account_collection.delete_one({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code })
    
    def list_account(self, cif_number):
        return self.account_collection.find({ 'cif_number' : cif_number }, {'_id' :  False})

    def list(self, cif_number):
        return self.collection.find({ 'cif_number' : cif_number }, {'_id' :  False}).sort('transaction_datetime', -1)

    def detail_account(self, cif_number, account_number, bank_code="009"):
        return self.account_collection.find_one({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code }, {'_id' : False })

    def account_list(self, cif_number, bank_code="009"):
        return self.account_collection.find({ 'cif_number' : cif_number }, {'_id' : False})

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

        # TODO: hard code URL
        return requests.post("http://localhost:9000/settlement", json=simulator_request)

    def find_transaction_id(self, transaction_id, account_number):
        return self.collection.find_one({'transaction_id' : transaction_id, 'account_number' : account_number}, {'_id': False})
