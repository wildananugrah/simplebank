#!/usr/bin/env python
import pika, sys, os, json

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='historical_transaction')

    def callback(ch, method, properties, body):
        message = json.loads(body)
        historical_transaction_url = os.environ.get("HISTORICAL_TRANSACTION_HOST")
        requests.post(f"{historical_transaction_url}/historical_transaction", json=message)

    channel.basic_consume(queue='historical_transaction', on_message_callback=callback, auto_ack=True)

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