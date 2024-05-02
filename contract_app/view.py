from rich.console import Console
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
            client = (f"{contract.client.first_name}"
                      f"{contract.client.last_name}")
            manager = (f"{contract.manager_assignee.first_name}"
                       f"{contract.manager_assignee.last_name}")
            table.add_row(
                str(contract.id),
                client,
                contract.total_amount,
                contract.remaining_amount,
                created_date,
                updated_at,
                contract.is_signed,
                manager
            )
        console.print(table, justify="left")

