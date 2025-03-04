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
                                   f"Prenom du commercial: {client.commercial_assignee.last_name} | "
                                   f"ID du collaborateur: {client.commercial_assignee.id} | "
                                   f"Role du collaborateur: {client.commercial_assignee.role}")
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
    def display_create_client_basic_info():
        client_data = {
            "first_name": Prompt.ask("[bold green]Saisissez le prénom du client[/bold green]"),
            "last_name": Prompt.ask("[bold green]Saisissez le nom du client[/bold green]")
        }
        return client_data

    @staticmethod
    def prompt_email():
        return Prompt.ask("[bold green]Veuillez saisir l'email du client[/bold green]")

    @staticmethod
    def prompt_phone_number():
        return Prompt.ask("[bold green]Veuillez saisir le numéro de téléphone du client[/bold green]")

    @staticmethod
    def display_client_table(client):
        table = Table(title="Recap de la création du client", title_style="bold magenta", border_style="bold yellow")
        table.add_column("Champs", style="bold blue", header_style="bold cyan")
        table.add_column("Valeur", style="bold blue", header_style="bold cyan")

        fields = ["first_name", "last_name", "email", "phone_number", "commercial_assignee"]
        for field in fields:
            value = getattr(client, field)
            table.add_row(str(field), str(value), style="bold cyan")

        console.print(table)

    @staticmethod
    def display_error(error_code):
        messages = {
            "INVALID_EMAIL_FORMAT": "Format d'email incorrect. Veuillez saisir un email valide.",
            "EMAIL_ALREADY_EXISTS": "Cet email est déjà utilisé. Veuillez en saisir un autre.",
            "NO_CLIENT_FOUND": "Aucun client trouvé pour ce commercial.",
            "NO_CLIENT_SELECTED": "Aucun client sélectionné.",
            "CLIENT_NOT_EXIST": "Le client spécifié n'existe pas.",
            "CLIENT_HAS_SIGNED_CONTRACT": "Le client que vous souhaité supprimer à un ou plusieurs contrats signés en cours"
        }
        console.print(messages.get(error_code, "Erreur inconnue."), style="bold red")

    @staticmethod
    def display_success(success_code):
        messages = {
            "SUCCESS_CREATE": "Client créé avec succès.",
            "SUCCESS_MODIFY": "Client mis à jour avec succès.",
            "SUCCESS_DELETE": "Client supprimé avec succès.",
        }

        message = messages.get(success_code, "Succès")

        if success_code == "SUCCESS_CREATE":
            console.print(f"✅[bold green] {message}[/bold green]")
        elif success_code == "SUCCESS_MODIFY":
            console.print(f"🔄[bold blue] {message}[/bold blue]")
        elif success_code == "SUCCESS_DELETE":
            console.print(f"✅[bold green] {message}[/bold green]")

    @staticmethod
    def prompt_modified_client_data():
        client_data = {
            "first_name": Prompt.ask("[bold green]Nouveau prénom du client[/bold green]"),
            "last_name": Prompt.ask("[bold green]Nouveau nom du client[/bold green]"),
            "email": Prompt.ask("[bold green]Nouvel email du client (laissez vide pour ne pas changer)[/bold green]"),
            "phone_number": Prompt.ask("[bold green]Nouveau numéro de téléphone du client[/bold green]")
        }
        return client_data

    @staticmethod
    def display_clients_table(clients):
        table = Table(title="Liste de vos clients", title_style="bold magenta", border_style="bold yellow")
        table.add_column("ID", style="bold blue", header_style="bold cyan")
        table.add_column("Prénom", style="bold blue", header_style="bold cyan")
        table.add_column("Nom", style="bold blue", header_style="bold cyan")
        table.add_column("Email", style="bold blue", header_style="bold cyan")
        table.add_column("Numéro de téléphone", style="bold blue", header_style="bold cyan")

        for client in clients:
            table.add_row(str(client.id), client.first_name, client.last_name, client.email, client.phone_number)

        console.print(table)


    @staticmethod
    def prompt_client_id(clients):
        valid_ids = [str(client.id) for client in clients]

        while True:
            client_id = Prompt.ask(
                "[bold green]Veuillez saisir l'ID du client à modifier (ou appuyez sur Entrée pour annuler)[/bold green]"
            ).strip()

            if client_id in valid_ids:
                return int(client_id)  # ✅ Retourne l'ID valide

            console.print("[bold red]ID invalide ou absent.[/bold red]")

            confirmation = Prompt.ask(
                "[bold yellow]Voulez-vous annuler l'opération ? (O/N)[/bold yellow]"
            ).strip().lower()

            if confirmation == "o":
                console.print("[bold cyan]Opération annulée.[/bold cyan]")
                return None

    @staticmethod
    def display_client_details(client):
        table = Table(title="Détails du client", title_style="bold magenta", border_style="bold yellow")
        table.add_column("Champ", style="bold blue", header_style="bold cyan")
        table.add_column("Valeur", style="bold blue", header_style="bold cyan")

        table.add_row("ID", str(client.id))
        table.add_row("Prénom", client.first_name)
        table.add_row("Nom", client.last_name)
        table.add_row("Email", client.email)
        table.add_row("Numéro de téléphone", client.phone_number)
        table.add_row("Créé le", str(client.created_at))
        table.add_row("Modifié le", str(client.updated_at))
        table.add_row("Commercial assigné", client.commercial_assignee.username)

        console.print(table)

    @staticmethod
    def prompt_modified_client_email():
        email = Prompt.ask("[bold green]Nouvel email du client (laissez vide pour ne pas changer)[/bold green]")
        return email

    @staticmethod
    def confirm_action(message):
        """Affiche un message de confirmation et retourne la réponse de l'utilisateur"""
        console.print(f"[bold yellow]{message}[/bold yellow]")
        return input("> ").strip().lower()