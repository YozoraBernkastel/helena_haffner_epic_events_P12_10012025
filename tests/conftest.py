import pytest
from peewee import SqliteDatabase
from models.db_models import Collaborator, Customer, Contract, Event
from settings.settings import MANAGEMENT, SUPPORT, SALES
from tests.mock import MANAGEMENT_USER1, SALES_USER1, SUPPORT_USER1


MODELS = [Collaborator, Customer, Contract, Event]

# create a temporary database for tests
@pytest.fixture(scope="session")
def db_connection():
    test_db = SqliteDatabase(':memory:')
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

    test_db.connect()
    test_db.create_tables(MODELS)

    Collaborator.create_collab(username=MANAGEMENT_USER1, password=MANAGEMENT_USER1, role=MANAGEMENT)
    Collaborator.create_collab(username=SALES_USER1, password=SALES_USER1, role=SALES)
    Collaborator.create_collab(username=SUPPORT_USER1, password=SUPPORT_USER1, role=SUPPORT)

    yield test_db

    test_db.close()


