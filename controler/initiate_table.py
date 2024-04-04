from peewee import PostgresqlDatabase
from model.model import Client, Contract, Collaborator, Event
from config.config import DATABASE_NAME, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD

db = PostgresqlDatabase(DATABASE_NAME,
                        user=DATABASE_USER,
                        password=DATABASE_PASSWORD,
                        host=DATABASE_HOST)

if db.database == DATABASE_NAME:
    print("DB existante")
else:
    print("DB inexistante")

if not Collaborator.table_exists():
    db.create_tables([Collaborator], safe=True)
    print("La table", Collaborator._meta.table_name, "a été crée")
else:
    print("La table", Collaborator._meta.table_name, "existe déjà.")

if not Client.table_exists():
    db.create_tables([Client], safe=True)
    print("La table", Client._meta.table_name, "a été crée")
else:
    print("La table", Client._meta.table_name, "existe déjà.")

if not Contract.table_exists():
    db.create_tables([Contract], safe=True)
    print("La table", Contract._meta.table_name, "a été crée")
else:
    print("La table", Contract._meta.table_name, "existe déjà.")

if not Event.table_exists():
    db.create_tables([Event], safe=True)
    print("La table", Event._meta.table_name, "a été crée")
else:
    print("La table", Event._meta.table_name, "existe déjà.")

