from models.db_models import Customer
from tests.mock import TO_CREATE_CUSTOMER, CUSTOMER_2, CUSTOMER_1_NEW_NAME, UNKNOWN_MAIL, NEW_PHONE, NEW_COMPANY


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
    input_values: list = ["1", CUSTOMER_1_NEW_NAME, "2", UNKNOWN_MAIL, "3", NEW_PHONE, "4", NEW_COMPANY]
    monkeypatch.setattr('builtins.input', lambda _: input_values.pop(0))

    customer = Customer.get_or_none(mail=CUSTOMER_2["mail"])
    assert isinstance(customer, Customer)
    assert customer.full_name == CUSTOMER_2["fullname"]
    assert customer.full_name != CUSTOMER_1_NEW_NAME

    # Test the name modification
    sales_controller.customer_modification_detail(customer)
    customer = Customer.get_or_none(mail=CUSTOMER_2["mail"])
    assert isinstance(customer, Customer)
    assert customer.full_name == CUSTOMER_1_NEW_NAME

    # Test the mail modification
    assert customer.mail == CUSTOMER_2["mail"]
    sales_controller.customer_modification_detail(customer)
    customer = Customer.get_or_none(mail=UNKNOWN_MAIL)
    assert isinstance(customer, Customer)
    assert customer.mail == UNKNOWN_MAIL
    assert customer.mail != CUSTOMER_2["mail"]

    # Test the phone modification
    assert customer.phone == CUSTOMER_2["phone"]
    sales_controller.customer_modification_detail(customer)
    customer = Customer.get_or_none(mail=UNKNOWN_MAIL)
    assert isinstance(customer, Customer)
    assert customer.phone == NEW_PHONE
    assert customer.phone != CUSTOMER_2["phone"]

    # Test the company name modification
    assert customer.company_name == CUSTOMER_2["company_name"]
    sales_controller.customer_modification_detail(customer)
    customer = Customer.get_or_none(mail=UNKNOWN_MAIL)
    assert isinstance(customer, Customer)
    assert customer.company_name == NEW_COMPANY
    assert customer.company_name != CUSTOMER_2["company_name"]

    customer.delete_instance()
