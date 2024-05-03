from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()


class ContractView:

    @staticmethod
    def display_contracts(contracts):
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
        table.add_column("client contact", style="cyan", justify="center")

        for contract in contracts:
            created_date = contract.created_date.strftime("%d-%m-%Y")
            updated_at = contract.updated_at.strftime("%d-%m-%Y")
            client = (f"{contract.client.first_name} "
                      f"{contract.client.last_name}")
            manager = (f"{contract.commercial_assignee.first_name} "
                       f"{contract.commercial_assignee.last_name}")
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
    def display_create_contract(clients, commercial_collaborators):
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

        commercial_table = Table(title="Informations Collaborateurs Commerciaux",
                                 title_style="bold magenta",
                                 show_header=True, header_style="bold magenta",
                                 border_style="bold yellow")
        commercial_table.add_column("ID", style="cyan", justify="center")
        commercial_table.add_column("Username", style="cyan", justify="center")
        commercial_table.add_column("Prenom", style="cyan", justify="center")
        commercial_table.add_column("Nom", style="cyan", justify="center")

        for collaborator in commercial_collaborators:
            commercial_table.add_row(str(collaborator.id),
                                     collaborator.username,
                                     collaborator.first_name,
                                     collaborator.last_name)

        console.print(client_table)
        console.print(commercial_table)

        contract_data = {
            "client": Prompt.ask("[bold green]"
                                 "Sélectionnez l'ID du client pour le contrat"
                                 "[/bold green]"),
            "commercial_assignee": Prompt.ask("[bold green]"
                                              "Sélectionnez l'ID du collaborateur commercial pour le contrat"
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

