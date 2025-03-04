from datetime import timedelta, datetime
from peewee import *
from collaborator_app.model import Collaborator
from client_app.model import Client
from contract_app.model import Contract
from services.basemodel import BaseModel


class Event(BaseModel):
    id = PrimaryKeyField(unique=True)
    contract = ForeignKeyField(Contract, backref='events', on_delete="CASCADE")
    client = ForeignKeyField(Client, backref='events', on_delete="CASCADE")
    client_info = TextField(null=True)
    support_contact = ForeignKeyField(Collaborator, null=True, on_delete="SET NULL")
    event_date_start = DateTimeField()
    event_date_end = DateTimeField()
    postal_address = CharField(max_length=200)
    attendees = IntegerField()
    notes = TextField(null=True)

    def __str__(self):
        return f"Event ID: Location: {self.postal_address}"

    def save(self, *args, **kwargs):
        if not self.event_date_start:
            self.event_date_start = datetime.now()
        if not self.event_date_end:
            self.event_date_end = self.event_date_start + timedelta(hours=24)
        super().save(*args, **kwargs)
