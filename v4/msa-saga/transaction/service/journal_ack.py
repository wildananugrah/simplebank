from dataclasses import dataclass
from sp_config import *
import pika, json

@dataclass
class JournalAck:

    journal_number: str = str

    def notify_journal(self, transaction_type, request_message, ack_type):
        print(f"sent request message: {request_message} ack_type: {ack_type} transaction_type: {transaction_type} ")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
        channel = connection.channel()

        channel.basic_publish(exchange='',routing_key=f"{ack_type}-{transaction_type}", body=json.dumps(request_message))

        connection.close()  
