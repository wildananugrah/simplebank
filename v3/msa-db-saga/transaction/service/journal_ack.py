from dataclasses import dataclass
from sp_config import *
import pika

@dataclass
class JournalAck:

    journal_number: str = str

    def notify_journal(self, transaction_type, request_message, ack_type):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
        channel = connection.channel()

        data = {
            "transaction_type" : transaction_type,
            "request_message" : request_message
        }

        channel.basic_publish(exchange='',routing_key=ack_type, body=json.dumps(data))

        connection.close()  
