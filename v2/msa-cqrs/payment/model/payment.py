from db import dbinstance
from datetime import datetime
import requests, os, pika, json

class PaymentModel():
    
    def __init__(self):
        db_read, db_write = dbinstance.get_db()
        self.read_db = db_read.simplebank_db
        self.read_collection = self.read_db.payments

        self.write_db = db_write.simplebank_db
        self.write_collection = self.write_db.payments

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
        self.write_collection.insert_one(data)
        return self.detail(transaction_id)

    def update_payment(self, transaction_id, status, incoming_response = {}):
        query = { 'transaction_id' : transaction_id }
        newvalues = { 'status' : status, 'incoming_response': incoming_response }

        return self.write_collection.update_one( query, { '$set' : newvalues } )

    def detail(self, transaction_id):
        return self.write_collection.find_one( { 'transaction_id' : transaction_id } , { '_id' : False } )

    def debit(self, account_number, amount, description, transaction_id):
        data = {
            'account_number' : account_number,
            'amount' : amount,
            'description' : description,
            'transaction_id' : transaction_id,
            'transaction_type': "PAYMENT",
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBIT_MQ_HOST'), port=os.getenv('RABBIT_MQ_PORT')))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_ACCOUNT_DEBIT'), body=json.dumps(data))

        connection.close()
    
    def reversal_payment(self, account_number, amount, description, transaction_id, journal_number):
        data = {
            'account_number' : account_number,
            'amount' : amount,
            'description' : description,
            'transaction_id' : transaction_id,
            'transaction_type': "REVERSAL_PAYMENT",
            'journal_number' : journal_number
        }

        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBIT_MQ_HOST'), port=os.getenv('RABBIT_MQ_PORT')))
        channel = connection.channel()

        channel.basic_publish(exchange='', routing_key=os.getenv('ROUTING_KEY_TO_REVERSAL_PAYMENT'), body=json.dumps(data))

        connection.close()

        return True

    def find_transaction_id(self,cif_number, transaction_id):
        return self.read_collection.find_one({ "cif_number" : cif_number, 'transaction_id' : transaction_id }, { '_id' : False })

    def list(self, cif_number):
        return self.read_collection.find({ 'cif_number' : cif_number }, { '_id' : False }).sort('transaction_datetime', -1)

    def inquiry_billers(self, bill_id):
        return requests.get(f"{os.getenv('SIM_BILLPAYMENT_HOST')}?bill_id={bill_id}")

    def notify_billers(self, message):
        print(message)
        return requests.post(f"{os.getenv('SIM_BILLPAYMENT_HOST')}/", json=message)

