from services.utils import CollaboratorService, AuthenticateService
from collaborator_app.model import Collaborator
from collaborator_app.view import MenuView


class MainController:
    @staticmethod
    def run():
        token = AuthenticateService.load_token()
        if token:
            user_id = AuthenticateService.decode_token(token)
            collaborator = CollaboratorService.get_collaborator_by_id(user_id)
            if collaborator:
                print("Un collaborateur est déjà authentifié.")
                MainController.display_role_menu(collaborator.role)
                return

        MenuView.display_menu()
        choice = input("Quel est votre choix ? ")
        if choice == "1":
            username, password = MenuView.display_login_menu()
            collaborator = CollaboratorService.authenticate_collaborator(username, password)
            if collaborator:
                print("TEST affichage du role du collaborateur authentifié:", collaborator.role)
                token = AuthenticateService.generate_token(collaborator.id)
                AuthenticateService.store_token(token)
                MainController.display_role_menu(collaborator.role)
            else:
                print("Authentification échouée. Nom d'utilisateur ou mot de passe incorrect.")
        elif choice == "2":
            MainController.display_existing_collaborators()
            MainController.run()
        elif choice.lower() == "q":
            print("Fermeture du programme.")

    @staticmethod
    def display_existing_collaborators():
        collaborators = Collaborator.select()
        MenuView.display_collaborators(collaborators)

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

    @staticmethod
    def display_role_menu(role):
        print("Affichage du role detecté a l'appel de la fonction display_role_menu:", role)
        if role == "Gestion":
            MenuView.display_gestion_menu()
            choice = input("Quel est votre choix ? ")
            if choice == "1":
                collaborator_data = MenuView.display_create_collaborator_menu(MainController.get_role_choices(),
                                                                              Collaborator.username_exists)
                MainController.create_first_collaborator(collaborator_data)
                return MenuView.display_gestion_menu()
            elif choice == "2":
                AuthenticateService.delete_token()
                MainController.run()
        elif role == "Commercial":
            MenuView.display_commercial_menu()
            choice = input("Quel est votre choix ? ")
            if choice == "2":
                AuthenticateService.delete_token()
                MainController.run()
        elif role == "Support":
            MenuView.display_support_menu()
            choice = input("Quel est votre choix ? ")
            if choice == "2":
                AuthenticateService.delete_token()
                MainController.run()

