from datetime import datetime
from settings.settings import SUPPORT
from view.sales_view import SalesView as View
from models.db_models import Collaborator, Customer, Event, Contract
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

    @staticmethod
    def add_customer_info(customer: Customer, old_info: str = "") -> None:
        new_info = View.add_customer_info_prompt(customer)
        customer.information = f"{old_info}{new_info}"
        customer.save()
        View.modification_done()

    def information_modification(self, customer: Customer) -> None:
        choice = View.customer_info_menu()

        if choice == "1":
            old_info = f"{customer.information}\n" if len(customer.information) > 0 else ""
            self.add_customer_info(customer, old_info)
        elif choice == "2":
            self.add_customer_info(customer)
        elif choice == "3":
            customer.information = ""
            customer.save()
            View.modification_done()
        else:
            return

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
        elif choice == "6":
            self.information_modification(customer)
            pass
        else:
            return

    def customer_detail(self, modification=False) -> None:
        customer_mail = View.asks_customer_mail()

        if self.is_quitting(customer_mail):
            return

        customer = Customer.get_or_none(mail=customer_mail, collaborator=self.user)

        if customer is None:
            View.unknown_customer()
            return

        if modification:
            self.customer_modification_detail(customer)
        else:
            View.display_customer_detail(customer)
            customer_events: list = Event.select().where(Event.customer == customer).execute()
            [View.event_display(event) for event in customer_events]

    def customers_menu(self) -> None:
        choice = View.customer_menu()

        if choice == "1":
            self.customer_creation()
        elif choice == "2":
            self.customer_detail(modification=True)
        elif choice == "3":
            self.my_customers_list()
        elif choice == "4":
            self.customer_detail()
        else:
            return

    def contracts_menu(self) -> None:
        pass

    def create_specific_datetime(self, is_starting=True) -> datetime | str:
        while True:
            date, hour = View.asks_event_date(is_starting)

            if self.is_quitting(date) or self.is_quitting(hour):
                return "q"

            formated_date = self.convert_str_in_datetime(date, hour)

            if isinstance(formated_date, datetime):
                return formated_date

    def events_creation(self) -> None:
        while True:
            event_name = View.asks_event_name()
            if self.is_quitting(event_name):
                return
            if self.is_available_event_name(event_name):
                break

        while True:
            contract_name = View.asks_contract_name()
            if self.is_quitting(contract_name):
                return
            contract = Contract.get_or_none(name=contract_name)
            if isinstance(contract, Contract):
                break

        while True:
            customer_mail = View.asks_customer_mail()
            if self.is_quitting(customer_mail):
                return
            if not self.is_available_mail(customer_mail):
                customer = Customer.get_or_none(mail=customer_mail)
                break

        while True:
            support_name: str = View.asks_username("appartenant au support")
            if self.is_quitting(support_name):
                return

            support_collab = Collaborator.get_or_none(username=support_name, role=SUPPORT)
            if isinstance(support_collab, Collaborator):
                break

        starting_date = self.create_specific_datetime()
        if self.is_quitting(starting_date):
            return
        ending_date = self.create_specific_datetime(is_starting=False)
        if self.is_quitting(ending_date):
            return

        address = View.asks_event_address()
        if self.is_quitting(address):
            return

        while True:
            attendant_participant = View.asks_number_of_participants()
            if self.is_quitting(attendant_participant):
                return
            if attendant_participant.isdigit():
                attendant_participant = int(attendant_participant)
                break

        comment = View.asks_info()

        Event.create(name=event_name, contract=contract, customer=customer, starting_date=starting_date,
                     ending_date=ending_date, support=support_collab, address=address,
                     attendant_participant=attendant_participant, comment=comment)

    def home_menu(self) -> None:
        while True:
            choice = View.menu()

            if choice == "1":
                self.customers_menu()
            elif choice == "2":
                self.contracts_menu()
            elif choice == "3":
                self.events_creation()
            elif choice == "4":
                self.account_menu(self.user)
            else:
                return
