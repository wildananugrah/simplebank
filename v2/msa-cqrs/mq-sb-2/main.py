#!/usr/bin/env python
import pika, sys, os, json, requests, time
from dotenv import load_dotenv

load_dotenv()

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBIT_MQ_HOST'), port=os.getenv('RABBIT_MQ_PORT')))
    channel = connection.channel()

    channel.queue_declare(queue='account_transfer')
    channel.queue_declare(queue='account_payment')
    channel.queue_declare(queue='account_transfer_interbank')
    channel.queue_declare(queue='account_reversal_payment')
    channel.queue_declare(queue='account_reversal_interbank_transfer')

    channel.queue_declare(queue='transfer_account')
    channel.queue_declare(queue='transfer_account_debit')
    channel.queue_declare(queue='transfer_account_reversal')
    
    channel.queue_declare(queue='payment_account_debit')
    channel.queue_declare(queue='payment_account_reversal')
    
    def on_account_transfer(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('TRANSFER_HOST')}/transfer/update/", json=message)
        print(f"channel account->transfer; message has been sent: {message}")

    def on_account_payment(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('PAYMENT_HOST')}/payment/update", json=message)
        print(f"channel account->payment; message has been sent: {message}")

    def on_account_transfer_interbank(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('TRANSFER_HOST')}/transfer/update/interbank", json=message)
        print(f"channel account->transfer_interbank; message has been sent: {message}")

    def on_account_reversal_payment(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('PAYMENT_HOST')}/payment/update/reversal", json=message)
        print(f"channel account->reversal_payment; message has been sent: {message}")
    
    def on_account_reversal_interbank_transfer(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('TRANSFER_HOST')}/transfer/update/reversal/interbank", json=message)
        print(f"channel account->reversal_interbank_transfer; message has been sent: {message}")
    
    def on_transfer_account(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('ACCOUNT_HOST')}/account/transfer/", json=message)
        print(f"channel transfer->account=>transfer; message has been sent: {message}")
    
    def on_transfer_account_debit(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('ACCOUNT_HOST')}/account/debit/", json=message)
        print(f"channel transfer->account=>debit; message has been sent: {message}")

    def on_transfer_account_reversal(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('ACCOUNT_HOST')}/account/reversal/", json=message)
        print(f"channel transfer->account=>reversal; message has been sent: {message}")
    
    def on_payment_account_debit(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('ACCOUNT_HOST')}/account/debit/", json=message)
        print(f"channel payment->account=>debit; message has been sent: {message}")

    def on_payment_account_reversal(ch, method, properties, body):
        message = json.loads(body)
        requests.post(f"{os.getenv('ACCOUNT_HOST')}/account/reversal/", json=message)
        print(f"channel payment->account=>reversal; message has been sent: {message}")

    channel.basic_consume(queue='account_transfer', on_message_callback=on_account_transfer, auto_ack=True)
    channel.basic_consume(queue='account_payment', on_message_callback=on_account_payment, auto_ack=True)
    channel.basic_consume(queue='account_transfer_interbank', on_message_callback=on_account_transfer_interbank, auto_ack=True)
    channel.basic_consume(queue='account_reversal_payment', on_message_callback=on_account_reversal_payment, auto_ack=True)
    channel.basic_consume(queue='account_reversal_interbank_transfer', on_message_callback=on_account_reversal_interbank_transfer, auto_ack=True)
    
    channel.basic_consume(queue='transfer_account', on_message_callback=on_transfer_account, auto_ack=True)
    channel.basic_consume(queue='transfer_account_debit', on_message_callback=on_transfer_account_debit, auto_ack=True)
    channel.basic_consume(queue='transfer_account_reversal', on_message_callback=on_transfer_account_reversal, auto_ack=True)
    channel.basic_consume(queue='payment_account_debit', on_message_callback=on_payment_account_debit, auto_ack=True)
    channel.basic_consume(queue='payment_account_reversal', on_message_callback=on_payment_account_reversal, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)