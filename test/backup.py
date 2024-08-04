# import pytest
# from unittest.mock import patch
# from peewee import PostgresqlDatabase, ProgrammingError
#
# # import collaborator_app.controller
# from collaborator_app.model import Collaborator
# from collaborator_app.controller import MainController
# from collaborator_app.view import MenuView
# from config.config import (db_test, DATABASE_TEST_NAME, DATABASE_TEST_USER, DATABASE_TEST_PASSWORD, DATABASE_TEST_HOST,
#                            ADMIN_USER)
#
#
# def create_test_database():
#     try:
#         # Connexion en tant qu'administrateur pour créer la base de données de test
#         db_admin = PostgresqlDatabase('postgres', user=ADMIN_USER, password=DATABASE_TEST_PASSWORD, host=DATABASE_TEST_HOST)
#         db_admin.connect()
#         print("Connexion réussie à PostgreSQL en tant qu'utilisateur 'postgres'.")
#     except Exception as e:
#         print(f"Erreur lors de la connexion à la base de données 'postgres' : {e}")
#         return
#
#     try:
#         # Vérifier si la base de données de test existe déjà
#         db_exists = db_admin.execute_sql(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_TEST_NAME}'").fetchone()
#         if not db_exists:
#             # Créer la base de données de test
#             db_admin.execute_sql(f'CREATE DATABASE {DATABASE_TEST_NAME} OWNER {ADMIN_USER}')
#             print(f"La base de données '{DATABASE_TEST_NAME}' a été créée avec succès.")
#         else:
#             print(f"La base de données '{DATABASE_TEST_NAME}' existe déjà.")
#     except ProgrammingError as e:
#         print(f"Erreur lors de la création ou vérification de la base de données : {e}")
#     finally:
#         db_admin.close()
#
#     try:
#         # Connexion à la base de données de test en tant qu'administrateur
#         db_test.init(DATABASE_TEST_NAME, user=ADMIN_USER, password=DATABASE_TEST_PASSWORD, host=DATABASE_TEST_HOST)
#         db_test.connect()
#         print(f"Connexion réussie à la base de données '{DATABASE_TEST_NAME}' en tant qu'utilisateur '{ADMIN_USER}'.")
#
#         # Modifier le propriétaire du schéma public
#         db_test.execute_sql("ALTER SCHEMA public OWNER TO postgres;")
#         print("Le propriétaire du schéma public a été modifié en 'postgres'.")
#
#         # Accorder les droits de création de table à l'utilisateur de test
#         db_test.execute_sql(f"GRANT CREATE ON SCHEMA public TO {DATABASE_TEST_USER};")
#         print(f"Autorisation de création accordée à l'utilisateur {DATABASE_TEST_USER} pour le schéma public.")
#     except ProgrammingError as e:
#         print(f"Erreur lors de la configuration des privilèges : {e}")
#     finally:
#         db_test.close()
#
#
# @pytest.fixture(scope='module')
# def test_db():
#     create_test_database()
#
#     db_test.init(DATABASE_TEST_NAME, user=DATABASE_TEST_USER, password=DATABASE_TEST_PASSWORD, host=DATABASE_TEST_HOST)
#     db_test.connect()
#     print("Connexion réussie à la base de données de test en tant qu'utilisateur 'user_collaborator'.")
#     db_test.bind([Collaborator])
#
#     # Créer les tables et afficher le chemin de la table créée de la db de test
#     db_test.create_tables([Collaborator])
#     print(f"Création de la Table {Collaborator._meta.table_name}, pour la db de test {db_test}")
#
#     cursor = db_test.execute_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
#     tables = cursor.fetchall()
#     print("Tables dans la base de données de test:")
#     for table in tables:
#         print(table)
#
#     yield db_test
#
#     # TEST supprimer la table et fermer la connexion
#     # db_test.drop_tables([Collaborator])
#     print(f"Fermeture de la connexion à la db de test {db_test.close()})")
#
#
# def test_create_commercial_collaborator(test_db):
#     commercial_collaborator = Collaborator.select().where(Collaborator.username == 'test_commercial_user').first()
#
#     if commercial_collaborator:
#         print("Le collaborateur avec le nom d'utilisateur 'test_commercial_user' existe déjà.")
#     else:
#         mock_collaborator_data = {
#             "username": "test_commercial_user",
#             "password": "1234",  # Mot de passe brut
#             "first_name": "test_toto_commercial",
#             "last_name": "test_user_toto",
#             "role": "C"
#         }
#
#         with patch('collaborator_app.view.MenuView.display_create_collaborator_menu',
#                    return_value=mock_collaborator_data):
#             MainController.create_first_collaborator()
#
#         commercial_collaborator = Collaborator.get(Collaborator.username == 'test_commercial_user')
#
#         # TEST de hasher le mot de passe du collaborateur de test avec set_password
#         commercial_collaborator.set_password("1234")
#
#         commercial_collaborator.save()
#
#         assert commercial_collaborator is not None
#         assert commercial_collaborator.first_name == 'test_toto_commercial'
#         assert commercial_collaborator.last_name == 'test_user_toto'
#         assert commercial_collaborator.role == 'C'
#
#         print("Collaborateur commercial créé avec succès et vérifié.")
#
#         # Afficher les collaborateurs créés
#         collaborators = Collaborator.select()
#         print("Collaborateurs dans la base de données de test:")
#         for collab in collaborators:
#             print(f"{collab.username}, {collab.first_name}, {collab.last_name}, {collab.role}")
#
#
# def test_display_create_collaborator_menu():
#     # Simuler la saisie utilisateur pour la création d'un collaborateur
#     with patch('rich.prompt.Prompt.ask', side_effect=[
#         "test_user",
#         "test_pass",
#         "Test",
#         "User",
#         "C"
#     ]):
#         collaborator_data = MenuView.display_create_collaborator_menu()
#         assert collaborator_data == {
#             "username": "test_user",
#             "password": "test_pass",
#             "first_name": "Test",
#             "last_name": "User",
#             "role": "C"
#         }
#         print("Création de collaborateur simulée et vérifiée avec succès.")
#
# # TODO " Tester le login en utilisant les données de test du collaborateur créer plus haut et
# #  utiliser un moyen de mocker le toekn lors du et_password +
# #  verifier dans pgadmin si le password du collaborateur de test dans la db de test est bien hashé et non visible sous sa forme veritable
# #  Imiter la logique du login afin de parvenir au menu du role du collaborateur de test"
#
#
# # Test de la vue simple du login, avec des valeurs inexistante car aucun appel a la db n'est faite
# # def test_display_login_menu():
# #     with patch('rich.prompt.Prompt.ask', side_effect=["test_user", "test_password"]):
# #         username, password = MenuView.display_login_menu()
# #
# #     assert username == "test_user"
# #     assert password == "test_password"
#
#
# # def test_login_collaborator():
# #     # Données du collaborateur de test
# #     mock_collaborator_data = {
# #         "username": "test_commercial_user",
# #         "password": "1234"
# #     }
# #
# #     # Simuler l'affichage du menu de connexion avec les données du collaborateur de test
# #     with patch('collaborator_app.view.MenuView.display_login_menu',
# #                return_value=mock_collaborator_data) as mock_display_login_menu:
# #         # Exécuter MainController.run()
# #         MainController.run()
# #
# #         # Vérifier que display_login_menu a été appelé une fois
# #         mock_display_login_menu.assert_called_once()
#
#
# def test_create_and_verify_password(test_db):
#     """Verifier le mot de passe brut saisie de celui stocké dans la db de test et hashé"""
#     # Supprimer le collaborateur s'il existe déjà
#     Collaborator.delete().where(Collaborator.username == 'test_commercial_user').execute()
#
#     # Création du collaborateur de test
#     mock_collaborator_data = {
#         "username": "test_commercial_user",
#         "password": "1234",
#         "first_name": "test_toto_commercial",
#         "last_name": "test_user_toto",
#         "role": "C"
#     }
#
#     with patch('collaborator_app.view.MenuView.display_create_collaborator_menu',
#                return_value=mock_collaborator_data):
#         MainController.create_first_collaborator()
#
#     # Récupérer le collaborateur depuis la base de données
#     commercial_collaborator = Collaborator.get(Collaborator.username == 'test_commercial_user')
#
#     # Verifier si la corrélation de l'utilisateur test correspond aux données présente dans la db de test
#     assert commercial_collaborator is not None
#     print(f"Assertion: commercial_collaborator is not None (username: {commercial_collaborator.username})")
#     assert commercial_collaborator.first_name == 'test_toto_commercial'
#     print(f"Assertion: {commercial_collaborator.first_name}")
#     assert commercial_collaborator.last_name == 'test_user_toto'
#     print(f"Assertion: {commercial_collaborator.last_name})")
#     assert commercial_collaborator.role == 'C'
#     print(f"Assertion: commercial_collaborator.role :{commercial_collaborator.role}")
#     # Vérifier que le mot de passe est bien hashé et non en clair
#     assert commercial_collaborator.password != "1234"
#     print(f"Assertion: {commercial_collaborator.password}")
#     # Vérifier que le mot de passe hashé correspond au mot de passe brut
#     is_password_verified = commercial_collaborator.verify_password("1234")
#     assert is_password_verified
#     print(f"Assertion: commercial_collaborator.verify_password('1234')")
#     # Afficher les hashs pour comparaison visuelle
#     print(f"Mot de passe brut: 1234")
#     print(f"Hashed password: {commercial_collaborator.password}")
#     # Vérifier que la corrélation des données entre le mot de passe brut et le mot de passe stocké est correcte
#     assert commercial_collaborator.password != "1234" and is_password_verified
#     print(f"Assertion: Correlation entre le mot de passe saisie et le mot de stocké est correcte")
#
#     print("Le mot de passe est correctement hashé et vérifié.")
#
#
# def test_login_collaborator(test_db):
#     # Supprimer le collaborateur s'il existe déjà pour avoir un état initial propre
#     Collaborator.delete().where(Collaborator.username == 'test_commercial_user').execute()
#
#     # Créer un collaborateur pour le test de connexion
#     mock_collaborator_data = {
#         "username": "test_commercial_user",
#         "password": "1234",
#         "first_name": "test_toto_commercial",
#         "last_name": "test_user_toto",
#         "role": "C"
#     }
#
#     with patch('collaborator_app.view.MenuView.display_create_collaborator_menu',
#                return_value=mock_collaborator_data):
#         MainController.create_first_collaborator()
#
#     # Simuler la saisie utilisateur pour la connexion
#     with patch('collaborator_app.view.MenuView.display_login_menu',
#                return_value=(mock_collaborator_data["username"], mock_collaborator_data["password"])):
#         login_username, login_password = MenuView.display_login_menu()
#
#         # Vérifier les informations de connexion
#         commercial_collaborator = Collaborator.get(Collaborator.username == login_username)
#         is_password_verified = commercial_collaborator.verify_password(login_password)
#
#         assert commercial_collaborator is not None
#         print(f"Assertion: commercial_collaborator n'est pas None (username: {commercial_collaborator.username})")
#
#         assert is_password_verified
#         print(f"Assertion: Mot de passe verifié pour l'utilisateur: {login_username}")
#
#         # Afficher les hashs pour comparaison visuelle
#         print(f"Mot de passe saisie: {login_password}")
#         print(f"Mot de passe hashé: {commercial_collaborator.password}")
#
#         print("Connexion utilisateur réussie et vérifiée.")
