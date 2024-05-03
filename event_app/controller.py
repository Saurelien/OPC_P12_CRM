from datetime import datetime

from event_app.model import Event
from event_app.view import EventView
from services.utils import CollaboratorService, AuthenticateService, CollaboratorValidator
from contract_app.model import Contract
from client_app.model import Client
from contract_app.view import ContractView
from collaborator_app.model import Collaborator


class MainEventController:
    contract = Contract
    client = Client
    support_contact = Collaborator
    @staticmethod
    def display_existing_contract():
        """Fonction qui récupère les champs souhaité pour l'affichage des clients dans les menus"""
        event = Event.select()
        EventView.display_events(event)

    @classmethod
    def create_event(cls):
        token = AuthenticateService.load_token()

        if token:
            commercial_collaborator = CollaboratorService.get_authenticated_collaborator(token)
            if commercial_collaborator.role == Collaborator.COMMERCIAL:
                client_id = EventView.get_client_id()
                client = CollaboratorService.get_client_by_id(client_id)

                if client.commercial_assignee == commercial_collaborator:
                    event_data = EventView.get_event_details(client)
                    new_event = Event(
                        name=event_data["name"],
                        client=client,
                        event_date_start=datetime.strptime(event_data["event_date_start"], "%d %mm %Y"),
                        event_date_end=datetime.strptime(event_data["event_date_end"], "%d %m %Y"),
                        support_assignee=event_data["support_assignee"],
                        address=event_data["address"],
                        attendees=event_data["attendees"],
                        notes=event_data["notes"]
                    )
                    new_event.save()
