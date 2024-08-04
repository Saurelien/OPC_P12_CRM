from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()


class EventView:

    @staticmethod
    def display_events(events):
        table = Table(title="== Liste des événements ==", title_style="bold magenta",
                      title_justify="center",
                      show_header=True,
                      header_style="bold magenta",
                      border_style="bold yellow")
        table.add_column("ID Event", style="cyan", justify="center")
        table.add_column("ID Contrat", style="cyan", justify="center")
        table.add_column("ID Client", style="cyan", justify="center")
        table.add_column("information du client", style="cyan", justify="center")
        table.add_column("Collaborateur de support du client", style="cyan", justify="center")
        table.add_column("Date de début", style="cyan", justify="center")
        table.add_column("Date de fin", style="cyan", justify="center")
        table.add_column("Adresse postale", style="cyan", justify="center")
        table.add_column("Nombre d'invités", style="cyan", justify="center")
        table.add_column("Notes", style="cyan", justify="center")

        for event in events:
            event_date_start = event.event_date_start.strftime("%d-%m-%Y")
            event_date_end = event.event_date_end.strftime("%d-%m-%Y")
            contract = str(event.contract.id)
            support_contact = f"{event.support_contact.id}, {event.support_contact.username}"
            client = f"{event.client_id}"
            client_info = f"{event.client_info}"
            table.add_row(
                str(event.id),
                contract,
                client,
                client_info,
                support_contact,
                event_date_start,
                event_date_end,
                event.postal_address,
                str(event.attendees),
                event.notes
            )
        console.print(table, justify="left")

    @staticmethod
    def get_contract_id(clients_with_signed_contracts):
        table = Table(title="Clients avec contrats signés", title_style="bold magenta", border_style="bold yellow",
                      header_style="purple")
        table.add_column("ID", style="bold cyan", justify="center")
        table.add_column("Nom & Prénom du client", style="bold cyan", justify="center")
        table.add_column("Email du client", style="bold cyan", justify="center")
        table.add_column("ID", style="bold cyan", justify="center")

        for contract in clients_with_signed_contracts:
            client = contract.client
            table.add_row(f"[bold green]ID du contrat:[/bold green] {str(contract.id)}",
                          f"{client.first_name} - {client.last_name}",
                          client.email,
                          f"[bold green]ID du client:[/bold green] {str(client.id)}")

        console.print(table)

        contract_id = Prompt.ask("[bold green]Saisissez l'ID du contrat pour l'événement[/bold green]")
        return contract_id

    @staticmethod
    def get_support_contact_id(support_collaborators):

        console.print("Collaborateurs de support disponibles:", style="bold blue")
        table = Table(title="Collaborateurs de support",
                      title_style="bold magenta",
                      border_style="bold yellow",
                      header_style="bold purple")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Username", style="cyan", justify="center")
        table.add_column("Prénom", style="cyan", justify="center")
        table.add_column("Nom", style="cyan", justify="center")

        for collaborator in support_collaborators:
            table.add_row(str(collaborator.id), collaborator.username, collaborator.first_name, collaborator.last_name)

        console.print(table)

        support_contact_id = Prompt.ask("[bold green]"
                                        "Saisissez l'ID du collaborateur de support pour l'événement"
                                        "[/bold green]")
        return support_contact_id

    @staticmethod
    def get_event_details():
        event_data = {
            "name": Prompt.ask("[bold green]"
                               "Nom de l'événement"
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

    @staticmethod
    def display_event_detail(event, name):
        table = Table(title="Détails de l'événement",
                      show_lines=True,
                      title_style="bold magenta",
                      show_header=False,
                      border_style="bold yellow")
        client_info = ""
        if event.client:
            client_info = (f"Prénom: {event.client.first_name}\n"
                           f"Nom: {event.client.last_name}\n"
                           f"Email: {event.client.email}\n"
                           f"Téléphone: {event.client.phone_number}")
        table.add_column("Champ", style="cyan", justify="center")
        table.add_column("Valeur", style="cyan", justify="center")

        table.add_row("Nom de l'évènement", name, style="cyan")
        table.add_row("ID de l'événement", str(event.id), style="cyan")
        table.add_row("ID du contrat", str(event.contract_id), style="cyan")
        table.add_row("ID du client", str(event.client_id), style="cyan")
        table.add_row("Info client", client_info, style="cyan")
        table.add_row("contact de support", str(event.support_contact), style="cyan")
        table.add_row("Date de début", str(event.event_date_start), style="cyan")
        table.add_row("Date de fin", str(event.event_date_end), style="cyan")
        table.add_row("Adresse", event.postal_address, style="cyan")
        table.add_row("Nombre d'invités", str(event.attendees), style="cyan")
        table.add_row("Notes", event.notes, style="cyan")

        console.print(table)

    @staticmethod
    def get_event_modification_details(event, support_collaborators):
        console.print(f"Modification de l'événement (ID: {event.id}) :")
        event_data = {}

        console.print("Collaborateurs de support disponibles:", style="bold blue")
        table = Table(title="Collaborateurs de support",
                      title_style="bold magenta",
                      border_style="bold yellow",
                      header_style="bold purple")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Username", style="cyan", justify="center")
        table.add_column("Prénom", style="cyan", justify="center")
        table.add_column("Nom", style="cyan", justify="center")

        for collaborator in support_collaborators:
            table.add_row(str(collaborator.id), collaborator.username, collaborator.first_name, collaborator.last_name)

        console.print(table)

        while True:
            new_support_contact_id = Prompt.ask(
                "[bold green]"
                "Nouvel ID du collaborateur de support assigné (laissez vide pour ne pas modifier)"
                "[/bold green]", default=str(event.support_contact.id))
            if not new_support_contact_id:
                break
            if new_support_contact_id.isdigit() and any(
                    collaborator.id == int(new_support_contact_id) for collaborator in support_collaborators):
                event_data["support_contact"] = int(new_support_contact_id)
                break
            else:
                EventView.display_error("INVALID_SUPPORT_CONTACT_ID")

        event_data["attendees"] = Prompt.ask("[bold green]"
                                             "Nouveau nombre d'invités"
                                             "[/bold green]", default=str(event.attendees))
        event_data["notes"] = Prompt.ask("[bold green]"
                                         "Nouvelles notes sur l'événement"
                                         "[/bold green]", default=event.notes)
        return event_data

    @staticmethod
    def get_event_id_to_modify(events):
        EventView.display_events(events)
        event_id = Prompt.ask("[bold green]"
                              "Saisissez l'ID de l'événement à modifier"
                              "[/bold green]")
        return event_id

    @staticmethod
    def display_error(error_code):
        messages = {
            "AUTH_ERROR": "Accès refusé. Vous devez être authentifié pour créer un événement.",
            "COLLABORATOR_NOT_FOUND": "Accès refusé. Collaborateur non trouvé.",
            "NO_SIGNED_CONTRACTS": "Aucun contrat signé trouvé pour ce commercial.",
            "INVALID_CONTRACT_ID": "ID de contrat invalide. Veuillez réessayer.",
            "INVALID_SUPPORT_CONTACT_ID": "Ce choix n'est pas valide ou collaborateur de support exigé. Veuillez "
                                          "réessayer.",
            "NO_EVENTS_FOUND": "Aucun événement trouvé pour ce gestionnaire/support.",
            "INVALID_EVENT_ID": "ID d'événement invalide. Veuillez réessayer."
        }
        console.print(messages.get(error_code, "Erreur inconnue."), style="bold red")
