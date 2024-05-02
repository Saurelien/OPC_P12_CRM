from peewee import *
from config.config import db
from collaborator_app.model import Collaborator


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    id = PrimaryKeyField(unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = CharField()
    phone_number = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    commercial_assignee = ForeignKeyField(Collaborator, backref='clients', on_delete="CASCADE")

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def get_full_phone_number(self):
        return f"{self.phone_country_code}{self.phone_number}"
