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
1

@pytest.fixture
def session_user_support(*args, **kwargs):
    from utils import generate_collaborator
    Session.user = generate_collaborator(role=Collaborator.SUPPORT)




