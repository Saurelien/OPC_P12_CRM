from unittest.mock import patch, ANY
from client_app.controller import MainClientController
from client_app.model import Client
from services.utils import Session
from rich.console import Console
from client_app.view import ClientView


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


def test_display_create_client_basic_info():
    client_data = {
        'first_name': "Jean1",
        'last_name': "Claude"
    }

    with patch("rich.prompt.Prompt.ask", side_effect=list(client_data.values())):
        result = ClientView.display_create_client_basic_info()

    assert result["first_name"] == client_data["first_name"]
    assert result["last_name"] == client_data["last_name"]


def test_display_error():
    error_code = "INVALID_EMAIL_FORMAT"

    with patch.object(Console, "print") as mock_print:
        ClientView.display_error(error_code)

        mock_print.assert_called_with("Format d'email incorrect. Veuillez saisir un email valide.", style='bold red')