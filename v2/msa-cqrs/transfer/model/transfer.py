from db import dbinstance
from datetime import datetime

import requests, os, json, pika

class TransferModel():
    def __init__(self):
        db_read, db_write = dbinstance.get_db()
        self.read_db = db_read.simplebank_db
        self.read_collection = self.read_db.transfers
        self.read_account_collection = self.read_db.transfer_accounts

        self.write_db = db_write.simplebank_db
        self.write_collection = self.write_db.transfers
        self.write_account_collection = self.write_db.transfer_accounts

    def transfer_account_number(self, from_account_number, to_account_number, transaction_id, amount, description):
        data = {
            'from_account_number' : from_account_number,
            'to_account_number': to_account_number,
            'transaction_id': transaction_id,
            'amount': amount,
            'description' : description
        }
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBIT_MQ_HOST'), port=os.getenv('RABBIT_MQ_PORT')))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_ACCOUNT'), body=json.dumps(data))

        connection.close()
        return True

    def inquiry_interbank_account_number(self, account_number, bank_code):
        return requests.get(f"{os.getenv('SIM_INTERBANK_HOST')}/?account_number={account_number}&bank_code={bank_code}")

    def save_transfer(self, cif_number, from_account_number, to_account_number, bank_code, amount, transaction_id, description):
        data = {
            'from_account_number': from_account_number, 
            'to_account_number': to_account_number, 
            'bank_code' : bank_code,
            'amount': amount,
            'transaction_datetime' : datetime.today().replace(microsecond=0),
            'transaction_id' : transaction_id,
            'cif_number' : cif_number,
            'description': description, 
            'status' : 'PENDING'
        }
        self.write_collection.insert_one(data)
        return data

    def detail(self, transaction_id):
        return self.write_collection.find_one({ 'transaction_id' : transaction_id }, { '_id' : False })
    
    def list(self, cif_number):
        return self.read_collection.find({ 'cif_number' : cif_number }, {'_id' : False}).sort('transaction_datetime', -1)

    def update(self, transaction_id, status):
        return self.write_collection.update_one({ 'transaction_id' : transaction_id }, {'$set' : { 'status' : status }})

    def settlement_account_number(self, from_account_number, to_account_number, bank_code, transaction_id, amount):
        data = { 
            'account_number' : from_account_number,
            'transaction_id' : transaction_id,
            'amount' : amount, 
            'description' : f'TRF {bank_code} {to_account_number}',
            'transaction_type': "INTERBANK_TRANSFER"
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBIT_MQ_HOST'), port=os.getenv('RABBIT_MQ_PORT')))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_ACCOUNT_DEBIT'), body=json.dumps(data))

        connection.close()
        return True

    def reversal_interbank(self, from_account_number, to_account_number, bank_code, transaction_id, amount, journal_number):
        data = { 
            'account_number' : from_account_number,
            'transaction_id' : transaction_id,
            'amount' : amount, 
            'description' : f'REVERSAL ',
            'transaction_type': "REVERSAL_INTERBANK_TRANSFER",
            'journal_number' : journal_number
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBIT_MQ_HOST'), port=os.getenv('RABBIT_MQ_PORT')))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_REVERSAL_INTERBANK'), body=json.dumps(data))

        connection.close()
        return True

    def save_account_number(self, cif_number, account_number, bank_code="009"):
        self.write_account_collection.insert_one({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code })
        return self.detail_account_number(cif_number, account_number, bank_code)

    def delete_account_number(self, cif_number, account_number, bank_code="009"):
        return self.write_account_collection.delete_one({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code })
    
    def list_account_number(self, cif_number):
        return self.read_account_collection.find({ 'cif_number' : cif_number }, {'_id' :  False})

    def list(self, cif_number):
        return self.read_collection.find({ 'cif_number' : cif_number }, {'_id' :  False}).sort('transaction_datetime', -1)

    def detail_account_number(self, cif_number, account_number, bank_code="009"):
        return self.write_account_collection.find_one({ 'cif_number' : cif_number, 'account_number' : account_number, 'bank_code' : bank_code }, {'_id' : False })

    def list_account_number(self, cif_number, bank_code="009"):
        return self.read_account_collection.find({ 'cif_number' : cif_number }, {'_id' : False})

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
        return self.read_collection.find_one({'transaction_id' : transaction_id, 'account_number' : account_number}, {'_id': False})
