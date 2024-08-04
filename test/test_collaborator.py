from unittest.mock import patch

from services.utils import Session
from utils import generate_collaborator_data, generate_collaborator, delete_collaborator
from collaborator_app.model import Collaborator
from collaborator_app.controller import MainController
from collaborator_app.view import MenuView


def mock_current_user_gestion(*args, **kwargs):
    return generate_collaborator(role=Collaborator.GESTION)


def mock_current_user_commercial(*args, **kwargs):
    return generate_collaborator(role=Collaborator.COMMERCIAL)


def mock_current_user_support(*args, **kwargs):
    return generate_collaborator(role=Collaborator.SUPPORT)


def test_create_commercial_collaborator(test_track):
    commercial_collaborator = Collaborator.select().where(Collaborator.username == 'test_commercial_user').first()

    if commercial_collaborator:
        print("Le collaborateur avec le nom d'utilisateur 'test_commercial_user' existe déjà.")
    else:
        mock_collaborator_data = generate_collaborator_data()

        with patch('collaborator_app.view.MenuView.display_create_collaborator_menu',
                   return_value=mock_collaborator_data):
            MainController.create_first_collaborator()

        commercial_collaborator = Collaborator.get(Collaborator.username == mock_collaborator_data['username'])

        commercial_collaborator.set_password(mock_collaborator_data['password'])
        commercial_collaborator.save()

        assert commercial_collaborator is not None
        assert commercial_collaborator.first_name == mock_collaborator_data['first_name']
        assert commercial_collaborator.last_name == mock_collaborator_data['last_name']
        assert commercial_collaborator.role == mock_collaborator_data['role']

        print("Collaborateur commercial créé avec succès et vérifié.")

        collaborators = Collaborator.select()
        print("Collaborateurs dans la base de données de test:")
        for collab in collaborators:
            print(f"{collab.username}, {collab.first_name}, {collab.last_name}, {collab.role}")


def test_create_gestion_collaborator(test_track):
    management_collaborator = Collaborator.select().where(Collaborator.username == 'test_management_user').first()

    if management_collaborator:
        print("Le collaborateur avec le nom d'utilisateur 'test_management_user' existe déjà.")
    else:
        mock_collaborator_data = generate_collaborator_data(role='G')

        with patch('collaborator_app.view.MenuView.display_create_collaborator_menu',
                   return_value=mock_collaborator_data):
            MainController.create_first_collaborator()

        management_collaborator = Collaborator.get(Collaborator.username == mock_collaborator_data['username'])

        management_collaborator.set_password(mock_collaborator_data['password'])
        management_collaborator.save()

        assert management_collaborator is not None
        assert management_collaborator.first_name == mock_collaborator_data['first_name']
        assert management_collaborator.last_name == mock_collaborator_data['last_name']
        assert management_collaborator.role == mock_collaborator_data['role']

        print("Collaborateur de gestion créé avec succès et vérifié.")

        collaborators = Collaborator.select()
        print("Collaborateurs dans la base de données de test:")
        for collab in collaborators:
            print(f"{collab.username}, {collab.first_name}, {collab.last_name}, {collab.role}")


def test_create_support_collaborator(test_track):
    support_collaborator = Collaborator.select().where(Collaborator.username == 'test_support_user').first()

    if support_collaborator:
        print("Le collaborateur avec le nom d'utilisateur 'test_support_user' existe déjà.")
    else:
        mock_collaborator_data = generate_collaborator_data(role='S')

        with patch('collaborator_app.view.MenuView.display_create_collaborator_menu',
                   return_value=mock_collaborator_data):
            MainController.create_first_collaborator()

        support_collaborator = Collaborator.get(Collaborator.username == mock_collaborator_data['username'])

        support_collaborator.set_password(mock_collaborator_data['password'])
        support_collaborator.save()

        assert support_collaborator is not None
        assert support_collaborator.first_name == mock_collaborator_data['first_name']
        assert support_collaborator.last_name == mock_collaborator_data['last_name']
        assert support_collaborator.role == mock_collaborator_data['role']

        print("Collaborateur de support créé avec succès et vérifié.")

        collaborators = Collaborator.select()
        print("Collaborateurs dans la base de données de test:")
        for collab in collaborators:
            print(f"{collab.username}, {collab.first_name}, {collab.last_name}, {collab.role}")


def test_create_and_save_collaborator(test_track):
    generated_collaborator = generate_collaborator()
    generated_collaborator.save()
    retrieved_collaborator = Collaborator.get(Collaborator.username == generated_collaborator.username)
    assert retrieved_collaborator is not None
    assert retrieved_collaborator.username == generated_collaborator.username
    assert retrieved_collaborator.first_name == generated_collaborator.first_name
    assert retrieved_collaborator.last_name == generated_collaborator.last_name
    assert retrieved_collaborator.role == generated_collaborator.role

    print("Test de création et sauvegarde de collaborateur passé avec succès.")


def test_collaborator_methods(test_track):
    generated_collaborator = generate_collaborator()
    password = "testpassword"
    generated_collaborator.set_password(password)
    assert generated_collaborator.verify_password(password) is True

    print("Test des méthodes de l'objet Collaborator passé avec succès.")


def test_display_create_collaborator_menu():
    with patch('rich.prompt.Prompt.ask', side_effect=[
        "test_user",
        "test_pass",
        "Test",
        "User",
        "C"
    ]):
        collaborator_data = MenuView.display_create_collaborator_menu()
        assert collaborator_data == {
            "username": "test_user",
            "password": "test_pass",
            "first_name": "Test",
            "last_name": "User",
            "role": "C"
        }
        print("Création de collaborateur simulée et vérifiée avec succès.")


def test_create_and_verify_password(test_track):
    commercial_collaborator = Collaborator.select().where(Collaborator.username == 'test_commercial_user').first()

    if not commercial_collaborator:
        mock_collaborator_data = generate_collaborator_data()

        with patch('collaborator_app.view.MenuView.display_create_collaborator_menu',
                   return_value=mock_collaborator_data):
            MainController.create_first_collaborator()

        commercial_collaborator = Collaborator.get(Collaborator.username == mock_collaborator_data['username'])

    commercial_collaborator.set_password("1234")
    commercial_collaborator.save()

    assert commercial_collaborator is not None
    assert commercial_collaborator.password != "1234"
    is_password_verified = commercial_collaborator.verify_password("1234")
    assert is_password_verified

    print("Le mot de passe est correctement hashé et vérifié.")


def test_login_collaborator(test_track):
    mock_collaborator_data = generate_collaborator_data()

    with patch('collaborator_app.view.MenuView.display_create_collaborator_menu', return_value=mock_collaborator_data):
        MainController.create_first_collaborator()

    with patch('collaborator_app.view.MenuView.display_login_menu',
               return_value=(mock_collaborator_data['username'], mock_collaborator_data['password'])):
        login_username, login_password = MenuView.display_login_menu()

        collaborator = Collaborator.get(Collaborator.username == login_username)
        is_password_verified = collaborator.verify_password(login_password)

        assert collaborator is not None
        assert is_password_verified

        print("Connexion utilisateur réussie et vérifiée.")


def test_username_exists(test_track):
    assert Collaborator.username_exists(Collaborator.username) is True
    assert Collaborator.username_exists('nonexistent_username') is False


def test_validate_username(test_track):
    assert Collaborator.validate_username('unique_username') is True
    assert Collaborator.validate_username(Collaborator.username) is False


def test_validate_password():
    assert Collaborator.validate_password('password123', 'password123') is True
    assert Collaborator.validate_password('password123', 'differentpassword') is False


def test_validate_role():
    assert Collaborator.validate_role('C') is True
    assert Collaborator.validate_role('G') is True
    assert Collaborator.validate_role('S') is True

    assert Collaborator.validate_role('A') is False
    assert Collaborator.validate_role('') is False
    assert Collaborator.validate_role(None) is False


# def test_delete_collaborator_as_gestion():
#     """
#     Teste la suppression d'un collaborateur par un utilisateur avec un rôle de gestion.
#     """
#     gestion_collaborator = generate_collaborator(role=Collaborator.GESTION)
#     Session.user = gestion_collaborator
#     collaborator_to_delete = generate_collaborator(role=Collaborator.COMMERCIAL)
#     with (patch('collaborator_app.controller.MenuView.delete_collaborator_by_id',
#                 return_value=collaborator_to_delete.id),
#           patch('collaborator_app.controller.MenuView.confirm_action', return_value="y"),
#           patch('collaborator_app.controller.MenuView.display_delete_success') as mock_success,
#           patch('collaborator_app.controller.MenuView.display_delete_failure') as mock_failure,
#           patch(
#               'collaborator_app.controller.MenuView.display_insufficient_permissions')
#           as mock_insufficient_permissions):
#         MainController.delete_collaborator()
#
#         assert mock_insufficient_permissions.call_count == 0, ("Le message d'insuffisance de permissions ne devrait "
#                                                                "pas être affiché pour un utilisateur de gestion.")
#         assert mock_success.call_count == 1, "Le message de succès devrait être affiché pour un utilisateur de gestion."
#         assert mock_failure.call_count == 0, ("Le message d'échec ne devrait pas être affiché pour un utilisateur de "
#                                               "gestion.")
#         print(
#             f"\nTest de suppression pour utilisateur de gestion réussi:"
#             f"\nLe collaborateur '{collaborator_to_delete.username}' a été supprimé avec succès.")
#
#
# def test_delete_collaborator_as_commercial():
#     """
#     Teste la tentative de suppression d'un collaborateur par un utilisateur avec un rôle commercial.
#     """
#     commercial_collaborator = generate_collaborator(role=Collaborator.COMMERCIAL)
#     Session.user = commercial_collaborator
#     collaborator_to_delete = generate_collaborator(role=Collaborator.COMMERCIAL)
#
#     with (patch('collaborator_app.controller.MenuView.delete_collaborator_by_id',
#                 return_value=collaborator_to_delete.id),
#           patch('collaborator_app.controller.MenuView.confirm_action', return_value="y"),
#           patch('collaborator_app.controller.MenuView.display_delete_success') as mock_success,
#           patch('collaborator_app.controller.MenuView.display_delete_failure') as mock_failure,
#           patch(
#               'collaborator_app.controller.MenuView.display_insufficient_permissions') as mock_insufficient_permissions):
#         MainController.delete_collaborator()
#
#         assert mock_success.call_count == 0, (
#             "Le message de succès ne devrait pas être affiché pour un utilisateur commercial.")
#
#         assert mock_failure.call_count == 0, (
#             "Le message d'échec ne devrait pas être affiché pour un utilisateur commercial.")
#
#         assert mock_insufficient_permissions.call_count == 1, (
#             "Le message d'insuffisance de permissions devrait être affiché pour un utilisateur commercial.")
#
#         print(
#             f"\nTest de suppression pour utilisateur commercial réussi:"
#             f"\nLe collaborateur '{collaborator_to_delete.username}' n'a pas été supprimé car l'utilisateur:"
#             f" {commercial_collaborator.username} n'a pas "
#             f"\nles permissions nécessaires."
#             f"\nPermission attendue: {Collaborator.GESTION}")
