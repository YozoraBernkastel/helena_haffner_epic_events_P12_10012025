from view.sales_view import SalesView as View
from models.db_models import Collaborator, Customer
from control.generic_controller import GenericController


class SalesController(GenericController):
    def __init__(self, user: Collaborator):
        self.user: Collaborator = user

    def my_customers_list(self) -> None:
        my_customers_list = Customer.select().where(Customer.collaborator == self.user).execute()
        [print(f"Client : {customer.full_name} - mail : {customer.mail} - entreprise : {customer.company_name}")
         for customer in my_customers_list]
        print()

    def customer_creation(self):
        is_mail_already_use: bool = True
        customer_mail: str = ""

        while is_mail_already_use:
            customer_mail = View.asks_customer_mail()

            if self.is_quitting(customer_mail):
                return

            if self.is_available_mail(customer_mail):
                break
            View.mail_already_used(customer_mail)

        customer_name = View.new_customer_name()
        if self.is_quitting(customer_name):
            return

        customer_company = View.new_customer_company()
        if self.is_quitting(customer_company):
            return

        customer_phone = View.asks_customer_phone_number()
        if self.is_quitting(customer_phone):
            return

        information = View.asks_info()

        Customer.create(full_name=customer_name, mail=customer_mail, phone=customer_phone,
                        company_name=customer_company, collaborator=self.user, information=information)

    def modify_customer(self, customer: Customer, attribute: str, new_data: str) -> None:
        if self.is_quitting(new_data):
            View.modification_canceled()
            return

        setattr(customer, attribute, new_data)
        customer.save()
        View.modification_done()

    def customer_modification_detail(self, customer: Customer):
        choice = View.customer_modification_menu(customer.full_name)

        if choice == "1":
            new_name = View.rename_customer_prompt(customer.full_name)
            self.modify_customer(customer, "full_name", new_name)
        elif choice == "2":
            new_mail = View.new_mail_customer_prompt(customer.full_name)
            self.modify_customer(customer, "mail", new_mail)
        elif choice == "3":
            new_phone = View.new_phone_customer_prompt(customer.full_name)
            self.modify_customer(customer, "phone", new_phone)
        elif choice == "4":
            new_company_name = View.new_company_prompt(customer.full_name)
            self.modify_customer(customer, "company_name", new_company_name)
        elif choice == "5":
            self.customer_collaborator_modification(customer)
        else:
            return

    def customer_modification(self) -> None:
        customer_mail = View.asks_customer_mail()

        if self.is_quitting(customer_mail):
            return

        customer = Customer.get_or_none(mail=customer_mail, collaborator=self.user)

        if customer is None:
            View.unknown_customer()
            return
        self.customer_modification_detail(customer)

    def customers_menu(self) -> None:
        choice = View.customer_menu()

        if choice == "1":
            self.customer_creation()
        elif choice == "2":
            self.customer_modification()
        elif choice == "3":
            self.my_customers_list()
        else:
            return

    def contracts_menu(self) -> None:
        pass

    def events_menu(self) -> None:
        pass

    def home_menu(self) -> None:
        while True:
            choice = View.menu()

            if choice == "1":
                self.customers_menu()
            elif choice == "2":
                self.contracts_menu()
            elif choice == "3":
                self.events_menu()
            elif choice == "4":
                self.account_menu(self.user)
            else:
                return

