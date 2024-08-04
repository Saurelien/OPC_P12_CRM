import datetime
import peewee
from rich.console import Console
from event_app.model import Event
from event_app.view import EventView
from services.utils import CollaboratorService, AuthenticateService, Session
from contract_app.model import Contract
from client_app.model import Client
from collaborator_app.model import Collaborator
import logging

logging.basicConfig(level=logging.INFO)

console = Console()


class MainEventController:
    contract = Contract
    client = Client
    support_contact = Collaborator

    @classmethod
    def display_existing_event(cls):
        if not Session.user:
            return
        events = Event.select()
        if not events.exists():
            EventView.display_error("NO_EVENTS_FOUND")
            return

        EventView.display_events(events)

    @classmethod
    def create_event(cls):
        if not Session.is_commercial():
            return

        clients_with_signed_contracts = Contract.select().join(Client).where(
            (Contract.commercial_assignee == Session.get_current_user()) &
            Contract.is_signed
        )

        if not clients_with_signed_contracts.exists():
            EventView.display_error("NO_SIGNED_CONTRACTS")
            return

        contract_id = EventView.get_contract_id(clients_with_signed_contracts)
        contract = Contract.get(Contract.id == contract_id)
        event_data = EventView.get_event_details()
        support_collaborators = Collaborator.select().where(Collaborator.role == Collaborator.SUPPORT)
        support_contact_id = EventView.get_support_contact_id(support_collaborators)
        support_contact = Collaborator.get(Collaborator.id == support_contact_id)

        client = contract.client
        client_info = "\n".join([
            f"Prénom: {client.first_name}",
            f"Nom: {client.last_name}",
            f"Email: {client.email}",
            f"Téléphone: {client.phone_number}"
        ]) if client else None

        new_event = Event(
            contract=contract,
            client=client,
            client_info=client_info,
            support_contact=support_contact,
            event_date_start=datetime.datetime.now(),
            event_date_end=datetime.datetime.now() + datetime.timedelta(hours=24),
            postal_address=event_data['address'],
            attendees=int(event_data['attendees']),
            notes=event_data['notes']
        )
        new_event.save()
        EventView.display_event_detail(new_event, event_data["name"])
        return new_event

    @classmethod
    def modify_event(cls):
        if Session.user is None or (not Session.is_gestion() and not Session.is_support()):
            EventView.display_error("UNAUTHORIZED_ACCESS")
            return None

        authenticated_collaborator = Session.user
        print(f"Utilisateur authentifié: {authenticated_collaborator}")

        if not authenticated_collaborator:
            EventView.display_error("COLLABORATOR_NOT_FOUND")
            return None

        if Session.is_gestion():
            events = Event.select()
            print("Tous les événements sont sélectionnés pour un gestionnaire.")
        else:
            events = Event.select().where(Event.support_contact == authenticated_collaborator)
            print(f"Événements sélectionnés pour le support collaborateur: {authenticated_collaborator}")

        if not events.exists():
            EventView.display_error("NO_EVENTS_FOUND")
            return None

        event_id = EventView.get_event_id_to_modify(events)
        print(f"ID de l'événement à modifier: {event_id}")

        try:
            event = Event.get_by_id(event_id)
            print(f"Événement trouvé: {event}")
        except peewee.DoesNotExist:
            EventView.display_error("INVALID_EVENT_ID")
            return None

        support_collaborators = Collaborator.select().where(Collaborator.role == Collaborator.SUPPORT)
        event_data = EventView.get_event_modification_details(event, support_collaborators)
        print(f"Données de modification de l'événement: {event_data}")

        if 'support_contact' in event_data:
            support_contact_id = event_data['support_contact']
            try:
                new_support_contact = Collaborator.get_by_id(support_contact_id)
                if new_support_contact.role != Collaborator.SUPPORT:
                    EventView.display_error("INVALID_SUPPORT_CONTACT_ROLE")
                    return None
                event.support_contact = new_support_contact
                print(f"Contact de support mis à jour: {new_support_contact}")
            except peewee.DoesNotExist:
                EventView.display_error("INVALID_SUPPORT_CONTACT_ID")
                return None

        event.attendees = event_data.get("attendees", event.attendees)
        event.notes = event_data.get("notes", event.notes)
        event.save()
        print(f"Événement modifié avec succès: {event.id}")
        return event

    @classmethod
    def list_events(cls):
        token = AuthenticateService.load_token()
        if not token:
            return

        user_id = AuthenticateService.decode_token(token)
        authenticated_collaborator = CollaboratorService.get_collaborator_by_id(user_id)
        if not authenticated_collaborator:
            return

        if authenticated_collaborator.role == Collaborator.SUPPORT:
            events = Event.select().where(Event.support_contact == authenticated_collaborator)
        else:
            events = Event.select()

        if not events.exists():
            EventView.display_error("NO_EVENTS_FOUND")
            return

        EventView.display_events(events)
