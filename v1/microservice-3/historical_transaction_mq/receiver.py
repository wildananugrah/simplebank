from dotenv import load_dotenv
import pika, sys, os, json, requests

def main():
    rabbit_mq_host = os.environ.get("RABBIT_MQ_HOST")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_host))
    channel = connection.channel()

    channel.queue_declare(queue='historical_transaction')

    def callback(ch, method, properties, body):
        message = json.loads(body)
        historical_transaction_url = os.environ.get("HISTORICAL_TRANSACTION_HOST")
        print(f"Message received: {message}")
        requests.post(f"{historical_transaction_url}/historical_transaction", json=message)

    channel.basic_consume(queue='historical_transaction', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        load_dotenv()
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)