import datetime
from unittest.mock import patch
from collaborator_app.model import Collaborator
from event_app.controller import MainEventController
from services.utils import Session
from utils import generate_contract_data, generate_collaborator, generate_event_data, generate_client


def test_create_event(test_track, session_user_commercial):
    contract = generate_contract_data(is_signed=True)
    commercial_contract_assignee = contract.commercial_assignee
    Session.user = commercial_contract_assignee
    client = contract.client
    support_contact = generate_collaborator(role=Collaborator.SUPPORT)
    client_info = (
        f"Prénom: {client.first_name}\n"
        f"Nom: {client.last_name}\n"
        f"Email: {client.email}\n"
        f"Téléphone: {client.phone_number}"
    )
    fixed_now = datetime.datetime(2024, 7, 15)
    fixed_end = fixed_now + datetime.timedelta(hours=24)
    event_data = {
        'contract': contract,
        'name': 'Nom de l\'event totot',
        'client': client,
        'client_info': client_info,
        'support_contact': support_contact,
        'event_date_start': fixed_now,
        'event_date_end': fixed_end,
        'postal_address': "123 rue de la soif",
        'attendees': "100",
        'notes': "Additional notes"
    }
    with patch("rich.prompt.Prompt.ask", side_effect=[
        str(contract.id),
        event_data['name'],
        event_data['postal_address'],
        event_data['attendees'],
        event_data['notes'],
        str(support_contact.id),
        event_data['client_info']
    ]), patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_now
        created_event = MainEventController.create_event()
    assert created_event is not None, "L'événement n'a pas été créé."
    assert created_event.client_info == event_data['client_info'], "les informé sont introuvables"
    assert created_event.support_contact.id == support_contact.id, "support de l'event non trouvé"
    assert created_event.event_date_start.strftime("%d-%m-%Y") == fixed_now.strftime("%d-%m-%Y"), "Format invalide"
    assert created_event.event_date_end.strftime("%d-%m-%Y") == fixed_end.strftime(
        "%d-%m-%Y"), "Format invalide"
    assert created_event.postal_address == event_data["postal_address"], "Adresse invalide"
    assert created_event.attendees == int(event_data["attendees"]), "Doit être un entier"
    assert created_event.notes == event_data["notes"], "Textfield introuvable"
    assert created_event.contract == contract, "Id du contrat introuvable"
    assert created_event.client == client, "client introuvable"
    print("Test de création d'événement réussi.")


def test_modify_event_by_gestion(test_track, session_user_gestion):
    event = generate_event_data()
    print(f"NOUVELLE EVENT CREE Event ID: {event.id}, Adresse Postale: {event.postal_address}")
    new_support = generate_collaborator(role=Collaborator.SUPPORT)
    client = event.client
    contract = event.contract
    client_info = event.client_info

    fixed_now = datetime.datetime(2024, 7, 15)
    fixed_end = fixed_now + datetime.timedelta(hours=24)
    new_event_data = {
        'contract': contract.id,
        'name': 'Nom de l\'event totot 22',
        'client': client.id,
        'client_info': client_info,
        'support_contact': new_support.id,
        'event_date_start': fixed_now,
        'event_date_end': fixed_end,
        'postal_address': "123 rue de la soif",
        'attendees': int("200"),
        'notes': f"assignation d'un nouveau support: {new_support}"
    }

    print(f"Event après modification: {new_event_data}")

    with patch("rich.prompt.Prompt.ask", side_effect=[
        str(event.id),
        str(new_support.id),
        new_event_data['attendees'],
        new_event_data['notes'],
    ]):
        modified_event = MainEventController.modify_event()

    if not modified_event:
        print("Échec de la modification de l'événement.")
    else:
        print(f"Modified event: {modified_event}")
        print("Test de modification d'événement réussi.")

    assert modified_event is not None, "L'événement n'a pas été modifié."
    assert modified_event.support_contact.id == new_support.id, "Le support contact n'a pas été modifié correctement."
    assert modified_event.attendees == int(new_event_data["attendees"]), ("Le nombre de participants n'a pas été "
                                                                          "modifié correctement.")
    assert modified_event.notes == new_event_data["notes"], "Les notes n'ont pas été modifiées correctement."


def test_modify_event_by_support(test_track, session_user_support):
    event = generate_event_data(Collaborator=Session.user)
    print(f"\nevent id: {event.id}"
          f"\nevent support contact: {event.support_contact}"
          f"\n client info: {event.client_info}"
          f"\nemail du client: {event.client.id}")
    assert event.support_contact is not None, "Le support contact ne doit pas être None."
    assert event.support_contact.id == event.support_contact.id, ("L'événement n'a pas été assigné au support "
                                                                  "collaborateur correct.")
    fixed_now = datetime.datetime(2024, 7, 15)
    fixed_end = fixed_now + datetime.timedelta(hours=24)
    new_event_data = {
        'contract': event.contract.id,
        'client': event.client.id,
        'client_info': event.client_info,
        'support_contact': event.support_contact,
        'event_date_start': fixed_now,
        'event_date_end': fixed_end,
        'postal_address': "123 rue de la soif",
        'attendees': 78,
        'notes': f"test de modification de mon event depuis mon utilisateur {event.support_contact} "
    }
    print(f"Event après modification: {new_event_data}")

    with patch("rich.prompt.Prompt.ask", side_effect=[
        str(event.id),
        '',
        str(new_event_data['attendees']),
        new_event_data['notes'],
    ]):
        modified_event = MainEventController.modify_event()
    if not modified_event:
        print("Échec de la modification de l'événement.")
    else:
        print(f"Modified event: {modified_event}")
        print("Test de modification d'événement réussi.")

    assert modified_event is not None, "L'événement n'a pas été modifié."
    assert modified_event.attendees == new_event_data['attendees'], ("Le nombre de participants n'a pas été modifié "
                                                                     "correctement.")
    assert modified_event.notes == new_event_data['notes'], "Les notes n'ont pas été modifiées correctement."
    assert modified_event.support_contact.id == session_user_support.id, "Le support contact ne doit pas être modifié."
