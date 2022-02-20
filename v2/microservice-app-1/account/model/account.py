from db import dbinstance
from datetime import datetime

import pika, os, json

class AccountModel():
    def __init__(self):
        self.db = dbinstance.get_db().simplebank_db
        self.collection = self.db.accounts
        self.hist_trx_collection = self.db.historical_transactions

    def create(self, account_number, cif_number, currency, balance):
        data = {
            'account_number' : account_number,
            'cif_number' : cif_number,
            'currency' : currency,
            'balance' : int(balance)
        }
        self.collection.insert_one(data)
        return self.detail(account_number)

    def delete(self, account_number):
        query = { 'account_number' : account_number }
        self.collection.delete_one(query)
        return True

    def detail(self, account_number):
        query = { 'account_number' : account_number }
        return self.collection.find_one(query, {'_id': False})

    def list(self, cif_number):
        query = { 'cif_number' : cif_number }
        return self.collection.find(query, {'_id': False})

    def update_balance(self, account_number, current_balance):
        query = { 'account_number' : account_number }
        newvalues = { '$set' : { 'balance' : int(current_balance) } }
        return self.collection.update_one(query, newvalues)

    def historical_transaction(self, account_number):
        query = { 'account_number' : account_number }
        return self.hist_trx_collection.find(query, {'_id' : False}).sort("transaction_datetime", -1) # descending

    def find_journal_number(self, journal_number, account_number):
        hist_trx = self.hist_trx_collection.find({ 'account_number' : account_number, 'journal_number' : journal_number }, {'_id': False})

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
        self.hist_trx_collection.insert_one(data)
        return True

    def mq_to_transfer(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBIT_MQ_HOST')))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_TRANSFER'), body=json.dumps(message))

        connection.close()

    def mq_to_debit_user(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBIT_MQ_HOST')))
        channel = connection.channel()

        if message['data']['transaction_type'] == "PAYMENT":
            channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_PAYMENT'), body=json.dumps(message))
        elif message['data']['transaction_type'] == "INTERBANK_TRANSFER":
            channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_INTERBANK'), body=json.dumps(message))

        connection.close()
    
    def mq_to_reversal_user(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(os.getenv('RABBIT_MQ_HOST')))
        channel = connection.channel()

        print("message:", message)

        if message['data']['transaction_type'] == "REVERSAL_PAYMENT":
            channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_REVERSAL_PAYMENT'), body=json.dumps(message))
        elif message['data']['transaction_type'] == "REVERSAL_INTERBANK_TRANSFER":
            channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_REVERSAL_INTERBANK_TRANSFER'), body=json.dumps(message))

        connection.close()