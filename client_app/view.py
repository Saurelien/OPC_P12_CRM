from rich.console import Console
from rich.table import Table
from datetime import datetime

console = Console()


class ClientView:

    @staticmethod
    def display_clients(clients):
        table = Table(title="== Liste des clients ==", title_style="bold magenta",
                      title_justify="center",
                      show_header=True,
                      header_style="bold magenta",
                      border_style="bold yellow")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("First Name", style="cyan", justify="center")
        table.add_column("Last Name", style="cyan", justify="center")
        table.add_column("Email", style="cyan", justify="center")
        table.add_column("Phone Number", style="cyan", justify="center")
        table.add_column("Created At", style="cyan", justify="center")
        table.add_column("Updated At", style="cyan", justify="center")
        table.add_column("Commercial Assignee", style="cyan", justify="left")

        for client in clients:
            created_at = client.created_at.strftime("%d-%m-%Y")
            updated_at = client.updated_at.strftime("%d-%m-%Y")
            commercial_assignee = (f"Nom du commercial: {client.commercial_assignee.username}"
                                   f"\nPrenom du commercial: {client.commercial_assignee.last_name}")
            table.add_row(
                str(client.id),
                client.first_name,
                client.last_name,
                client.email,
                client.phone_number,
                created_at,
                updated_at,
                commercial_assignee)

        console.print(table, justify="left")
