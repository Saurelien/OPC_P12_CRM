from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from datetime import datetime

console = Console()


class ClientView:
    @staticmethod
    def get_choice():
        return Prompt.ask("[bold green]Quel est votre choix ? [/bold green]")

    @staticmethod
    def display_clients(clients):
        table = Table(title="== Liste des clients ==", title_style="bold magenta",
                      title_justify="center",
                      show_header=True,
                      caption_justify="center",
                      header_style="bold magenta",
                      border_style="bold yellow")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("First Name", style="cyan", justify="center")
        table.add_column("Last Name", style="cyan", justify="center")
        table.add_column("Email", style="cyan", justify="center")
        table.add_column("Phone Number", style="cyan", justify="center")
        table.add_column("Created At", style="cyan", justify="center")
        table.add_column("Updated At", style="cyan", justify="center")
        table.add_column("Commercial Assignee", style="cyan", justify="center", no_wrap=True)

        for client in clients:
            created_at = client.created_at.strftime("%d-%m-%Y")
            updated_at = client.updated_at.strftime("%d-%m-%Y")
            commercial_assignee = (f"Nom du commercial: {client.commercial_assignee.username} | "
                                   f"Prenom du commercial: {client.commercial_assignee.last_name}")
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

    @staticmethod
    def display_create_client():
        collaborator_data = {"first_name": Prompt.ask("[bold green]"
                                                      "Saisissez le prénom du collaborateur"
                                                      "[/bold green]"),
                             "last_name": Prompt.ask("[bold green]"
                                                     "Saisissez le nom du collaborateur: "
                                                     "[/bold green]"),
                             "email": Prompt.ask("[bold green]"
                                                 "Veuillez saisir l'email du client"
                                                 "[/bold green]"),
                             "phone_number": Prompt.ask("[bold green]"
                                                        "Veuillez saisir le numéro de téléphone du client"
                                                        "[/bold green]")}
        return collaborator_data


def display_client_table(client_data):
    table = Table(title="Recap de la création du client", title_style="bold magenta", border_style="bold yellow")
    table.add_column("Champs", style="bold blue", header_style="bold cyan")
    table.add_column("Valeur", style="bold blue", header_style="bold cyan")

    for field, value in client_data.items():
        table.add_row(str(field), str(value), style="bold cyan")

    console.print(table)
