import logging
from client_app.view import ClientView
from services.utils import CollaboratorService, AuthenticateService, CollaboratorModificationService, Session
from collaborator_app.model import Collaborator
from collaborator_app.view import MenuView, display_collaborator_table
from client_app.controller import MainClientController
from contract_app.controller import MainContractController
from event_app.controller import MainEventController


class MainController:
    LOGIN = "1"
    QUIT = "Q"

    @staticmethod
    def run():
        if Session.load_session():
            MainController.display_role_menu(Session.user.role)
            return

        while True:
            MenuView.display_menu()
            choice = MenuView.get_choice()
            if choice == MainController.LOGIN:
                username, password = MenuView.display_login_menu()
                if Session.authenticate(username, password):
                    MainController.display_role_menu(Session.user.role)
                    break
                else:
                    MenuView.display_fail_auth()
            elif choice.lower() == MainController.QUIT:
                MenuView.display_closing_message()
                break

    @staticmethod
    def display_existing_collaborators():
        collaborators = Collaborator.select()
        MenuView.display_collaborators(collaborators)

    @staticmethod
    def display_role_menu(role):
        if role == Collaborator.COMMERCIAL:
            MainController.commercial_control_menu()
        elif role == Collaborator.GESTION:
            MainController.gestion_control_menu()
        elif role == Collaborator.SUPPORT:
            MainController.support_control_menu()

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
            elif choice == "4":
                MainEventController.display_existing_event()
            elif choice == "5":
                MainContractController.create_contract()
            elif choice == "6":
                MainContractController.modify_contract()
            elif choice == "7":
                MainEventController.modify_event()
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
            elif choice == "2":
                MainClientController.display_existing_client()
            elif choice == "3":
                MainContractController.display_existing_contract()
            elif choice == "4":
                MainEventController.display_existing_event()
            elif choice == "5":
                MainClientController.modify_client()
            elif choice == "6":
                MainContractController.modify_contract()
            elif choice == "7":
                MainContractController.display_contracts()
            elif choice == "8":
                MainEventController.create_event()
            elif choice == "9":
                MainController.display_existing_collaborators()
            elif choice.upper() == "Q":
                AuthenticateService.delete_token()
                MainController.run()

    @classmethod
    def support_control_menu(cls):
        while True:
            MenuView.display_support_menu()
            choice = ClientView.get_choice()
            if choice == "1":
                logging.info("display_existing_client called")
                MainClientController.display_existing_client()
            elif choice == "2":
                logging.info("display_existing_contract called")
                MainContractController.display_existing_contract()
            elif choice == "3":
                logging.info("display_existing_event called")
                MainEventController.display_existing_event()
            elif choice == "4":
                logging.info("display_existing_collaborators called")
                MainController.display_existing_collaborators()
            elif choice == "5":
                logging.info("list_events called")
                MainEventController.list_events()
            elif choice == "6":
                logging.info("modify_event called")
                MainEventController.modify_event()
            elif choice.upper() == "Q":
                logging.info("Se déconnecter called")
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
        if not Session.is_gestion():
            MenuView.display_insufficient_permissions()
            return

        collaborator_id = MenuView.modify_collaborator_by_id()
        data = MenuView.get_new_collaborator_info()
        CollaboratorModificationService.validate_collaborator_modification_data(collaborator_id)
        collaborator = CollaboratorService.get_collaborator_by_id(collaborator_id)
        collaborator.set_password(data['password'])
        collaborator.username = data["username"]
        collaborator.first_name = data["first_name"]
        collaborator.last_name = data["last_name"]
        collaborator.role = data["role"]

        collaborator.save()
        current_user = Session.get_current_user()
        if current_user.id == collaborator_id:
            Session.logout()
            MainController.run()

    @classmethod
    def delete_collaborator(cls):
        if Session.user.role != Collaborator.GESTION:
            MenuView.display_insufficient_permissions()
            return

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
