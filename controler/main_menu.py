from services.utils import CollaboratorService
from model.model import Collaborator
from view.main_menu_view import MenuView


class MainController:
    @staticmethod
    def run():
        MenuView.display_menu()
        choice = input("Quel est votre choix ? ")
        if choice == "1":
            collaborator_data = MenuView.display_create_first_collaborator_menu(MainController.get_role_choices())
            MainController.create_first_collaborator(collaborator_data)
        elif choice == "2":  #
            MainController.display_existing_collaborators()
        elif choice.lower() == "q":
            print("Fermeture du programme.")

    @staticmethod
    def display_existing_collaborators():
        collaborators = Collaborator.select()
        MenuView.display_collaborators(collaborators)
        MainController.run()

    @staticmethod
    def get_role_choices():
        return Collaborator.ROLE_CHOICES

    @staticmethod
    def create_first_collaborator(collaborator_data):
        username = collaborator_data.get('username')
        if not Collaborator.username_exists(username):
            print("Username unique. Création du collaborateur en cours...")
            CollaboratorService.create_first_collaborator(**collaborator_data)
            print("Collaborateur créé avec succès !")
        else:
            print("Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
        MainController.run()


MainController.run()
