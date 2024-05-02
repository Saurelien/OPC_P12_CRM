import os
from collaborator_app.model import Collaborator
from client_app.model import Client
from contract_app.model import Contract
from event_app.model import Event
import jwt
from config.config import SECRET_KEY
from rich.console import Console
from peewee import DoesNotExist

console = Console()


class CollaboratorService:

    @staticmethod
    def authenticate_collaborator(username, password):
        try:
            collaborator = Collaborator.get(Collaborator.username == username)
            if collaborator.verify_password(password):
                return collaborator
            else:
                return None
        except Collaborator.DoesNotExist:
            return None

    @staticmethod
    def get_collaborator_by_id(user_id):
        try:
            return Collaborator.get(Collaborator.id == user_id)
        except Collaborator.DoesNotExist:
            return None


class AuthenticateService:
    @staticmethod
    def generate_token(user_id):
        return jwt.encode({'user_id': user_id}, SECRET_KEY, algorithm='HS256')

    @staticmethod
    def store_token(token):
        with open('config/token.txt', 'w') as f:
            f.write(token)

    @staticmethod
    def load_token():
        try:
            with open('config/token.txt', 'r') as f:
                token = f.read()
                return token.strip() if token.strip() else None
        except FileNotFoundError:
            return None

    @staticmethod
    def decode_token(token):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded_token.get('user_id')
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def delete_token():
        try:
            os.remove('config/token.txt')
        except FileNotFoundError:
            pass


class CollaboratorValidator:
    @staticmethod
    def validate_username(username):
        print(username)
        return not Collaborator.username_exists(username)

    @staticmethod
    def validate_role(role_code):
        print(role_code)
        return role_code in ['C', 'G', 'S']

    @staticmethod
    def validate_collaborator_data(collaborator_data):
        is_valid = True

        if not CollaboratorValidator.validate_username(collaborator_data.get("username")):
            console.print("Nom d'utilisateur déjà utilisé. Veuillez en choisir un autre.", style="bold red")
            is_valid = False

        if not CollaboratorValidator.validate_role(collaborator_data.get("role")):
            console.print("Code de rôle invalide.", style="bold red")
            is_valid = False
        print(is_valid)
        return is_valid


class CollaboratorModificationService:
    @staticmethod
    def validate_collaborator_modification_data(collaborator_id):
        if not CollaboratorModificationService.is_valid_collaborator_id(collaborator_id):
            raise ValueError("ID Collaborateur invalide")

        # if not CollaboratorModificationService.validate_new_collaborator_info(modified_collaborator):
        #     raise ValueError("Informations de la modification du collaborateur invalide")

    @staticmethod
    def is_valid_collaborator_id(collaborator_id):
        try:
            Collaborator.get_by_id(collaborator_id)
            return True
        except DoesNotExist:
            console.print("ID du collaborateur inexistant.", style="bold red")
            return False


def get_model_fields(model):
    """
    Récupère les champs d'un modèle et retourne une liste de tuples (nom du champ, type du champ).
    """
    fields = []
    for field_name, field in model._meta.fields.items():
        fields.append((field_name, type(field).__name__))
    return fields

