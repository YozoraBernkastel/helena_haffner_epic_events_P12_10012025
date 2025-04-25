import pytest
from peewee import SqliteDatabase
from control.management_controller import ManagementController
from models.db_models import Collaborator, Customer, Contract, Event
from tests.mock import MANAGEMENT_1, SALES_1, SUPPORT_1, TO_CHANGE_COLLAB, CUSTOMER_1, CONTRACT_1, EVENT_1

MODELS = [Collaborator, Customer, Contract, Event]


def collaborators_setup():
    Collaborator.create_collab(username=MANAGEMENT_1["username"], password=MANAGEMENT_1["password"],
                               role=MANAGEMENT_1["role"])
    Collaborator.create_collab(username=SALES_1["username"], password=SALES_1["password"], role=SALES_1["role"])
    Collaborator.create_collab(username=SUPPORT_1["username"], password=SUPPORT_1["password"], role=SUPPORT_1["role"])
    Collaborator.create_collab(username=TO_CHANGE_COLLAB["username"], password=TO_CHANGE_COLLAB["password"],
                               role=TO_CHANGE_COLLAB["role"])


def customers_setup():
    collab_1: Collaborator = Collaborator.get(username=SALES_1["username"])

    Customer.create(full_name=CUSTOMER_1["fullname"], mail=CUSTOMER_1["mail"], phone=CUSTOMER_1["phone"],
                    company_name=CUSTOMER_1["company_name"], information=CUSTOMER_1["information"],
                    collaborator=collab_1)


def contrats_setup():
    collab_1: Collaborator = Collaborator.get(username=SALES_1["username"])
    customer_1: Customer = Customer.get(mail=CUSTOMER_1["mail"])

    Contract.create(name=CONTRACT_1["name"], customer=customer_1, collaborator=collab_1,
                    total_value=CONTRACT_1["total"], remains_to_be_paid=CONTRACT_1["total"])


def events_setup():
    contract_1: Contract = Contract.get(name=CONTRACT_1["name"])
    support_1: Collaborator = Collaborator.get(username=SUPPORT_1["username"])

    Event.create(name=EVENT_1["name"], contract=contract_1, starting_time=EVENT_1["start"],
                 ending_time=EVENT_1["end"], support=support_1, address=EVENT_1["address"],
                 attendant_number=EVENT_1["attendant"], information=EVENT_1["information"])


def objects_setup():
    collaborators_setup()
    customers_setup()
    contrats_setup()
    events_setup()

# create a temporary database for tests
@pytest.fixture(scope="session")
def db_connection():
    test_db = SqliteDatabase(':memory:')
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

    test_db.connect()
    test_db.create_tables(MODELS)
    objects_setup()

    yield test_db

    test_db.close()

@pytest.fixture()
def management_controller():
    user: Collaborator = Collaborator.get(username=MANAGEMENT_1["username"])
    yield ManagementController(user)