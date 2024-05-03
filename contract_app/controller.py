from datetime import datetime
from collaborator_app.model import Collaborator
from services.utils import CollaboratorService, AuthenticateService, CollaboratorValidator
from contract_app.model import Contract
from client_app.model import Client
from contract_app.view import ContractView


class MainContractController:
    client = Client
    @staticmethod
    def display_existing_contract():
        """Fonction qui récupère les champs souhaité pour l'affichage des clients dans les menus"""
        contract = Contract.select()
        ContractView.display_contracts(contract)

    @classmethod
    def create_contract(cls):
        clients = Client.select()
        commercial_collaborators = Collaborator.select().where(Collaborator.role == Collaborator.COMMERCIAL)
        contract_data = ContractView.display_create_contract(clients, commercial_collaborators)
        client = Client.get_or_none(Client.id == contract_data['client'])
        commercial_assignee = Collaborator.get_or_none(Collaborator.id == contract_data['commercial_assignee'])

        is_signed_value = contract_data["is_signed"].lower()
        if is_signed_value not in ['true', 'false']:
            raise ValueError("La valeur de is_signed doit être 'true' ou 'false'")
        is_signed = is_signed_value == 'true'

        new_contract = Contract(
            client=client,
            commercial_assignee=commercial_assignee,
            total_amount=contract_data['total_amount'],
            remaining_amount=contract_data['remaining_amount'],
            created_date=datetime.now(),
            updated_at=datetime.now(),
            is_signed=is_signed
        )
        new_contract.save()
