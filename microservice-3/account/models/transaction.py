from databases.historical_transaction import HistoricalTransactionDB
import requests, os, pika, json

class TransactionModel():
    def __init__(self, db=None):
        self.db = db

    def transfer(self, from_account_number, to_account_number, journal_number, amount, timestamp):
        
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='historical_transaction')

        account_url = os.environ.get("ACCOUNT_HOST")
        response_from_account = requests.post(f"{account_url}/account/update_balance", json={
            "account" : from_account_number,
            "action" : "DEBIT",
            "amount": amount
        })

        response_to_account = requests.post(f"{account_url}/account/update_balance", json={
            "account" : to_account_number,
            "action" : "CREDIT",
            "amount": amount
        })

        data = {
            "account_number": from_account_number, 
            "current_account_balance": response_from_account.json()['balance'], 
            "amount": amount, 
            "action": "DEBIT",
            "transaction_type" : "TRANSFER"
        }

        channel.basic_publish(exchange='', routing_key='historical_transaction', body=json.dumps(data))
        print(f" [x] Sent: {json.dumps(data)}")

        data = {
            "account_number": to_account_number, 
            "current_account_balance": response_to_account.json()['balance'], 
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "TRANSFER"
        }

        channel.basic_publish(exchange='', routing_key='historical_transaction', body=json.dumps(data))
        print(f" [x] Sent: {json.dumps(data)}")

        connection.close()

        return True

    def deposit(self, account_number, journal_number, amount, timestamp):

        account_url = os.environ.get("ACCOUNT_HOST")
        response = requests.post(f"{account_url}/account/update_balance", json={
            "account" : account_number,
            "action" : "CREDIT",
            "amount": amount
        })

        response = requests.get(f"{account_url}/account?account={account_number}")
        response_json = response.json()

        data = {
            "account_number": account_number, 
            "current_account_balance": response_json['balance'], 
            "amount": amount, 
            "action": "CREDIT",
            "transaction_type" : "DEPOSIT"
        }

        channel.basic_publish(exchange='', routing_key='historical_transaction', body=json.dumps(data))
        print(f" [x] Sent: {json.dumps(data)}")

        if response.status_code != 200:
            return False

        return True
