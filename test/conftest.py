import pytest
from peewee import SqliteDatabase

from client_app.model import Client
from collaborator_app.model import Collaborator
from contract_app.model import Contract
from event_app.model import Event
from services.utils import Session


MODELS = [Collaborator, Client, Contract, Event]
test_db = SqliteDatabase(':memory:')


@pytest.fixture(scope="session")
def test_track():
    print("début")
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    test_db.connect()
    test_db.create_tables(MODELS)
    yield
    print("fin de test")


@pytest.fixture
def session_user_commercial(*args, **kwargs):
    from utils import generate_collaborator
    Session.user = generate_collaborator(role=Collaborator.COMMERCIAL)


@pytest.fixture
def session_user_gestion(*args, **kwargs):
    from utils import generate_collaborator
    Session.user = generate_collaborator(role=Collaborator.GESTION)


@pytest.fixture
def session_user_support(*args, **kwargs):
    from utils import generate_collaborator
    Session.user = generate_collaborator(role=Collaborator.SUPPORT)


# def create_test_database():
#     print('-' * 80)
#     try:
#         db_admin = PostgresqlDatabase('postgres',
#                                       user=ADMIN_USER,
#                                       password=DATABASE_TEST_PASSWORD,
#                                       host=DATABASE_TEST_HOST)
#         db_admin.connect()
#         print("Connexion réussie à PostgreSQL en tant qu'utilisateur 'postgres'.")
#     except Exception as e:
#         print(f"Erreur lors de la connexion à la base de données 'postgres' : {e}")
#         return
#
#     try:
#         db_exists = db_admin.execute_sql(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_TEST_NAME}'").fetchone()
#         if not db_exists:
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
#         db_test.init(DATABASE_TEST_NAME, user=ADMIN_USER, password=DATABASE_TEST_PASSWORD, host=DATABASE_TEST_HOST)
#         db_test.connect()
#         print(f"Connexion réussie à la base de données '{DATABASE_TEST_NAME}' en tant qu'utilisateur '{ADMIN_USER}'.")
#
#         db_test.execute_sql("ALTER SCHEMA public OWNER TO postgres;")
#         print("Le propriétaire du schéma public a été modifié en 'postgres'.")
#
#         db_test.execute_sql(f"GRANT CREATE ON SCHEMA public TO {DATABASE_TEST_USER};")
#         print(f"Autorisation de création accordée à l'utilisateur {DATABASE_TEST_USER} pour le schéma public.")
#     except ProgrammingError as e:
#         print(f"Erreur lors de la configuration des privilèges : {e}")
#     finally:
#         db_test.close()

# @pytest.fixture(scope='session')
# def test_db():
#     print("debut du test")
#     create_test_database()
#
#     db_test.init(DATABASE_TEST_NAME, user=DATABASE_TEST_USER, password=DATABASE_TEST_PASSWORD, host=DATABASE_TEST_HOST)
#     db_test.connect()
#     print("Connexion réussie à la base de données de test en tant qu'utilisateur 'user_collaborator'.")
#     db_test.bind([Collaborator, Client, Contract, Event])
#
#     db_test.create_tables([Collaborator, Client, Contract, Event])
#     print(f"Création de la Table {Collaborator._meta.table_name}, pour la db de test {db_test.database}")
#     print(f"Création de la Table {Client._meta.table_name}, pour la db de test {db_test.database}")
#     print(f"Création de la Table {Contract._meta.table_name}, pour la db de test {db_test.database}")
#     print(f"Création de la Table {Event._meta.table_name}, pour la db de test {db_test.database}")
#
#     cursor = db_test.execute_sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
#     tables = cursor.fetchall()
#     print("Tables dans la base de données de test:")
#     for table in tables:
#         print(table)
#
#     yield test_db
#     print("fin du test")
#     print(f"Fermeture de la connexion à la db de test {db_test.database}:{db_test.close()})")



