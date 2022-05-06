from model.transaction import DebitTransaction, Transaction
from sp_config import *
import pika, json

def on_debit(ch, method, properties, body):
    json_request = json.loads(body)
    model = DebitTransaction()
    
    if 'bank_code' in json_request:
        model.bank_code = json_request['bank_code']
    if 'to_account_number' in json_request:
        model.to_account_number = json_request['to_account_number']

    model.transaction_id = json_request['transaction_id']
    model.transaction_type = json_request['transaction_type']
    model.from_account_number = json_request['from_account_number']
    model.cif_number = json_request['cif_number']
    model.amount = int(json_request['amount'])
    model.description = json_request['description']
    journal_number = model.debit()
    print(f"execute on_debit; message: {json_request}")

def on_reversal(ch, method, properties, body):
    json_request = json.loads(body)
    model = Transaction()
    model.reversal(json_request['account_number'], json_request['amount'], json_request['journal_number'])
    print(f"execute on_reversal; message: {json_request}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
channel = connection.channel()
channel.queue_declare(queue='debit')
channel.basic_consume(queue='debit', on_message_callback=on_debit, auto_ack=True)

channel.queue_declare(queue='reversal')
channel.basic_consume(queue='reversal', on_message_callback=on_reversal, auto_ack=True)