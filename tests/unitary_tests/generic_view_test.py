from view.generic_view import View
from settings.settings import ROLES_LIST
from tests.mock import question

def test_yes_or_no_choice(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    assert View.yes_or_no_choice()

    monkeypatch.setattr('builtins.input', lambda _: "oui")
    assert View.yes_or_no_choice()

    monkeypatch.setattr('builtins.input', lambda _: "2")
    assert not View.yes_or_no_choice()

    monkeypatch.setattr('builtins.input', lambda _: "azerty")
    assert not View.yes_or_no_choice()


def test_is_choice_valid():
    max_range: int = 3

    assert View.is_choice_valid(str(max_range - 1), max_range)
    assert View.is_choice_valid(str(max_range), max_range)
    assert View.is_choice_valid("q", max_range)
    assert View.is_choice_valid("Q", max_range)

    assert not View.is_choice_valid(str(max_range + 1), max_range)
    assert not View.is_choice_valid("0", max_range)
    assert not View.is_choice_valid("-2", max_range)
    assert not View.is_choice_valid("azerty", max_range)

def test_choice_loop(monkeypatch):
    user_input: str = str(len(ROLES_LIST))
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    assert View.choice_loop(question, ROLES_LIST) == user_input

def test_check_price_validity():
    int_format_price: str = "12"
    valid_price = View.check_price_validity(int_format_price)
    assert isinstance(valid_price, float)
    assert valid_price == float(int_format_price)

    dot_format_price: str = "12.12"
    valid_price = View.check_price_validity(dot_format_price)
    assert isinstance(valid_price, float)
    assert valid_price == float(dot_format_price)

    comma_format_price: str = "12,12"
    valid_price = View.check_price_validity(comma_format_price)
    assert isinstance(valid_price, float)
    assert valid_price == float(dot_format_price)

    not_a_price: str = "azerty"
    invalid_price = View.check_price_validity(not_a_price)
    assert isinstance(valid_price, float)
    assert invalid_price == View.error_price()

def test_update_contract_remain(monkeypatch):
    remain_to_paid: float = 99.66
    monkeypatch.setattr('builtins.input', lambda _: str(remain_to_paid))
    assert View.update_contract_remain(remain_to_paid) == remain_to_paid

    remain_to_paid: float = 0.00
    assert View.update_contract_remain(remain_to_paid) == remain_to_paid
