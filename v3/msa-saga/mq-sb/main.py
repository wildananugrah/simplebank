#!/usr/bin/env python
from dotenv import load_dotenv
from sp_config import *
import pika, sys, os, json, requests, time

load_dotenv()

# HELPER [STARTED]

# def ack_debit_payment(message):
#     requests.post(f"{PAYMENT_HOST}/transaction/payment/eletrical/update/", json=message)
#     print(f"execute payment::ack_debit; message has been sent: {message}")

# def ack_debit_interbank(message):
#     requests.post(f"{INTERBANK_HOST}/transaction/transfer/interbank/update/", json=message)
#     print(f"execute interbank::ack_debit; message has been sent: {message}")

# HELPER [ENDED]

# CONFIG [STARTED]

# function_dict = {
#     "ELECTRICAL_BILLPAYMENT" : ack_debit_payment,
#     "INTERBANK" : ack_debit_interbank
# }

# CONFIG [ENDED]

# def on_historical_transaction_save(ch, method, properties, body):
#     message = json.loads(body)
#     requests.post(f"{HISTORICAL_TRANSACTION_HOST}/historical_transaction/", json=message)
#     print(f"execute historical_transcation::save; message has been sent: {message}")

# def on_debit(ch, method, properties, body):
#     message = json.loads(body)
#     requests.post(f"{TRANSACTION_HOST}/transaction/debit/", json=message)
#     print(f"execute historical_transcation::save; message has been sent: {message}")

# def reversal(ch, method, properties, body):
#     message = json.loads(body)
#     requests.post(f"{TRANSACTION_HOST}/transaction/reversal/", json=message)
#     print(f"execute historical_transcation::reversal; message has been sent: {message}")

# def on_ack_debit(ch, method, properties, body):
#     message = json.loads(body)
#     function_dict[message['transaction_type']](message['request_message'])

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_MQ_HOST, port=RABBIT_MQ_PORT))
    channel = connection.channel()

    # channel.queue_declare(queue='historical_transaction_save')
    
    # channel.queue_declare(queue='debit')
    # channel.queue_declare(queue='ack_debit')

    # channel.queue_declare(queue='reversal')
    
    # channel.basic_consume(queue='historical_transaction_save', on_message_callback=on_historical_transaction_save, auto_ack=True)

    # channel.basic_consume(queue='debit', on_message_callback=on_debit, auto_ack=True)
    # channel.basic_consume(queue='ack_debit', on_message_callback=on_ack_debit, auto_ack=True)

    # channel.basic_consume(queue='reversal', on_message_callback=reversal, auto_ack=True)
    
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