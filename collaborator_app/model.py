from peewee import *
from config.config import SECRET_KEY
import argon2
from services.basemodel import BaseModel

PH = argon2.PasswordHasher()


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
        salted_password = password + SECRET_KEY
        hashed_password = PH.hash(salted_password)
        self.password = hashed_password

    def verify_password(self, password):
        try:
            PH.verify(self.password, password + SECRET_KEY)
            return True
        except:
            return False

    @classmethod
    def username_exists(cls, username):
        return cls.select().where(cls.username == username).exists()

    @staticmethod
    def validate_username(username):
        return not Collaborator.username_exists(username)

    @staticmethod
    def validate_password(password1, password2):
        return password1 == password2

    @staticmethod
    def validate_role(role_code):
        return role_code in ['C', 'G', 'S']
