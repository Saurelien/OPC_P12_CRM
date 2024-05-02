from services.utils import CollaboratorService, AuthenticateService, CollaboratorValidator
from client_app.model import Client
from client_app.view import ClientView


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
