import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='historical_transaction')

data = {
        "account_number": "1122344", 
        "current_account_balance": "443321", 
        "amount": "100", 
        "action": "CREDIT",
        "transaction_type" : "TRANSFER"
    }

channel.basic_publish(exchange='',
                      routing_key='historical_transaction',
                      body=json.dumps(data))
                      
print(" [x] Sent 'Hello World!'")

connection.close()