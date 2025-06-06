from control.generic_controller import GenericController
from models.db_models import Collaborator, Customer, Contract, Event
from settings.settings import ROLES_LIST, MANAGEMENT
from tests.mock import (q, MANAGEMENT_1, UNKNOWN_USERNAME, CUSTOMER_1, UNKNOWN_MAIL, CONTRACT_1, UNKNOWN_CONTRACT_NAME,
                        EVENT_1, UNKNOWN_EVENT_NAME, SALES_1, SUPPORT_1, CUSTOMER_1_NEW_NAME)


def test_is_quitting():
    assert GenericController.is_quitting("q")
    assert not GenericController.is_quitting("a")


def test_is_available_username():
    assert GenericController.is_available_username(UNKNOWN_USERNAME)
    assert not GenericController.is_available_username(MANAGEMENT_1["username"])


def test_is_available_mail():
    assert GenericController.is_available_mail(UNKNOWN_MAIL)
    assert not GenericController.is_available_mail(CUSTOMER_1["mail"])


def test_is_available_contract_name():
    assert GenericController.is_available_contract_name(UNKNOWN_CONTRACT_NAME)
    assert not GenericController.is_available_contract_name(CONTRACT_1["name"])


def test_is_available_event_name():
    assert GenericController.is_available_event_name(UNKNOWN_EVENT_NAME)
    assert not GenericController.is_available_event_name(EVENT_1["name"])


def test_convert_str_in_datetime():
    assert GenericController.convert_str_in_datetime("12/12/2026", "9h32") is not None
    assert GenericController.convert_str_in_datetime("autre chose", "9h32") is None
    assert GenericController.convert_str_in_datetime("12/12/2026", "autre chose") is None


def test_find_collab(monkeypatch):
    collaborators_names: list = [MANAGEMENT_1["username"], SUPPORT_1["username"], SALES_1["username"]]

    for collaborator, role in zip(collaborators_names, ROLES_LIST):
        monkeypatch.setattr('builtins.input', lambda _: collaborator)
        collab = GenericController.find_collab(role)
        assert isinstance(collab, Collaborator)

    monkeypatch.setattr('builtins.input', lambda _: q)
    collab = GenericController.find_collab(MANAGEMENT)
    assert collab == q


def test_find_customer(monkeypatch):
    salesman = Collaborator.get(username=SALES_1["username"])
    monkeypatch.setattr('builtins.input', lambda _: CUSTOMER_1["mail"])
    customer = GenericController.find_customer(salesman)
    assert isinstance(customer, Customer)

    monkeypatch.setattr('builtins.input', lambda _: q)
    customer = GenericController.find_customer(salesman)
    assert customer == q


def test_find_contract(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: CONTRACT_1["name"])
    contract = GenericController.find_contract()
    assert isinstance(contract, Contract)

    monkeypatch.setattr('builtins.input', lambda _: q)
    contract = GenericController.find_contract()
    assert contract == q


def test_find_event(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: EVENT_1["name"])
    event = GenericController.find_event()
    assert isinstance(event, Event)

    monkeypatch.setattr('builtins.input', lambda _: q)
    event = GenericController.find_event()
    assert event == q


def test_modify_obj():
    customer = Customer.get(mail=CUSTOMER_1["mail"])
    GenericController.modify_obj(customer, "full_name", CUSTOMER_1_NEW_NAME)
    modified_customer: Customer = Customer.get(mail=CUSTOMER_1["mail"])

    assert customer.full_name == CUSTOMER_1_NEW_NAME
    assert modified_customer.full_name == CUSTOMER_1_NEW_NAME
