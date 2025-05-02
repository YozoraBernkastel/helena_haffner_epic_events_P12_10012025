from models.db_models import Customer
from tests.mock import TO_CREATE_CUSTOMER, CUSTOMER_1, CUSTOMER_1_NEW_NAME, UNKNOWN_MAIL


def test_customer_interactions(monkeypatch, sales_controller):
    input_values: list = (list(TO_CREATE_CUSTOMER.values()) +
                          [TO_CREATE_CUSTOMER["mail"], TO_CREATE_CUSTOMER["mail"]])

    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))
    sales_controller.customer_creation()

    new_customer = sales_controller.find_customer(sales_controller.user)
    assert isinstance(new_customer, Customer)
    assert new_customer.mail == TO_CREATE_CUSTOMER["mail"]

    sales_controller.delete_customer()
    assert Customer.get_or_none(mail=TO_CREATE_CUSTOMER["mail"]) is None


def test_customer_modification_detail(sales_controller, monkeypatch):
    input_values: list = ["1", CUSTOMER_1_NEW_NAME]
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))

    customer = Customer.get_or_none(mail=CUSTOMER_1["mail"])
    assert isinstance(customer, Customer)
    assert customer.full_name == CUSTOMER_1["fullname"]
    assert customer.full_name != CUSTOMER_1_NEW_NAME

    # sales_controller.customer_modification_detail(customer)
    # customer = Customer.get_or_none(mail=CUSTOMER_1["mail"])
    # assert isinstance(customer, Customer)
    # assert customer.mail == CUSTOMER_1["mail"]
    # assert customer.full_name == CUSTOMER_1_NEW_NAME
    #
    # sales_controller.delete_customer()
    # assert Customer.get_or_none(mail=UNKNOWN_MAIL) is None
