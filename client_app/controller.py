import datetime
import re
from client_app.model import Client
from client_app.view import ClientView, display_client_table
from collaborator_app.model import Collaborator
from services.utils import AuthenticateService, CollaboratorService


class MainClientController:

    @staticmethod
    def display_existing_client():
        """Fonction qui récupère les champs souhaité pour l'affichage des clients dans les menus"""
        client = Client.select(
            Client.id,
            Client.first_name,
            Client.last_name,
            Client.email,
            Client.phone_number,
            Client.created_at,
            Client.updated_at,
            Client.commercial_assignee)
        ClientView.display_clients(client)

    @classmethod
    def create_client(cls):
        client_data = ClientView.display_create_client()
        token = AuthenticateService.load_token()

        if token:
            user_id = AuthenticateService.decode_token(token)
            commercial_collaborator = CollaboratorService.get_collaborator_by_id(user_id)

            if commercial_collaborator.role == Collaborator.COMMERCIAL:
                email_value = client_data["email"]
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email_value):
                    raise ValueError("Format d'email incorrect.")
                email = email_value
                new_client = Client(
                    first_name=client_data["first_name"],
                    last_name=client_data["last_name"],
                    email=email,
                    phone_number=client_data["phone_number"],
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now(),
                    commercial_assignee=commercial_collaborator
                )
                new_client.save()
                display_client_table(client_data)
