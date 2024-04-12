from peewee import *
from config.config import db
from collaborator_app.model import Collaborator


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = CharField(unique=True)
    phone_country_code = CharField(max_length=5, default='+33')
    phone_number = IntegerField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    commercial_assignee = ForeignKeyField(Collaborator, backref='clients', null=True)

    def __str__(self):
        return self.email

    def get_full_phone_number(self):
        return f"{self.phone_country_code}{self.phone_number}"
