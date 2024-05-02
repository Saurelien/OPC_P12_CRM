from client_app.view import ClientView
from services.utils import CollaboratorService, AuthenticateService, CollaboratorModificationService
from collaborator_app.model import Collaborator, PH
from client_app.model import Client
from event_app.model import Event
from collaborator_app.view import MenuView, display_collaborator_table
from client_app.controller import MainClientController
from contract_app.controller import MainContractController


class MainController:
    LOGIN = "1"
    QUIT = "Q"

    @staticmethod
    def run():
        token = AuthenticateService.load_token()
        if token:
            user_id = AuthenticateService.decode_token(token)
            collaborator = CollaboratorService.get_collaborator_by_id(user_id)
            if collaborator:
                MainController.display_role_menu(collaborator.role)
                return

        while True:
            MenuView.display_menu()
            choice = MenuView.get_choice()
            if choice == MainController.LOGIN:
                username, password = MenuView.display_login_menu()
                collaborator = CollaboratorService.authenticate_collaborator(username, password)
                if collaborator:
                    token = AuthenticateService.generate_token(collaborator.id)
                    AuthenticateService.store_token(token)
                    MainController.display_role_menu(collaborator.role)
                    break
                else:
                    MenuView.display_fail_auth()
            elif choice.lower() == MainController.QUIT:
                MenuView.display_closing_message()
                break

    @staticmethod
    def display_existing_collaborators():
        """Fonction qui récupère les champs souhaité pour l'affichage des collaborateurs dans les menus en indiquant en params de select les champs voulus"""
        collaborators = Collaborator.select(Collaborator.id,
                                            Collaborator.username,
                                            Collaborator.first_name,
                                            Collaborator.last_name,
                                            Collaborator.role)
        MenuView.display_collaborators(collaborators)

    @staticmethod
    def display_role_menu(role):
        if role == Collaborator.GESTION:
            MainController.gestion_control_menu()
        elif role == Collaborator.COMMERCIAL:
            MainController.commercial_control_menu()
        elif role == Collaborator.SUPPORT:
            MenuView.display_support_menu()
            choice = MenuView.get_choice()
            if choice.upper() == "Q":
                AuthenticateService.delete_token()
                MainController.run()

    @classmethod
    def gestion_control_menu(cls):
        while True:
            MenuView.display_gestion_menu()
            choice = MenuView.get_choice()

            if choice == "1":
                cls.create_first_collaborator()
            elif choice == "2":
                MainClientController.display_existing_client()
            elif choice == "3":
                MainContractController.display_existing_contract()
            elif choice == "5":
                # cls qui affiche un sous menu avec un choix de création et un choix de modification d'un contrat
                pass
            elif choice == "8":
                MainController.display_existing_collaborators()
                cls.modify_collaborator()
            elif choice == "9":
                MainController.display_existing_collaborators()
            elif choice == "10":
                MainController.display_existing_collaborators()
                cls.delete_collaborator()
            elif choice.upper() == "Q":
                AuthenticateService.delete_token()
                MainController.run()

    @classmethod
    def commercial_control_menu(cls):
        while True:
            MenuView.display_commercial_menu()
            choice = ClientView.get_choice()
            if choice == "1":
                MainClientController.create_client()
            elif choice.upper() == "Q":
                AuthenticateService.delete_token()
                MainController.run()

    @classmethod
    def create_first_collaborator(cls):
        collaborator_data = MenuView.display_create_collaborator_menu()
        new_collaborator = Collaborator(username=collaborator_data["username"],
                                        first_name=collaborator_data["first_name"],
                                        last_name=collaborator_data["last_name"],
                                        role=collaborator_data["role"])
        password = collaborator_data["password"]
        new_collaborator.set_password(password)
        new_collaborator.save()
        display_collaborator_table(collaborator_data)

    @classmethod
    def modify_collaborator(cls):
        collaborator_id = MenuView.modify_collaborator_by_id()
        data = MenuView.get_new_collaborator_info()
        CollaboratorModificationService.validate_collaborator_modification_data(collaborator_id)

        collaborator = CollaboratorService.get_collaborator_by_id(collaborator_id)
        collaborator.set_password(data['password'])
        collaborator.username = data["username"]
        collaborator.first_name = data["first_name"]
        collaborator.last_name = data["last_name"]
        collaborator.role = data["role"]
        Collaborator.save(collaborator)
        token = AuthenticateService.load_token()
        if token:
            user_id = AuthenticateService.decode_token(token)
            if user_id == collaborator_id:
                AuthenticateService.delete_token()
                MainController.run()

    @classmethod
    def delete_collaborator(cls):
        collaborator_id = MenuView.delete_collaborator_by_id()
        try:
            collaborator = Collaborator.get_by_id(collaborator_id)
        except Collaborator.DoesNotExist:
            return

        confirmation = MenuView.confirm_action(collaborator.username)
        if confirmation.lower() == "y":
            collaborator.delete_instance()
            MenuView.display_delete_success(collaborator.username)
        else:
            MenuView.display_delete_failure(collaborator.username)
