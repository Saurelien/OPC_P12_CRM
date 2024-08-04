from unittest.mock import patch

from collaborator_app.model import Collaborator
from contract_app.controller import MainContractController
from contract_app.model import Contract
from services.utils import Session
from utils import generate_contract_data, generate_client, generate_collaborator


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


def test_modify_contract_as_commercial(test_track, session_user_commercial):
    client = generate_client()
    commercial = client.commercial_assignee
    contract = Contract.create(
        total_amount=1000,
        remaining_amount=500,
        is_signed=False,
        commercial_assignee=commercial,
        client=client
    )

    Session.user = commercial

    new_contract_data = {
        'total_amount': '1200',
        'remaining_amount': '600',
        'is_signed': 'oui'
    }

    with patch("rich.prompt.Prompt.ask", side_effect=[
        str(contract.id),
        new_contract_data['total_amount'],
        new_contract_data['remaining_amount'],
        new_contract_data['is_signed'],
        ""
    ]):
        modified_contract = MainContractController.modify_contract()

    assert modified_contract is not None
    assert modified_contract.total_amount == new_contract_data['total_amount']
    assert modified_contract.remaining_amount == new_contract_data['remaining_amount']
    assert modified_contract.is_signed == (new_contract_data['is_signed'].lower() == 'oui')
    assert modified_contract.commercial_assignee == commercial

    print("Test de modification de contrat par un commercial réussi.")


def test_modify_contract_as_gestion(test_track, session_user_gestion):
    new_commercial = generate_collaborator(role=Collaborator.COMMERCIAL)

    contract = generate_contract_data()
    print(f"\nContrat généré: {contract}"
          f"\nCommercial assigné: {contract.commercial_assignee}"
          f"\nClient: {contract.client}")

    # Session.user = new_commercial
    # print(f"Session.user: {Session.user}")

    updated_data = {
        'total_amount': '1500',
        'remaining_amount': '800',
        'is_signed': 'oui',
        'commercial_assignee': new_commercial
    }
    print(f"Contrat mis à jour: {updated_data}"
          f"\ncommercial_assignee: {new_commercial}"
          f"\ncommercial assignée id: {new_commercial.id}")

    with patch("rich.prompt.Prompt.ask", side_effect=[
        str(contract.id),
        updated_data['total_amount'],
        updated_data['remaining_amount'],
        updated_data['is_signed'],
        str(new_commercial.id)
    ]):
        try:
            updated_contract = MainContractController.modify_contract()
        except Exception as e:
            print(f"Erreur rencontrée: {e}")
            raise

    assert updated_contract is not None
    assert updated_contract.total_amount == updated_data['total_amount']
    assert updated_contract.remaining_amount == updated_data['remaining_amount']
    assert updated_contract.is_signed == (updated_data['is_signed'].lower() == 'oui')

    new_assignee = Collaborator.get_or_none(Collaborator.id == updated_data['commercial_assignee'])
    assert updated_contract.commercial_assignee == new_assignee

    print("Test de modification de contrat avec changement de commercial assigné réussi.")
