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
    phone_country_code = CharField(max_length=5, default='+33')
    phone_number = CharField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    commercial_assignee = ForeignKeyField(Collaborator, backref='clients', null=True, on_delete="CASCADE")

    def validate_email(self) -> bool:
        return '@' in self.email and '.' in self.email

    def save(self, *args, **kwargs):
        self.validate_email()
        if self.commercial_assignee.role != Collaborator.COMMERCIAL:
            raise ValueError("Le commercial assigné doit être un collaborateur ayant le rôle de commercial.")

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def get_full_phone_number(self):
        return f"{self.phone_country_code}{self.phone_number}"
