from mongoengine import *


class Contact(Document):
    fullname = StringField(required=True, max_length=150)
    email = StringField(max_length=50)
    phone = StringField(max_length=30)
    preferable_contact = IntField(required=True, min_value=1, max_value=2)
    is_message_sent = BooleanField(required=True, default=False)
    meta = {'allow_inheritance': True, 'collection': 'contacts'}
