import os
from collaborator_app.model import Collaborator
import jwt
from config.config import SECRET_KEY


class CollaboratorService:
    @staticmethod
    def create_first_collaborator(username, password, first_name, last_name, role):
        collaborator = Collaborator(username=username, password=password, first_name=first_name, last_name=last_name, role=role)
        collaborator.set_password(password)
        collaborator.save()
        return collaborator

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
