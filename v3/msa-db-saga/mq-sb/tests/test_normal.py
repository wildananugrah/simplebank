import pika, json, pytest

RABBIT_MQ_HOST="45.113.232.164"
RABBIT_MQ_PORT="3020"

@pytest.mark.run(order=1)
def test_historical_transaction_save():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
    channel = connection.channel()

    data = {
        "transaction_type": "INTERBANK",
        "account_number": "1234567890",
        "amount": 0,
        "journal_number": "123456",
        "current_balance": 1000,
        "description": "TEST DESCRIPTION"
    }

    channel.basic_publish(exchange='',
                        routing_key='historical_transaction_save',
                        body=json.dumps(data))

    connection.close()

def test_debit():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
    channel = connection.channel()

    data = {
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

def test_ack_debit():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
    channel = connection.channel()

    data = {
        "journal_number": '123456'
    }

    channel.basic_publish(exchange='',
                        routing_key='ack_debit',
                        body=json.dumps(data))

    connection.close()

def test_reversal():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
    channel = connection.channel()

    data = {
        "journal_number": '123456'
    }

    channel.basic_publish(exchange='',
                        routing_key='reversal',
                        body=json.dumps(data))

    connection.close()

def test_ack_reversal():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
    channel = connection.channel()

    data = {
        "account_number": "1234567890",
        "amount": 100,
        "journal_number": "123456"
    }

    channel.basic_publish(exchange='',
                        routing_key='ack_reversal',
                        body=json.dumps(data))

    connection.close()
