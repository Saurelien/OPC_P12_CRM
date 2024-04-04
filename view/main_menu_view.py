from rich.console import Console
from rich.table import Table

console = Console()


class MenuView:
    @staticmethod
    def display_menu():
        console.clear()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="cyan")
        table.add_column("Description")
        table.add_row("1", "Créer un nouveau collaborateur")
        table.add_row("2", "Afficher les collaborateurs crées")
        table.add_row("Q", "Quit")
        console.print(table)

    @staticmethod
    def display_collaborators(collaborators):
        console.clear()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan")
        table.add_column("Username", style="cyan")
        table.add_column("Password", style="cyan")
        table.add_column("First Name", style="cyan")
        table.add_column("Last Name", style="cyan")
        table.add_column("Role", style="cyan")

        for collaborator in collaborators:
            table.add_row(
                str(collaborator.id),
                collaborator.username,
                collaborator.password,
                collaborator.first_name,
                collaborator.last_name,
                collaborator.role
            )

        console.print(table)

    @staticmethod
    def display_create_first_collaborator_menu(role_choices):
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
                    role_code = input("Saisir le code du rôle du collaborateur: ").upper()
                    valid_role_codes = [code for code, _ in role_choices]
                    if role_code in valid_role_codes:
                        role_desc = dict(role_choices)[role_code]
                        collaborator_data[field] = role_desc
                        table.add_row(field.capitalize(), role_desc)
                        break
                    else:
                        print("Code de rôle invalide ! Veuillez choisir un code de la liste.")
            elif field == "password":
                password_value = input(f"Enter {field.capitalize()}: ")
                collaborator_data[field] = password_value
                table.add_row(field.capitalize(), "Mot de Passe saisie")
            else:
                value = input(f"Enter {field.capitalize()}: ")
                collaborator_data[field] = value
                table.add_row(field.capitalize(), value)

        console.print(table)

        return collaborator_data
