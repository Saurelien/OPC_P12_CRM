from unittest.mock import patch
from client_app.controller import MainClientController
from client_app.model import Client
from services.utils import Session
from utils import generate_client


def test_create_client(test_track, session_user_commercial):
    client_data = {
        'first_name': "Jean1",
        'last_name': "Claude",
        'email': "jean@claude1.com",
        'phone_number': "0102010201",
        'commercial_assignee': Session.user
    }
    print(f"Base de données utilisée pour le client: {Client._meta.database.database}")
    with patch("rich.prompt.Prompt.ask", side_effect=list(client_data.values())):
        create_client = MainClientController.create_client()

    assert create_client.first_name == client_data['first_name']
    assert create_client.last_name == client_data['last_name']
    assert create_client.email == client_data['email']
    assert create_client.phone_number == client_data['phone_number']
    assert create_client.commercial_assignee == Session.user

    print("Client créé et vérifié avec succès.")


def test_modify_client(test_track, session_user_commercial):
    client = generate_client(collaborator=Session.user)
    print(f"\nClient initial: {client.first_name} {client.last_name}, \nCommercial: {client.commercial_assignee.username}")
    db_client = Client.get(Client.id == client.id)
    assert db_client is not None, "Le client n'existe pas dans la base de données avant modification"
    new_client_data = {
        'client': client.id,
        'first_name': "Jean",
        'last_name': "Claude123",
        'email': "jean_claude@aa.com",
        'phone_number': "0102010201",
        'commercial_assignee': Session.user.id
    }
    with patch("rich.prompt.Prompt.ask", side_effect=list(new_client_data.values())):
        modified_client = MainClientController.modify_client()

    assert modified_client is not None, "La modification du client a échoué, aucun client retourné"

    modified_client = Client.get_by_id(modified_client.id)
    assert modified_client.first_name == "Jean"
    assert modified_client.last_name == new_client_data['last_name']
    assert modified_client.email == new_client_data['email']
    assert modified_client.phone_number == new_client_data['phone_number']
    assert modified_client.commercial_assignee.id == Session.user.id

    print(f"\nClient modifié first_name: {modified_client.first_name} last_name: {modified_client.last_name},"
          f"\nCommercial: {modified_client.commercial_assignee.username}"
          f"\nEmail du cleint modifier: {modified_client.email}")
    print("Client modifié et vérifié avec succès.")


