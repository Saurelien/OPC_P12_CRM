from services.basemodel import BaseModel
from peewee import *
from collaborator_app.model import Collaborator
from client_app.model import Client


class Contract(BaseModel):
    id = PrimaryKeyField(unique=True)
    client = ForeignKeyField(Client, backref='contracts', on_delete="CASCADE")
    total_amount = IntegerField(constraints=[Check('total_amount >= 0')])
    remaining_amount = IntegerField(constraints=[Check('total_amount >= 0')])
    is_signed = BooleanField(default=False)
    commercial_assignee = ForeignKeyField(Collaborator, backref='contracts', null=True, on_delete="SET NULL")

    def mark_as_signed(self):
        self.is_signed = True
        self.save()

    def make_payment(self, amount):
        if amount <= self.remaining_amount:
            self.remaining_amount -= amount
            self.save()
        else:
            raise ValueError("La somme dépasse le montant à payer.")
