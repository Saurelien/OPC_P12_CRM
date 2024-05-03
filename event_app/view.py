from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()


class EventView:

    @staticmethod
    def display_events(events):
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

        for event in events:
            event_date_start = event.event_date_start.strftime("%d-%m-%Y")
            event_date_end = event.event_date_end.strftime("%d-%m-%Y")
            contract = f"{event.contract.id}"
            client = (f"{event.client.first_name} "
                      f"{event.client.last_name}")
            table.add_row(
                str(event.id),
                contract,
                client,
                event.client.email,
                event_date_start,
                event_date_end,
                event.postal_adress,
                event.attendees,
                event.notes
            )
        console.print(table, justify="left")

    @staticmethod
    def get_client_id(assigned_clients):
        console.print("Clients assignés disponibles:")
        table = Table(title="Clients assignés", title_style="bold magenta", border_style="bold yellow")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Nom complet", style="cyan", justify="center")

        for client in assigned_clients:
            table.add_row(str(client.id), f"{client.first_name} {client.last_name}")

        console.print(table)

        client_id = Prompt.ask("Saisissez l'ID du client pour l'événement:")
        return client_id

    @staticmethod
    def get_event_details(client):
        event_data = {
            "name": Prompt.ask("[bold green]"
                               "Nom de l'événement"
                               "[/bold green]"),
            "event_date_start": Prompt.ask("[bold green]"
                                           "Date de début de l'événement (ex. 4 Jun 2023 @ 1PM)"
                                           "[/bold green]"),
            "event_date_end": Prompt.ask("[bold green]"
                                         "Date de fin de l'événement (ex. 5 Jun 2023 @ 2AM)"
                                         "[/bold green]"),
            "support_assignee": Prompt.ask("[bold green]"
                                           "Personne de support assignée"
                                           "[/bold green]"),
            "address": Prompt.ask("[bold green]"
                                  "Adresse de l'événement"
                                  "[/bold green]"),
            "attendees": Prompt.ask("[bold green]"
                                    "Nombre de personnes attendues"
                                    "[/bold green]"),
            "notes": Prompt.ask("[bold green]"
                                "Notes sur l'événement"
                                "[/bold green]")
        }
        return event_data


