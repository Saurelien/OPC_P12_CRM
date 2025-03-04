from collaborator_app.model import Collaborator
from contract_app.model import Contract
from services.utils import Session
from utils import generate_contract_data, generate_client, generate_collaborator
from unittest.mock import patch
from contract_app.controller import MainContractController

def test_create_contract_as_gestion(test_track, session_user_gestion):
    client = generate_client()
    commercial_contract_assignee = client.commercial_assignee
    print(f"Client généré:{client.first_name},commercial assigné a la création du client: {client.commercial_assignee}")

    contract_data = {
        'total_amount': '1000',
        'remaining_amount': '500',
        'is_signed': 'true',
        'commercial_assignee': commercial_contract_assignee,
        'client': client
    }
    print("Contract Data:", contract_data)
    side_effect = [contract_data['client'],
                   contract_data['total_amount'],
                   contract_data['remaining_amount'],
                   contract_data['is_signed']]

    with patch("rich.prompt.Prompt.ask", side_effect=side_effect):
        created_contract = MainContractController.create_contract()

    if created_contract is None:
        print("Erreur : Le contrat créé est None")
    else:
        print(f"Contrat créé avec succès: {created_contract.id}")

    assert created_contract is not None
    assert created_contract.client == client
    assert created_contract.total_amount == contract_data['total_amount']
    assert created_contract.remaining_amount == contract_data['remaining_amount']
    assert created_contract.is_signed == (contract_data['is_signed'].lower() == 'true')
    assert created_contract.commercial_assignee == commercial_contract_assignee

    print("Test de création de contrat réussi.")


def test_create_signed_contract(test_track, session_user_gestion):
    client = generate_client()
    commercial_contract_assignee = client.commercial_assignee
    print(f"Client généré: {client.first_name}, commercial assigné a la création du client: {client.commercial_assignee}")

    contract_data_signed = {
        'total_amount': '1000',
        'remaining_amount': '500',
        'is_signed': 'true',
        'commercial_assignee': commercial_contract_assignee,
        'client': client
    }

    print("Contract Data (Signé):", contract_data_signed)
    side_effect_signed = [contract_data_signed['client'],
                          contract_data_signed['total_amount'],
                          contract_data_signed['remaining_amount'],
                          contract_data_signed['is_signed']]

    with patch("rich.prompt.Prompt.ask", side_effect=side_effect_signed):
        created_contract_signed = MainContractController.create_contract()

    if created_contract_signed is None:
        print("Erreur : Le contrat signé créé est None")
    else:
        print(f"Contrat signé créé avec succès: {created_contract_signed.id}")

    assert created_contract_signed is not None
    assert created_contract_signed.client == client
    assert created_contract_signed.total_amount == contract_data_signed['total_amount']
    assert created_contract_signed.remaining_amount == contract_data_signed['remaining_amount']
    assert created_contract_signed.is_signed == (contract_data_signed['is_signed'].lower() == 'true')
    assert created_contract_signed.commercial_assignee == commercial_contract_assignee

    print("Test de création de contrat signé réussi.")

def test_create_unsigned_contract(test_track, session_user_gestion):
    client = generate_client()
    commercial_contract_assignee = client.commercial_assignee
    print(f"Client généré: {client.first_name}, commercial assigné a la création du client: {client.commercial_assignee}")

    contract_data_unsigned = {
        'total_amount': '2000',
        'remaining_amount': '1000',
        'is_signed': 'false',
        'commercial_assignee': commercial_contract_assignee,
        'client': client
    }

    print("Contract Data (Non Signé):", contract_data_unsigned)
    side_effect_unsigned = [contract_data_unsigned['client'],
                            contract_data_unsigned['total_amount'],
                            contract_data_unsigned['remaining_amount'],
                            contract_data_unsigned['is_signed']]

    with patch("rich.prompt.Prompt.ask", side_effect=side_effect_unsigned):
        created_contract_unsigned = MainContractController.create_contract()

    if created_contract_unsigned is None:
        print("Erreur : Le contrat non signé créé est None")
    else:
        print(f"Contrat non signé créé avec succès: {created_contract_unsigned.id}")

    assert created_contract_unsigned is not None
    assert created_contract_unsigned.client == client
    assert created_contract_unsigned.total_amount == contract_data_unsigned['total_amount']
    assert created_contract_unsigned.remaining_amount == contract_data_unsigned['remaining_amount']
    assert created_contract_unsigned.is_signed == (contract_data_unsigned['is_signed'] == 'true')
    assert created_contract_unsigned.commercial_assignee == commercial_contract_assignee

    print("Test de création de contrat non signé réussi.")