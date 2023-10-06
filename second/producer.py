import json
from random import randint

import faker
import pika

from connect import db_name, client_mongo
from models import Contact


exec(f"db = client_mongo.{db_name}")

NUMBER_CONTACTS = 100

fake_data = faker.Faker("uk_UA")

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_exchange', exchange_type='direct')
channel.queue_declare(queue='task_email', durable=True)
channel.queue_bind(exchange='task_exchange', queue='task_email')
channel.queue_declare(queue='task_sms', durable=True)
channel.queue_bind(exchange='task_exchange', queue='task_sms')

def get_fake_contacts():
    for _ in range(NUMBER_CONTACTS):
        Contact(fullname=fake_data.name(), email=fake_data.email(), phone=fake_data.phone_number(), preferable_contact=randint(1, 2)).save()


def main():
    for contact in Contact.objects:
        if not contact.is_message_sent:
            message = {
                "id": str(contact.id)
            }

            channel.basic_publish(
                exchange='task_exchange',
                routing_key='task_email' if contact.preferable_contact == 1 else 'task_sms',
                body=json.dumps(message).encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                )
            )

            print(" [x] Sent %r" % message)


if __name__ == '__main__':
    get_fake_contacts()
    main()
    connection.close()