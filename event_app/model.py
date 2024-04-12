from peewee import *
from config.config import db
from collaborator_app.model import Collaborator
from client_app.model import Client
from contract_app.model import Contract


class BaseModel(Model):
    class Meta:
        database = db


class Event(BaseModel):
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
