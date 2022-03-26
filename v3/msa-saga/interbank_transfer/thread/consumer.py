from model.interbank_transfer import InterbankTransfer as InterbankTransferModel
from datetime import datetime
from sp_config import *
import pika, json

def ack_debit_interbank(ch, method, properties, body):
    json_request = json.loads(body)
    
    model = InterbankTransferModel()     
    function_list = {
        "DONE" : model.notify,
        "FAILED" : model.update
    }

    function_list[json_request['status']](json_request['transaction_id'], {
        "journal_number" : json_request['journal_number'],
        "status" : json_request['status'],
        "message" : json_request['message']
    }) 
    
    print(f"execute ack_debit_interbank; message: {json_request}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
channel = connection.channel()
channel.queue_declare(queue='ack_debit-INTERBANK')
channel.basic_consume(queue='ack_debit-INTERBANK', on_message_callback=ack_debit_interbank, auto_ack=True)