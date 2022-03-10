from dataclasses import dataclass
from sp_config import *
import requests, os, pika

@dataclass
class Transaction:

    from_account_number: str = None
    transaction_type: str = None
    cif_number: str = None
    amount: int = 0
    journal_number: str = None
    description: str = None
    transaction_id: str = None

    def debit(self):
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
        channel = connection.channel()

        data = {
            "transaction_id" : self.transaction_id,
            "from_account_number": self.from_account_number,
            "transaction_type": self.transaction_type,
            "cif_number": self.cif_number,
            "amount": self.amount,
            "description": self.description
        }

        channel.basic_publish(exchange='',
                            routing_key='debit',
                            body=json.dumps(data))

        connection.close()
    
    def reversal(self):
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
        channel = connection.channel()

        data = {
            "account_number": self.from_account_number,
            "amount": self.amount,
            "journal_number": self.journal_number
        }

        channel.basic_publish(exchange='',
                            routing_key='reversal',
                            body=json.dumps(data))

        connection.close()
