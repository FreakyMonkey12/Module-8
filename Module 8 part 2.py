import pika
import json
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField

connect('my_database', host='mongodb://username:password@host:port/my_database')

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='email_queue')

fake = Faker()
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    contact = Contact(fullname=fullname, email=email)
    contact.save()
    message = {'contact_id': str(contact.id)}
    channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))

print("Contacts and messages sent to queue.")
connection.close()

def send_email(contact_id):
    contact = Contact.objects.get(id=contact_id)
    contact.sent = True
    contact.save()

def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    send_email(contact_id)

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()

