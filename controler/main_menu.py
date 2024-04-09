from services.utils import CollaboratorService
from model.model import Collaborator, JWT_SECRET
from view.main_menu_view import MenuView
import jwt


class MainController:

    JWT_SECRET = JWT_SECRET

    @staticmethod
    def run():
        MenuView.display_menu()
        choice = input("Quel est votre choix ? ")
        # TODO "Faire en sorte de créer une méthode qui accède depuis le controleur a la db pour verifie la présence du username saisie par l'utilisateur | VALIDE |"
        if choice == "1":
            collaborator_data = MenuView.display_create_first_collaborator_menu(MainController.get_role_choices(),
                                                                                MainController.get_username_validity)
            MainController.create_first_collaborator(collaborator_data)
        elif choice == "2":  # Tester l'affichage de la db des collaborateurs
            MainController.display_existing_collaborators()
        elif choice == "3":  # Tester Le login et le maintien de la presence de l'utilisateur connecter avec les informations d'un collaborateur
            MainController.login()
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
    def get_username_validity(username=None):
        return Collaborator.select().where(Collaborator.username == username).exists()

    @staticmethod
    def create_first_collaborator(collaborator_data):
        CollaboratorService.create_first_collaborator(**collaborator_data)
        MainController.run()

    @staticmethod
    def login():
        while True:
            username = MainController.get_valid_username()
            password = input("Entrer un Password: ")
            collaborator = Collaborator.get_or_none(username=username)
            if collaborator:
                if collaborator.verify_password(password) == collaborator.set_password(password):
                    token = MainController.generate_token(collaborator.id)
                    MainController.save_token(token)
                    print("Connexion réussie!")
                    break
                else:
                    print("Mot de passe incorrect.")
            else:
                print("Nom d'utilisateur incorrect.")

    @staticmethod
    def get_valid_username():
        while True:
            try:
                username = input("Enter Username: ")
                if Collaborator.username_exists(username):
                    print("Le nom d'utilisateur a été trouvé")
                    return username
                else:
                    print("Nom utilisateur inconnu !")
            except ValueError as e:
                print(e)

    @staticmethod
    def generate_token(collaborator_id):
        payload = {
            'collaborator_id': collaborator_id,
        }
        token = jwt.encode(payload, MainController.JWT_SECRET, algorithm='HS256')
        return token.decode('utf-8')

    @staticmethod
    def save_token(token):
        with open('token.txt', 'w') as file:
            file.write(token)


MainController.run()
