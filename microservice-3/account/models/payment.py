from databases.h2h_lookup import H2HLookupDB
from models.historical_transaction import HistoricalTransactionModel

import os, requests, pika, json

class Payment():
    def __init__(self, url, db=None):
        self.db = db
        self.url = url
        self.request_message = None

    def debit(self, account_number, amount):
        db_account = AccountModel(self.db).detail(account_number)
        db_account.balance = db_account.balance - amount
        self.db.commit()
        
        journal_number = HistoricalTransactionModel().generate_journal_number()

        rabbit_mq_host = os.environ.get("RABBIT_MQ_HOST")
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_mq_host))
        channel = connection.channel()

        channel.queue_declare(queue='historical_transaction')

        data = {
            "account_number": account_number, 
            "current_account_balance": db_account.balance, 
            "amount": amount, 
            "action": "DEBIT",
            "transaction_type" : "PAYMENT"
        }

        channel.basic_publish(exchange='',
                            routing_key='historical_transaction',
                            body=json.dumps(data))
                            
        print(f" [x] Sent {data}")

        return True

    def insert_to_h2hlookup(self, bill_id, bill_type, transaction_type, account_number, cif_number, action, status):
        db_h2h_lookup = H2HLookupDB(
            bill_id=bill_id,
            bill_type=bill_type,
            transaction_type=transaction_type, 
            account_number=account_number, 
            cif_number=cif_number,
            action=action, 
            status=status
        )

        self.db.add(db_h2h_lookup)
        self.db.commit()

        return True