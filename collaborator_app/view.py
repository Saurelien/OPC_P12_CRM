from rich.console import Console
from rich.table import Table
from rich.align import Align
from rich.prompt import Prompt

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
        username = Prompt.ask("[bold green]Nom d'utilisateur[/bold green]")
        password = Prompt.ask("[bold green]Mot de passe[/bold green]", password=True)
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
        table.add_column("description", style="bold cyan", justify="center", no_wrap=True)
        table.add_column("helper", style="bold cyan", justify="left", no_wrap=True)
        rows = [
            ("1.", "Créer un nouveau collaborateur", "Permet la création d'un nouveau collaborateur"),
            ("2.", "Rechercher un client", "Affiche les clients existants"),
            ("3.", "Rechercher un contrat", "Affiche tout les contrats existant"),
            ("4.", "Rechercher un évènement", "Affiche les event existant"),
            ("5.", "Créer un contrat",
             "Affiche un menu pour la création d'un contrat"),
            ("6.", "Modification d'un contrat", "Modification d'un contrat"),
            ("7.", "Assigner un support a un évènement",
             "Assigner un collaborateur du département support à un évènnement"),
            ("8.", "Modifier un collaborateur", ""),
            ("9.", "Afficher les collaborateurs", "Affiche les collaborateurs existants"),
            ("10.", "Supprimer un collaborateur", "Permet la suppression d'un collaborateur"),
            ("Q.", "Se déconnecter", "Deconnecte l'utilisateur en toute sécurité du programme"),
        ]
        for choice, description, helper in rows:
            table.add_row(choice, description, helper)
        console.print(table)

    @staticmethod
    def display_commercial_menu():
        console.bell()
        table = Table(title="== Menu Commercial ==", show_header=True,
                      header_style="bold magenta",
                      border_style="bold yellow",
                      title_style="bold magenta",
                      title_justify="center")
        table.add_column(Align.center("Choix Commercial"), style="bold cyan", justify="center")
        table.add_column(Align.center("Description"), style="bold cyan", justify="left")
        table.add_column(Align.center("HELPER"), style="bold cyan", justify="left")
        table.add_row("1.", "Créer une fiche client", "Permet de créer une fiche avec les informations du client")
        table.add_row("2.", "Rechercher un client", "Affiche tous les clients existants")
        table.add_row("3.", "Rechercher un contrat", "Affiche tous les contrats existant")
        table.add_row("4.", "Rechercher un évènement", "Affiche les event existant")
        table.add_row("5.", "Mettre à jour un client", "Permet la modifications des informations d'un client")
        table.add_row("6.", "Mettre à jour un contrat", "Permet la modifcation des informations d'un contrat")
        table.add_row("7.", "Afficher les contrats non signé/impayé", "Affiche les contrats ayant un impayé et ou non "
                                                                      "signé")
        table.add_row("8.", "Créer un évènement pour un client ayant souscrit a un contrat", "Affiche un tableau"
                                                                                             "contenant les contrats "
                                                                                             "que"
                                                                                             "vos clients"
                                                                                             "ont signé")
        table.add_row("9.", "Afficher les collaborateurs", "Affiche tous les collaborateurs")
        table.add_row("10.", "Supprimer un client", "Affiche les clients du commercial avant le choix de l'id pour la suppression")
        table.add_row("Q.", "Se déconnecter", "Quitte votre session")
        console.print(table)

    @staticmethod
    def display_support_menu():
        console.bell()
        table = Table(title="== Menu Support ==", show_header=True,
                      header_style="bold magenta",
                      border_style="bold yellow",
                      title_style="bold magenta",
                      title_justify="center")
        table.add_column("Choix Support", style="bold cyan", justify="center")
        table.add_column("Description", style="bold cyan", justify="left")
        table.add_column("HELPER", style="bold cyan", justify="left")
        table.add_row("1.", "Rechercher un client", "Affiche les clients existants")
        table.add_row("2.", "Rechercher un contrat", "Affiche tout les contrats existant")
        table.add_row("3.", "Rechercher un évènement", "Affiche les event existant")
        table.add_row("4.", "Afficher les collaborateurs", "Affiche les collaborateurs"),
        table.add_row("5.", "Afficher vos évènements", "Affiche vos évènements auxquels vous êtes assigné"),
        table.add_row("6.", "Modifier vos évènements", "Permet la modification d'un event auquel vous êtes assigné"),
        table.add_row("Q.", "Se déconnecter", "Quitte votre session")
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
    def get_new_collaborator_info(collaborator):
        console.print("Entrez les nouvelles informations du collaborateur (laisser vide pour ne pas modifier) : ",
                      style="bold magenta")

        modify_collaborator = {
            "username": Prompt.ask("[bold green]Saisissez un nom utilisateur pour le collaborateur[/bold green]",
                                   default=collaborator.username),
            "password": Prompt.ask("[bold green]Saisissez un mot de passe pour le collaborateur[/bold green]",
                                   password=True),
            "first_name": Prompt.ask("[bold green]Saisissez le prénom du collaborateur[/bold green]",
                                     default=collaborator.first_name),
            "last_name": Prompt.ask("[bold green]Saisissez le nom du collaborateur[/bold green]",
                                    default=collaborator.last_name),
            "role": Prompt.ask(
                "[bold green]Saisissez le rôle du collaborateur (C pour Commercial, G pour Gestion, S pour Support)[/bold green]",
                default=collaborator.role).upper()
        }

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

    @staticmethod
    def display_insufficient_permissions():
        print("Vous n'avez pas les permissions nécessaires pour supprimer un collaborateur."
              " Seul un gestionnaire peut effectuer cette action.")


def display_collaborator_table(collaborator_data):
    table = Table(title="Création du collaborateur", title_style="bold magenta", border_style="bold yellow")
    table.add_column("Champs", style="bold blue", header_style="bold cyan")
    table.add_column("Valeur", style="bold blue", header_style="bold cyan")

    for field, value in collaborator_data.items():
        if field != "password":
            table.add_row(str(field), str(value), style="bold cyan")

    console.print(table)
