from rich.console import Console
from rich.table import Table
import getpass

console = Console(width=200)


class MenuView:
    @staticmethod
    def display_menu():
        table = Table(show_header=True, header_style="bold magenta", title_justify="center", border_style="bold yellow")
        table.add_column("Choix", justify="center", style="bold cyan")
        table.add_column("Description", justify="center", style="bold cyan")
        table.add_row("1", "Se connecter")
        table.add_row("2", "Afficher les collaborateurs crées")
        table.add_row("Q", "Quitter")
        console.print(table)

    @staticmethod
    def display_collaborators(collaborators):
        table = Table(show_header=True, header_style="bold magenta", border_style="bold yellow")
        table.add_column("ID", style="cyan", justify="center")
        table.add_column("Username", style="cyan", justify="center")
        table.add_column("Password", style="cyan", justify="center")
        table.add_column("First Name", style="cyan", justify="center")
        table.add_column("Last Name", style="cyan", justify="center")
        table.add_column("Role", style="cyan", justify="center")

        for collaborator in collaborators:
            table.add_row(
                str(collaborator.id),
                collaborator.username,
                collaborator.password,
                collaborator.first_name,
                collaborator.last_name,
                collaborator.role
            )

        console.print(table, justify="center")

    @staticmethod
    def display_login_menu():
        console.print("[bold cyan]== Connexion ==[/bold cyan]")
        username = input("Nom d'utilisateur : ")
        password = getpass.getpass("Mot de passe : ")
        return username, password

    @staticmethod
    def display_gestion_menu():
        console.bell()
        table = Table(show_header=True, header_style="bold magenta", border_style="bold yellow")
        table.add_column("== Menu Gestion ==", style="bold cyan", justify="center")
        table.add_row("1. Créer un nouveau collaborateur")
        table.add_row("2. Rechercher un client")
        table.add_row("3. Rechercher un contrat")
        table.add_row("4. Rechercher un évènement")
        table.add_row("5. Créer ou modifier un contrat")
        table.add_row("6. Afficher tous les évènements")
        table.add_row("7. Assigner un support a un évènement")
        table.add_row("Q. Se déconnecter")
        console.print(table)

    @staticmethod
    def display_commercial_menu():
        table = Table(show_header=True, header_style="bold magenta", border_style="bold yellow")
        table.add_column("== Menu Commercial ==", style="bold cyan", justify="center")
        table.add_row("1. Créer une fiche client")
        table.add_row("2. Rechercher un client")
        table.add_row("3. Rechercher un contrat")
        table.add_row("4. Rechercher un évènement")
        table.add_row("5. Mettre à jour un client")
        table.add_row("6. Mettre à jour un contrat")
        table.add_row("7. Afficher les contrats non signé/impayé")
        table.add_row("8. Créer un évènement pour un client ayant souscrit a un contrat")
        table.add_row("Q. Se déconnecter")
        console.print(table)

    @staticmethod
    def display_support_menu():
        table = Table(show_header=True, header_style="bold magenta", border_style="bold yellow")
        table.add_column("== Menu Support ==", style="bold cyan", justify="center")
        table.add_row("1. Rechercher un client")
        table.add_row("2. Rechercher un contrat")
        table.add_row("3. Rechercher un évènement")
        table.add_row("Q. Se déconnecter")
        console.print(table)

    @staticmethod
    def display_create_collaborator_menu(role_choices, get_username_validity):
        console.clear()
        collaborator_data = {}
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Champs", style="bold cyan")
        table.add_column("Valeurs Utilisateur", style="bold yellow")
        collaborator_fields = ["username", "password", "first_name", "last_name", "role"]
        for field in collaborator_fields:
            if field == "role":
                for role_code, role_desc in role_choices:
                    console.print(f" - {role_code}: {role_desc}")
                while True:
                    role_code = input("Saisir le rôle du collaborateur: ").upper()
                    valid_role_codes = [code for code, _ in role_choices]
                    if role_code in valid_role_codes:
                        role_desc = dict(role_choices)[role_code]
                        collaborator_data[field] = role_desc
                        table.add_row(field.capitalize(), role_desc)
                        break
                    else:
                        console.print("Rôle invalide ! Veuillez choisir un role de la liste.", style="red")
            elif field == "username":
                while True:
                    username_value = input(f"Enter {field.capitalize()}: ")
                    if not get_username_validity(username_value):
                        collaborator_data[field] = username_value
                        table.add_row(field.capitalize(), username_value)
                        break
                    else:
                        console.print("Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.", style="red")
            elif field == "password":
                password_value = input(f"Entrer un {field.capitalize()}: ")
                collaborator_data[field] = password_value
                table.add_row(field.capitalize(), "Mot de Passe bien enregistré :)")
            else:
                value = input(f"Entrer un {field.capitalize()}: ")
                collaborator_data[field] = value
                table.add_row(field.capitalize(), value)

        console.print(table)

        return collaborator_data
