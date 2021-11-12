import requests, os, pika, json

class TransactionModel():

    def __init__(self, db):
        self.db = db

    def transfer(self, from_account_number, db_from_account_number, to_account_number, db_to_account_number, journal_number, amount, timestamp):
        
        current_from_account_balance = db_from_account_number.balance - amount
        db_from_account_number.balance = current_from_account_balance

        current_to_account_balance = db_to_account_number.balance + amount
        db_to_account_number.balance = current_to_account_balance
        self.db.commit()
        
        rabbit_mq_host = os.environ.get("RABBIT_MQ_HOST")
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_mq_host))
        channel = connection.channel()

        channel.queue_declare(queue='historical_transaction')

        data = {
            "account_number": from_account_number, 
            "current_account_balance": current_from_account_balance,
            "amount": amount, 
            "action": "DEBIT",
            "transaction_type" : "TRANSFER"
        }

        channel.basic_publish(exchange='',
                            routing_key='historical_transaction',
                            body=json.dumps(data))
                            
        print(f" [x] Sent {data}")

        data = {
            "account_number": to_account_number, 
            "current_account_balance": current_to_account_balance, 
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "TRANSFER"
        }

        channel.basic_publish(exchange='',
                            routing_key='historical_transaction',
                            body=json.dumps(data))
                            
        print(f" [x] Sent {data}")

        connection.close()

        return True

    def deposit(self, account_number, db_account_number, journal_number, amount, timestamp):

        current_account_balance = db_account_number.balance + amount
        db_account_number.balance = current_account_balance
        self.db.commit()

        rabbit_mq_host = os.environ.get("RABBIT_MQ_HOST")
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_mq_host))
        channel = connection.channel()

        channel.queue_declare(queue='historical_transaction')

        request_json = {
            "account_number": account_number, 
            "current_account_balance": current_account_balance,
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "DEPOSIT"
        }

        channel.basic_publish(exchange='',
                            routing_key='historical_transaction',
                            body=json.dumps(request_json))
                            
        print(f" [x] Sent {request_json}")

        connection.close()

        return True
