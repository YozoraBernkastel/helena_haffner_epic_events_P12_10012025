from view.unwanted_view import UnwantedView
from tests.mock import CONTRACT_1, MANAGEMENT_1, UNKNOWN_MAIL


def test_unknown_user_or_password():
    UnwantedView.unknown_user_or_password()


def test_unknown_customer():
    UnwantedView.unknown_customer()


def test_unknown_event():
    UnwantedView.unknown_event()


def test_unknown_contract():
    UnwantedView.unknown_contract(CONTRACT_1["name"])


def test_access_denied():
    UnwantedView.access_denied()


def test_bad_password() -> None:
    UnwantedView.bad_password()


def test_already_used_prompt():
    UnwantedView.already_used_prompt("La catégorie", "portant ce nom", True)


def test_username_already_used():
    UnwantedView.username_already_used(MANAGEMENT_1["username"])


def test_missing_collaborator():
    UnwantedView.missing_collaborator(MANAGEMENT_1["username"])


def test_mail_already_used():
    UnwantedView.mail_already_used(UNKNOWN_MAIL)


def test_unknown_option():
    UnwantedView.unknown_option()


def test_error_price():
    assert UnwantedView.error_price() == -1.00


def test_different_passwords_prompt():
    UnwantedView.different_passwords_prompt()


def test_modification_canceled():
    UnwantedView.modification_canceled()


def test_unknown_sales_collaborator():
    UnwantedView.unknown_sales_collaborator(MANAGEMENT_1["username"])


def test_unknown_support_collaborator():
    UnwantedView.unknown_support_collaborator(MANAGEMENT_1["username"])


def test_cannot_delete_own_account():
    UnwantedView.cannot_delete_own_account()
