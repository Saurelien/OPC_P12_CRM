import datetime
import re
from client_app.model import Client
from client_app.view import ClientView
from collaborator_app.model import Collaborator
from services.utils import AuthenticateService, CollaboratorService, Session


class MainClientController:

    @staticmethod
    def display_existing_client():
        client = Client.select()
        ClientView.display_clients(client)

    @classmethod
    def create_client(cls):
        """test de la fonction current_user retournant un utilisateur authentifié"""
        if not Session.is_commercial():
            return

        client_data = ClientView.display_create_client_basic_info()
        client_data["email"] = cls.get_valid_email()
        client_data["phone_number"] = ClientView.prompt_phone_number()
        client_data["commercial_assignee"] = Session.get_current_user().username

        new_client = Client.create(
            first_name=client_data["first_name"],
            last_name=client_data["last_name"],
            email=client_data["email"],
            phone_number=client_data["phone_number"],
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            commercial_assignee=Session.get_current_user()
        )
        ClientView.display_client_table(new_client)
        return new_client

    @classmethod
    def modify_client(cls):
        if not Session.is_commercial():
            return None

        clients = Client.select().where(
            (Client.commercial_assignee == Session.get_current_user())
        )
        ClientView.display_clients_table(clients)
        client_id = ClientView.prompt_client_id(clients)
        if not client_id:
            ClientView.display_error("NO_CLIENT_SELECTED")
            return None

        client = Client.get_or_none(Client.id == client_id)
        if not client:
            ClientView.display_error("CLIENT_NOT_EXIST")
            return None

        ClientView.display_client_details(client)
        new_client_data = ClientView.prompt_modified_client_data()

        if new_client_data["first_name"]:
            client.first_name = new_client_data["first_name"]
        if new_client_data["last_name"]:
            client.last_name = new_client_data["last_name"]
        if new_client_data["email"]:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", new_client_data["email"]):
                ClientView.display_error("INVALID_EMAIL_FORMAT")
                return None
            if Client.select().where((Client.email == new_client_data["email"]) & (Client.id != client_id)).exists():
                ClientView.display_error("EMAIL_ALREADY_EXISTS")
                return None
            client.email = new_client_data["email"]
        if new_client_data["phone_number"]:
            client.phone_number = new_client_data["phone_number"]

        client.save()
        ClientView.display_client_details(client)
        ClientView.display_success("SUCCESS_MODIFY")
        return client

    @staticmethod
    def get_valid_email():
        while True:
            email = ClientView.prompt_email()
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                ClientView.display_error("INVALID_EMAIL_FORMAT")
                continue

            if Client.select().where(Client.email == email).exists():
                ClientView.display_error("EMAIL_ALREADY_EXISTS")
            else:
                break

        return email
