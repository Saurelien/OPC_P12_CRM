import datetime
from client_app.model import Client
from collaborator_app.model import Collaborator
from client_app.view import ClientView, display_client_table
from services.utils import AuthenticateService, CollaboratorService


class MainClientController:

    @staticmethod
    def display_existing_client():
        """Fonction qui récupère les champs souhaité pour l'affichage des clients dans les menus"""
        client = Client.select(
            Client.id,
            Client.first_name,
            Client.last_name,
            Client.email,
            Client.phone_number,
            Client.created_at,
            Client.updated_at,
            Client.commercial_assignee)
        ClientView.display_clients(client)

    @classmethod
    def create_client(cls):
        client_data = ClientView.display_create_client()
        token = AuthenticateService.load_token()

        if token:
            user_id = AuthenticateService.decode_token(token)
            commercial_collaborator = CollaboratorService.get_collaborator_by_id(user_id)

            if commercial_collaborator:
                # Créer une instance de Client en utilisant les données saisies par l'utilisateur
                new_client = Client(
                    first_name=client_data["first_name"],
                    last_name=client_data["last_name"],
                    email=client_data["email"],
                    phone_number=client_data["phone_number"],  # Assurez-vous que le numéro de téléphone est fourni
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now(),
                    commercial_assignee=commercial_collaborator  # Utilisez l'objet Collaborator lui-même
                )

                try:
                    # Enregistrer le nouveau client dans la base de données
                    new_client.save()
                    # Afficher les détails du client dans un tableau
                    display_client_table(client_data)
                except Exception as e:
                    print(f"Une erreur s'est produite lors de la création du client : {e}")
            else:
                print("Le collaborateur n'a pas été trouvé.")
        else:
            print("Token invalide.")
