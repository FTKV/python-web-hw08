import json
import time
import sys

import pika

from connect import db_name, client_mongo
from models import Contact


exec(f"db = client_mongo.{db_name}")


def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    contact = Contact.objects(id=message.get("id"))[0]
    print(f" [x] Sending email to {contact.email}")
    contact.update(is_message_sent=True)
    time.sleep(1)
    print(f" [x] Done: {method.delivery_tag}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():

    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='task_email', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_email', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
