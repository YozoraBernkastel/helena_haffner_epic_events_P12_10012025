from control.generic_controller import GenericController
from models.db_models import Contract
from tests.conftest import db_connection
from tests.mock import (MANAGEMENT_1, UNKNOWN_USERNAME, CUSTOMER_1, UNKNOWN_MAIL, CONTRACT_1, UNKNOWN_CONTRACT_NAME,
                        EVENT_1, UNKNOWN_EVENT_NAME)



def test_is_quitting():
    assert GenericController.is_quitting("q")
    assert not GenericController.is_quitting("a")

def test_is_available_username(db_connection):
    assert GenericController.is_available_username(UNKNOWN_USERNAME)
    assert not GenericController.is_available_username(MANAGEMENT_1["username"])

def test_is_available_mail(db_connection):
    assert GenericController.is_available_mail(UNKNOWN_MAIL)
    assert not GenericController.is_available_mail(CUSTOMER_1["mail"])

def test_is_available_contract_name(db_connection):
    assert GenericController.is_available_contract_name(UNKNOWN_CONTRACT_NAME)
    assert not GenericController.is_available_contract_name(CONTRACT_1["name"])

def test_is_available_event_name(db_connection):
    assert GenericController.is_available_event_name(UNKNOWN_EVENT_NAME)
    assert not GenericController.is_available_event_name(EVENT_1["name"])


def test_convert_str_in_datetime():
    assert GenericController.convert_str_in_datetime("12/12/2026", "9h32") is not None
    assert GenericController.convert_str_in_datetime("autre chose", "9h32") is None
    assert GenericController.convert_str_in_datetime("12/12/2026", "autre chose") is None

def test_find_contract(db_connection, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: CONTRACT_1["name"])
    contract = GenericController.find_contract()
    assert isinstance(contract, Contract)

    monkeypatch.setattr('builtins.input', lambda _: "q")
    contract = GenericController.find_contract()
    assert contract == "q"
