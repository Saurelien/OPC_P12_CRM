import peewee
from peewee import PostgresqlDatabase
from collaborator_app.model import Collaborator
from contract_app.model import Contract
from client_app.model import Client
from event_app.model import Event
from config.config import DATABASE_NAME, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, SECRET_KEY

SECRET_KEY = SECRET_KEY


def initialize_database():
    db = PostgresqlDatabase(DATABASE_NAME,
                            user=DATABASE_USER,
                            password=DATABASE_PASSWORD,
                            host=DATABASE_HOST)

    if db.database == DATABASE_NAME:
        print("DB existante")
    else:
        return
    if not Collaborator.select().where(Collaborator.username == 'admin').exists():
        create_admin_collaborator()
    # Créer les tables si elles n'existent pas
    for model_class in [Collaborator, Client, Contract, Event]:
        if not model_class.table_exists():
            db.create_tables([model_class], safe=True)
        else:
            return


def create_admin_collaborator():
    if not Collaborator.select().where(Collaborator.username == 'admin').exists():
        predefined_data = {
            "username": "admin",
            "password": "admin123",
            "first_name": "Admin",
            "last_name": "Admin",
            "role": "Gestion"
        }

        primary_collaborator = Collaborator(
            username=predefined_data["username"],
            first_name=predefined_data["first_name"],
            last_name=predefined_data["last_name"],
            role=predefined_data["role"]
        )
        primary_collaborator.set_password(predefined_data["password"])

        try:
            primary_collaborator.save()
        except peewee.IntegrityError as e:
            print(e)
    else:
        print("Un collaborateur administrateur existe déjà.")

