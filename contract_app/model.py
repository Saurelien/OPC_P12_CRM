from peewee import *
from config.config import db
from collaborator_app.model import Collaborator
from client_app.model import Client


class BaseModel(Model):
    class Meta:
        database = db


class Contract(BaseModel):
    id = PrimaryKeyField(unique=True)
    client = ForeignKeyField(Client, backref='contracts', on_delete="CASCADE")
    total_amount = IntegerField()
    remaining_amount = IntegerField()
    created_date = DateField()
    updated_at = DateTimeField()
    is_signed = BooleanField(default=False)
    manager_assignee = ForeignKeyField(Collaborator, backref='contracts', null=True, on_delete="CASCADE")

    def mark_as_signed(self):
        self.is_signed = True
        self.save()

    def make_payment(self, amount):
        if amount <= self.remaining_amount:
            self.remaining_amount -= amount
            self.save()
        else:
            raise ValueError("La somme dépasse le montant à payer.")

    # def save(self, *args, **kwargs):
    #     if self.manager_assignee.role != Collaborator.COMMERCIAL:
    #         raise ValueError("Le commercial assigné doit être un collaborateur ayant le rôle de commercial.")
