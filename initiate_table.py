from peewee import PostgresqlDatabase
from collaborator_app.model import Collaborator
from contract_app.model import Contract
from client_app.model import Client
from event_app.model import Event
from config.config import (DATABASE_NAME, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, SECRET_KEY)

SECRET_KEY = SECRET_KEY


def get_database_connection(db_name, db_user, db_password, db_host):
    print(f"Connexion a la base de donnée {db_name} en tant qu'utilisateur: {db_user} dans {db_host}")
    return PostgresqlDatabase(db_name, user=db_user, password=db_password, host=db_host)


def initialize_database():
    db = get_database_connection(DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST)
    with db:
        db.create_tables([Collaborator, Client, Contract, Event])
        print("Tables created in the final database")
    db.close()
