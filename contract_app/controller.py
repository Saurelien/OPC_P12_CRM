from services.utils import CollaboratorService, AuthenticateService, CollaboratorValidator
from contract_app.model import Contract
from client_app.model import Client
from contract_app.view import ContractView


class MainContractController:
    client = Client
    @staticmethod
    def display_existing_contract():
        """Fonction qui récupère les champs souhaité pour l'affichage des clients dans les menus"""
        contract = Contract.select(
            Contract.client,
            Contract.total_amount.cast('text'),
            Contract.remaining_amount.cast('text'),
            Contract.created_date,
            Contract.updated_at,
            Contract.is_signed.cast('text'),
            Contract.manager_assignee)
        ContractView.display_contracts(contract)
