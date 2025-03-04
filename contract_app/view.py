from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()


class ContractView:

    @staticmethod
    def display_contracts(contracts):
        console.clear_live()
        table = Table(title="== Liste des contrats ==", title_style="bold magenta",
                      title_justify="center",
                      show_header=True,
                      header_style="bold magenta",
                      border_style="bold yellow")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("client", style="cyan", justify="center")
        table.add_column("total_amount", style="cyan", justify="center")
        table.add_column("remaining_amount", style="cyan", justify="center")
        table.add_column("created_date", style="cyan", justify="center")
        table.add_column("updated_at", style="cyan", justify="center")
        table.add_column("is_signed", style="cyan", justify="center")
        table.add_column("commercial contact", style="cyan", justify="center")

        for contract in contracts:
            created_date = contract.created_at.strftime("%d-%m-%Y")
            updated_at = contract.updated_at.strftime("%d-%m-%Y")
            client = (f"{contract.client.first_name} "
                      f"{contract.client.last_name}")
            manager = (f"{contract.commercial_assignee.first_name} {contract.commercial_assignee.last_name}"
                       if contract.commercial_assignee else "Non assigné")
            table.add_row(
                str(contract.id),
                client,
                str(contract.total_amount),
                str(contract.remaining_amount),
                created_date,
                updated_at,
                str(contract.is_signed),
                manager
            )
        console.print(table, justify="left")

    @staticmethod
    def display_create_contract(clients):
        client_table = Table(title="Informations Clients",
                             title_style="bold magenta",
                             show_header=True,
                             header_style="bold magenta",
                             border_style="bold yellow")
        client_table.add_column("ID", style="cyan", justify="center")
        client_table.add_column("Prénom", style="cyan", justify="center")
        client_table.add_column("Nom", style="cyan", justify="center")

        for client in clients:
            client_table.add_row(str(client.id), client.first_name, client.last_name)

        console.print(client_table)

        contract_data = {
            "client": Prompt.ask("[bold green]"
                                 "Sélectionnez l'ID du client pour le contrat"
                                 "[/bold green]"),
            "total_amount": Prompt.ask("[bold green]"
                                       "Entrez le montant total du contrat"
                                       "[/bold green]"),
            "remaining_amount": Prompt.ask("[bold green]"
                                           "Entrez le montant restant du contrat"
                                           "[/bold green]"),
            "is_signed": Prompt.ask("[bold green]"
                                    "Le contrat est-il signé ? (True/False)"
                                    "[/bold green]")
        }

        return contract_data

    @staticmethod
    def display_contract_selection(contracts):
        console.print("Liste des contrats existants:", style="bold purple")
        table = Table(title="Contrats", title_style="bold magenta", border_style="bold yellow")
        table.add_column("ID du contrat", style="cyan", justify="center")
        table.add_column("Client", style="cyan", justify="center")
        table.add_column("Montant", style="cyan", justify="center")
        table.add_column("Signé", style="cyan", justify="center")
        table.add_column("Commercial", style="cyan", justify="center")

        for contract in contracts:
            signed = "Oui" if contract.is_signed else "Non"
            commercial = f"{contract.commercial_assignee.first_name} {contract.commercial_assignee.last_name}"\
                if contract.commercial_assignee else "Non assigné"
            table.add_row(
                str(contract.id),
                f"{contract.client.first_name} {contract.client.last_name}",
                f"{contract.total_amount}",
                signed,
                commercial
            )
        console.print(table)

        contract_id = Prompt.ask("[bold green]"
                                 "Saisissez l'ID du contrat à modifier"
                                 "[/bold green]")
        if contract_id:
            return int(contract_id)

    @staticmethod
    def get_contract_modification_details(contract, collaborators):
        console.print(f"Modification du contrat (ID: {contract.id})")
        contract_data = {
            "total_amount": Prompt.ask("Nouveau montant total du contrat", default=str(contract.total_amount)),
            "remaining_amount": Prompt.ask("Nouveau montant restant du contrat", default=str(contract.remaining_amount))
        }

        if not contract.is_signed:
            is_signed_input = Prompt.ask("Le contrat a-t-il été signé ? (Oui/Non)", default="Non")
            contract_data["is_signed"] = True if is_signed_input.lower() == "oui" else False

        console.print("Liste des collaborateurs commerciaux disponibles pour assignation")
        table = Table(title="Collaborateurs commerciaux", title_style="bold magenta", border_style="bold yellow")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Nom d'utilisateur", style="cyan", justify="center")

        for collaborator in collaborators:
            table.add_row(str(collaborator.id), collaborator.username)

        console.print(table)

        selected_id = Prompt.ask(
            "[bold green]"
            "Saisissez l'ID du collaborateur commercial pour la réaffectation (laisser vide pour ne pas changer)"
            "[/bold green]")
        if selected_id:
            contract_data["commercial_assignee"] = int(selected_id)
        return contract_data

    @staticmethod
    def display_contract_modification_summary(contract_data):
        console.print("Récapitulatif des modifications:")
        table = Table(title="Champs modifiés", title_style="bold magenta", border_style="bold yellow")
        table.add_column("Champ", style="cyan", justify="center")
        table.add_column("Nouvelle valeur", style="cyan", justify="center")

        for field, new_value in contract_data.items():
            table.add_row(field, str(new_value))

        console.print(table)

    @staticmethod
    def display_error(error_code, collaborator=None):
        messages = {
            "NO_CONTRACTS_FOUND": (
                f"Aucun contrat trouvé pour le commercial {collaborator.id}, {collaborator.username}."
                if collaborator else "Aucun contrat trouvé."
            ),
            "NO_CONTRACTS_NON_SIGNED_FOUND": "Aucun contrat non signé trouvé.",
            "NO_CONTRACTS_REMAINING_AMOUNT_FOUND": "Aucun contrat avec un montant restant trouvé.",
            "NO_CONTRACT_SELECTED": "Veuillez saisir un ID de contrat à modifier"
        }
        console.print(messages.get(error_code, "Erreur inconnue."), style="bold red")

    @staticmethod
    def display_non_signed_contracts(contracts):
        if not contracts.exists():
            console.print("Aucun contrat non signé trouvé.", style="bold red")
            return

        table = Table(title="Contrats non signés", title_style="bold magenta", border_style="bold yellow")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("ID Client", style="cyan", justify="center")
        table.add_column("Montant total", style="cyan", justify="center")
        table.add_column("Montant restant", style="cyan", justify="center")
        table.add_column("Est signé ?", style="cyan", justify="center")

        for contract in contracts:
            client_id = contract.client.id if contract.client else "N/A"
            table.add_row(
                str(contract.id),
                str(client_id),
                str(contract.total_amount),
                str(contract.remaining_amount),
                "Oui" if contract.is_signed else "Non"
            )

        console.print(table)

    @staticmethod
    def display_contracts_with_remaining_amount(contracts):
        if not contracts.exists():
            console.print("Aucun contrat avec un montant restant différent de zéro trouvé.", style="bold red")
            return

        table = Table(title="Contrats avec un montant restant", title_style="bold magenta", border_style="bold yellow")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("ID Client", style="cyan", justify="center")
        table.add_column("Montant total", style="cyan", justify="center")
        table.add_column("Montant restant", style="cyan", justify="center")
        table.add_column("Est signé ?", style="cyan", justify="center")

        for contract in contracts:
            client_id = contract.client.id if contract.client else "N/A"
            table.add_row(
                str(contract.id),
                str(client_id),
                str(contract.total_amount),
                str(contract.remaining_amount),
                "Oui" if contract.is_signed else "Non"
            )

        console.print(table)
