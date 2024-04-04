from model.model import Collaborator


class CollaboratorService:
    @staticmethod
    def create_first_collaborator(username, password, first_name, last_name, role):
        collaborator = Collaborator(username=username, first_name=first_name, last_name=last_name, role=role)
        collaborator.set_password(password)
        collaborator.save()
        return collaborator

