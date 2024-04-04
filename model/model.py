from peewee import *
from config.config import db
from datetime import datetime
import secrets
from argon2 import PasswordHasher

PH = PasswordHasher()


class BaseModel(Model):
    class Meta:
        database = db


class Collaborator(BaseModel):
    COMMERCIAL = 'C'
    GESTION = 'G'
    SUPPORT = 'S'

    ROLE_CHOICES = [
        (COMMERCIAL, 'Commercial'),
        (GESTION, 'Gestion'),
        (SUPPORT, 'Support'),
    ]

    ROLE_CHOICES_DICT = dict(ROLE_CHOICES)

    id = PrimaryKeyField(unique=True)
    username = CharField(unique=True)
    password = CharField()
    first_name = CharField()
    last_name = CharField()
    role = CharField(choices=ROLE_CHOICES, default=GESTION)

    def __str__(self):
        return f"{self.username}, {self.role}"

    def set_password(self, password):
        salt_a_bit = secrets.token_bytes(16)
        salt_hex = salt_a_bit.hex()
        hashing_password = PH.hash(password + salt_hex)
        self.password = hashing_password

    def verify_password(self, password):
        try:
            return PH.verify(self.password, password)
        except:
            return False

    @classmethod
    def username_exists(cls, username):
        return cls.select().where(cls.username == username).exists()


class Client(BaseModel):
    id = PrimaryKeyField(unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = CharField(unique=True)
    phone_country_code = CharField(max_length=5, default='+33')
    phone_number = CharField(max_length=10)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()
    commercial_assignee = ForeignKeyField(Collaborator, backref='clients', null=True)

    def __str__(self):
        return self.email

    def get_full_phone_number(self):
        return f"{self.phone_country_code}{self.phone_number}"


class Contract(BaseModel):
    id = PrimaryKeyField(unique=True)
    client = ForeignKeyField(Client, backref='contracts')
    total_amount = IntegerField()
    remaining_amount = IntegerField()
    created_date = DateField()
    updated_at = DateTimeField()
    is_signed = BooleanField(default=False)
    manager_assignee = ForeignKeyField(Collaborator, backref='contracts', null=True)

    def mark_as_signed(self):
        self.is_signed = True
        self.save()

    def make_payment(self, amount):
        if amount <= self.remaining_amount:
            self.remaining_amount -= amount
            self.save()
        else:
            raise ValueError("La somme dépasse le montant à payer.")


class Event(BaseModel):
    id = PrimaryKeyField(unique=True)
    contract = ForeignKeyField(Contract, backref='events')
    client = ForeignKeyField(Client, backref='events')
    support_contact = ForeignKeyField(Collaborator)
    event_date_start = DateTimeField()
    event_date_end = DateTimeField()
    postal_address = CharField(max_length=200)
    attendees = IntegerField()
    notes = TextField(null=True)

    def __str__(self):
        return f"Event ID: Location: {self.postal_address}"
