from dataclasses import dataclass
from sp_config import *
from datetime import datetime
import pika, json

@dataclass
class HistoricalTransaction:

    transaction_type: str = None
    account_number: str = None
    amount: int = 0
    journal_number: str = str
    current_balance: int = 0
    description: str = None

    def save(self):
        try:
            data = {
                'transaction_type': self.transaction_type,
                'account_number': self.account_number,
                'amount': self.amount,
                'journal_number': self.journal_number,
                'current_balance': self.current_balance,
                'description': self.description
            }
            print(f"sent queue: {data}")
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
            channel = connection.channel()

            channel.basic_publish(exchange='',
                                routing_key='historical_transaction_save',
                                body=json.dumps(data))

            connection.close()
        except Exception as error:
            print(f"ERROR: {error}")
