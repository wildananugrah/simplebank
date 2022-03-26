from model.historical_transaction import HistoricalTransaction as HistTrxModel
from datetime import datetime
from sp_config import *
import pika, json

def on_historical_transaction_save(ch, method, properties, body):
    json_request = json.loads(body)
    start = datetime.now()
    hist_model = HistTrxModel()
    hist_model.transaction_type = json_request['transaction_type']
    hist_model.account_number = json_request['account_number']
    hist_model.amount = int(json_request['amount'])
    hist_model.journal_number = json_request['journal_number']
    hist_model.current_balance = int(json_request['current_balance'])
    hist_model.description = json_request['description']
    historical_trx = hist_model.save()
    print(f"execute on_historical_transaction_save; message: {json_request}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
channel = connection.channel()
channel.queue_declare(queue='historical_transaction_save')
channel.basic_consume(queue='historical_transaction_save', on_message_callback=on_historical_transaction_save, auto_ack=True)