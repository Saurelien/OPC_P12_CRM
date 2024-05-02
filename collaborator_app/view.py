from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import getpass

console = Console()


class MenuView:
    @staticmethod
    def display_fail_auth():
        console.print("Authentification échoué, veuillez réessayé", style="bold red")

    @staticmethod
    def get_choice():
        return Prompt.ask("[bold green]Quel est votre choix ? [/bold green]")

    @staticmethod
    def display_closing_message():
        console.print("Fermeture du programme.", style="bold blue")

    @staticmethod
    def display_menu():
        table = Table(show_header=True, header_style="bold magenta", title_justify="center", border_style="bold yellow")
        table.add_column("Choix", justify="center", style="bold cyan")
        table.add_column("Description", justify="center", style="bold cyan")
        table.add_row("1", "Se connecter")
        table.add_row("Q", "Quitter")
        console.print(table)

    @staticmethod
    def display_collaborators(collaborators):
        table = Table(title="== Liste des collaborateurs ==", title_style="bold magenta",
                      title_justify="center",
                      show_header=True,
                      header_style="bold magenta",
                      border_style="bold yellow")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Username", style="cyan", justify="center")
        table.add_column("First Name", style="cyan", justify="center")
        table.add_column("Last Name", style="cyan", justify="center")
        table.add_column("Role", style="cyan", justify="center")

        for collaborator in collaborators:
            table.add_row(
                str(collaborator.id),
                collaborator.username,
                collaborator.first_name,
                collaborator.last_name,
                collaborator.role
            )

        console.print(table, justify="left")

    @staticmethod
    def display_login_menu():
        console.print("== Connexion ==", style="bold cyan")
        username = input("Nom d'utilisateur : ")
        password = getpass.getpass("Mot de passe : ")
        return username, password

    @staticmethod
    def display_gestion_menu():
        console.bell()
        table = Table(title="== Menu Gestion ==",
                      show_header=True,
                      header_style="bold blue",
                      border_style="bold yellow",
                      title_justify="center",
                      title_style="bold magenta")
        table.add_column("choix", style="bold cyan", justify="center")
        table.add_column("description", style="bold cyan", justify="left")
        rows = [
            ("1", "Créer un nouveau collaborateur"),
            ("2", "Rechercher un client"),
            ("3", "Rechercher un contrat"),
            ("4", "Rechercher un évènement"),
            ("5", "Créer ou modifier un contrat"),
            ("6", "Afficher tous les évènements"),
            ("7", "Assigner un support a un évènement"),
            ("8", "Modifier un collaborateur"),
            ("9", "Afficher les collaborateurs"),
            ("10", "Supprimer un collaborateur"),
            ("Q", "Se déconnecter"),
        ]
        for choice, description in rows:
            table.add_row(choice, description)
        console.print(table)

    @staticmethod
    def display_commercial_menu():
        table = Table(show_header=True, header_style="bold magenta", border_style="bold yellow")
        table.add_column("== Menu Commercial ==", style="bold cyan", justify="center")
        table.add_column("== Description ==", style="bold cyan", justify="center")
        table.add_row("1. Créer une fiche client")
        table.add_row("2. Rechercher un client")
        table.add_row("3. Rechercher un contrat")
        table.add_row("4. Rechercher un évènement")
        table.add_row("5. Mettre à jour un client")
        table.add_row("6. Mettre à jour un contrat")
        table.add_row("7. Afficher les contrats non signé/impayé")
        table.add_row("8. Créer un évènement pour un client ayant souscrit a un contrat")
        table.add_row("9" "Afficher les collaborateurs", "affiche les collaborateurs")
        table.add_row("Q. Se déconnecter")
        console.print(table)

    @staticmethod
    def display_support_menu():
        table = Table(show_header=True, header_style="bold magenta", border_style="bold yellow")
        table.add_column("== Menu Support ==", style="bold cyan", justify="center")
        table.add_column("== Description ==", style="bold cyan", justify="center")
        table.add_row("1. Rechercher un client", "Affiche les clients")
        table.add_row("2. Rechercher un contrat")
        table.add_row("3. Rechercher un évènement")
        table.add_row("4", "Afficher les collaborateurs"),
        table.add_row("Q. Se déconnecter")
        console.print(table)

    @staticmethod
    def display_create_collaborator_menu():
        collaborator_data = {"username": Prompt.ask("[bold green]"
                                                    "Saisissez un nom utilisateur pour le collaborateur"
                                                    "[/bold green]"),
                             "password": Prompt.ask("[bold green]"
                                                    "Saisissez un mot de passe pour le collaborateur"
                                                    "[/bold green]", password=True),
                             "first_name": Prompt.ask("[bold green]"
                                                      "Saisissez le prénom du collaborateur"
                                                      "[/bold green]"),
                             "last_name": Prompt.ask("[bold green]"
                                                     "Saisissez le nom du collaborateur: "
                                                     "[/bold green]"),
                             "role": Prompt.ask("[bold green]"
                                                "Saisissez le code du rôle du collaborateur ("
                                                "C pour Commercial, "
                                                "G pour Gestion, "
                                                "S pour Support"
                                                ")"
                                                "[/bold green]").upper()}
        return collaborator_data

    """Modification d'un collaborateur"""

    @staticmethod
    def display_modify_collaborator_menu():
        table = Table(title="Menu Modification Collaborateur", title_style="bold magenta")
        table.add_column("Choix", style="cyan", justify="center")
        table.add_column("Description", style="cyan", justify="center")
        table.add_row("1", "Rechercher un collaborateur à modifier")
        table.add_row("3", "Retour au menu principal")
        console.print(table)

    @staticmethod
    def modify_collaborator_by_id():
        return int(Prompt.ask("[bold green]Entrez l'ID du collaborateur à modifier [/bold green]"))

    @staticmethod
    def get_new_collaborator_info():
        console.print("Entrez les nouvelles informations du collaborateur: ", style="bold magenta")
        modify_collaborator = {"username": Prompt.ask("[bold green]"
                                                      "Saisissez un nom utilisateur pour le collaborateur"
                                                      "[/bold green]"),
                               "password": Prompt.ask("[bold green]"
                                                      "Saisissez un mot de passe pour le collaborateur"
                                                      "[/bold green]", password=True),
                               "first_name": Prompt.ask("[bold green]"
                                                        "Saisissez le prénom du collaborateur"
                                                        "[/bold green]"),
                               "last_name": Prompt.ask("[bold green]"
                                                       "Saisissez le nom du collaborateur: "
                                                       "[/bold green]"),
                               "role": Prompt.ask("[bold green]"
                                                  "Saisissez le code du rôle du collaborateur ("
                                                  "C pour Commercial, "
                                                  "G pour Gestion, "
                                                  "S pour Support"
                                                  ")"
                                                  "[/bold green]").upper()}
        return modify_collaborator

    """Delete d'un collaborateur """

    @staticmethod
    def delete_collaborator_by_id():
        return int(Prompt.ask("[bold green]Entrez l'ID du collaborateur à supprimer [/bold green]"))

    @staticmethod
    def confirm_action(username):
        return Prompt.ask(f"[bold magenta]"
                          f"Voulez-vous vraiment supprimer le collaborateur [bold cyan]{username}[/ bold cyan] ? (Y/N)"
                          f"[/bold magenta]")

    @staticmethod
    def display_delete_success(username):
        console.print(f"[bold green]"
                      f"Le collaborateur [bold cyan]{username}[/ bold cyan] a été supprimé avec succès."
                      f"[/bold green]")

    @staticmethod
    def display_delete_failure(username):
        console.print(f"[bold red]"
                      f"La suppression du collaborateur {username} a échoué ou a été annulée."
                      f"[/bold red]")


def display_collaborator_table(collaborator_data):
    table = Table(title="Création du collaborateur", title_style="bold magenta", border_style="bold yellow")
    table.add_column("Champs", style="bold blue", header_style="bold cyan")
    table.add_column("Valeur", style="bold blue", header_style="bold cyan")

    for field, value in collaborator_data.items():
        if field != "password":
            table.add_row(str(field), str(value), style="bold cyan")

    console.print(table)
