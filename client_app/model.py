from peewee import *
from collaborator_app.model import Collaborator
from services.basemodel import BaseModel


class Client(BaseModel):
    id = PrimaryKeyField(unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = CharField()
    phone_number = CharField()
    commercial_assignee = ForeignKeyField(Collaborator, backref='clients', null=True, on_delete="SET NULL")

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.email

    def get_full_phone_number(self):
        return f"{self.phone_number}"
