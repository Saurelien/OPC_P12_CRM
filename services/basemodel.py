from datetime import datetime
from peewee import *
from config.config import db


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField()

    class Meta:
        database = db

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)
