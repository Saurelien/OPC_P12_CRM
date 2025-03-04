from datetime import datetime
from collaborator_app.model import Collaborator
from services.utils import CollaboratorService, AuthenticateService, Session
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
        if not Session.is_gestion():
            return
        clients = Client.select()
        contract_data = ContractView.display_create_contract(clients)
        client_id = contract_data['client']
        client = Client.get_or_none(Client.id == client_id)
        commercial_collaborator_id = None
        if client:
            commercial_collaborator_id = client.commercial_assignee_id

        commercial_collaborator = CollaboratorService.get_collaborator_by_id(commercial_collaborator_id)

        is_signed_value = contract_data["is_signed"].lower()
        if is_signed_value not in ['true', 'false']:
            raise ValueError("La valeur de is_signed doit être 'true' ou 'false'")
        is_signed = is_signed_value == 'true'

        new_contract = Contract(
            client=client,
            commercial_assignee=commercial_collaborator,
            total_amount=contract_data['total_amount'],
            remaining_amount=contract_data['remaining_amount'],
            created_date=datetime.now(),
            updated_at=datetime.now(),
            is_signed=is_signed
        )
        new_contract.save()
        return new_contract

    @classmethod
    def modify_contract(cls):
        user = Session.get_current_user()
        print(f"User récupéré : {user}")

        if user is None or (not Session.is_commercial() and not Session.is_gestion()):
            ContractView.display_error("UNAUTHORIZED_ACCESS")
            return None

        if Session.is_commercial():
            contracts = Contract.select().where(Contract.commercial_assignee == user)
        else:
            contracts = Contract.select()

        if not contracts.exists():
            ContractView.display_error("NO_CONTRACTS_FOUND", user)
            return None

        contract = None
        while not contract:
            contract_id = ContractView.display_contract_selection(contracts)

            if not contract_id:
                ContractView.display_error("NO_CONTRACT_SELECTED")
                continue

            contract = Contract.get_or_none(Contract.id == contract_id)

            if not contract:
                ContractView.display_error("CONTRACT_NOT_FOUND")
                continue

        collaborators = Collaborator.select().where(Collaborator.role == Collaborator.COMMERCIAL)
        contract_data = ContractView.get_contract_modification_details(contract, collaborators)

        if not contract_data:
            ContractView.display_error("INVALID_CONTRACT_DATA")
            return None

        if "total_amount" in contract_data:
            contract.total_amount = contract_data["total_amount"]
        if "remaining_amount" in contract_data:
            contract.remaining_amount = contract_data["remaining_amount"]
        if "is_signed" in contract_data:
            contract.is_signed = contract_data["is_signed"]
        if "commercial_assignee" in contract_data:
            new_assignee_id = contract_data["commercial_assignee"]
            new_assignee = Collaborator.get_or_none(Collaborator.id == new_assignee_id)

            if new_assignee and new_assignee.role == Collaborator.COMMERCIAL:
                contract.commercial_assignee = new_assignee
            else:
                ContractView.display_error("INVALID_COMMERCIAL_ASSIGNEE")
                return None

        contract.updated_at = datetime.now()
        contract.save()

        ContractView.display_contract_modification_summary(contract_data)

    @classmethod
    def display_contracts(cls):
        if not Session.is_commercial():
            return
        print(f"{Session.get_current_user().role}")
        authenticated_collaborator = Session.get_current_user()
        if authenticated_collaborator:
            contracts_non_signed = Contract.select().where(
                (Contract.commercial_assignee == authenticated_collaborator) &
                (Contract.is_signed is False)
            )
            contracts_with_remaining_amount = Contract.select().where(
                (Contract.commercial_assignee == authenticated_collaborator) &
                (Contract.remaining_amount > 0)
            )

            if not contracts_non_signed.exists() and not contracts_with_remaining_amount.exists():
                ContractView.display_error("NO_CONTRACTS_FOUND", authenticated_collaborator)
                return

            if contracts_non_signed.exists():
                ContractView.display_non_signed_contracts(contracts_non_signed)
            if contracts_with_remaining_amount.exists():
                ContractView.display_contracts_with_remaining_amount(contracts_with_remaining_amount)
