from datetime import datetime
from xmlrpc.client import DateTime
from peewee import ModelSelect

from settings.settings import SUPPORT
from view.sales_view import SalesView as View
from models.db_models import Collaborator, Customer, Event, Contract
from control.generic_controller import GenericController


class SalesController(GenericController):
    def __init__(self, user: Collaborator):
        self.user: Collaborator = user

    def my_customers_list(self) -> None:
        my_customers_list = Customer.select().where(Customer.collaborator == self.user).execute()
        View.display_customers_detail(my_customers_list)

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

        View.create_with_success(f"du client {customer_name}")

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

    def customer_detail_modification(self) -> None:
        customer = self.find_customer(collaborator=self.user)
        if self.is_quitting(customer):
            return

        self.customer_modification_detail(customer)

    def customer_detail(self) -> None:
        customer = self.find_customer(collaborator=self.user)
        if self.is_quitting(customer):
            return

        View.display_customer_detail(customer)
        customer_events: list = Event.select().where(Event.customer == customer).execute()
        [View.event_display(event) for event in customer_events]

    def delete_customer(self) -> None:
        customer = self.find_customer(collaborator=self.user)
        if self.is_quitting(customer):
            return
        customer.delete_instance()

    def customers_menu(self) -> None:
        choice = View.customer_menu()

        if choice == "1":
            self.customer_creation()
        elif choice == "2":
            self.customer_detail_modification()
        elif choice == "3":
            self.my_customers_list()
        elif choice == "4":
            self.customer_detail()
        elif choice == "5":
            self.delete_customer()
        else:
            return

    def my_contract_detail(self, my_contract_list: ModelSelect) -> None:
        while True:
            contract_name = View.asks_contract_name()
            if self.is_quitting(contract_name):
                return

            my_contract: Contract | None = None

            for contract in my_contract_list:
                if contract.name == contract_name:
                    my_contract = contract
                    break

            if my_contract is not None:
                View.contract_display(my_contract)
                return

            View.unknown_contract(contract_name)

    def contracts_menu(self) -> None:
        choice = View.sales_collab_contract_menu()
        my_contracts: ModelSelect = Contract.select().where(Contract.collaborator == self.user).execute()

        if choice == "1":
            [View.contract_display(contract) for contract in my_contracts]
        elif choice == "2":
            without_event = [contract for contract in my_contracts if Event.get_or_none(contract=contract) is None]
            [View.no_event_contract(contract) for contract in without_event]
        elif choice == "3":
            self.my_contract_detail(my_contracts)
        elif choice == "4":
            self.contract_detail_modification(self.user)
        else:
            return

    def create_specific_datetime(self, is_starting=True) -> datetime | str:
        while True:
            date, hour = View.asks_event_date(is_starting)

            if self.is_quitting(date) or self.is_quitting(hour):
                return "q"

            formated_date = self.convert_str_in_datetime(date, hour)

            if isinstance(formated_date, datetime):
                return formated_date

    def event_name(self) -> str:
        while True:
            event_name = View.asks_event_name()
            if self.is_quitting(event_name) or self.is_available_event_name(event_name):
                return event_name

    def events_creation(self) -> None:
        event_name: str = self.event_name()
        if self.is_quitting(event_name):
            return

        contract: Contract | str = self.find_contract()
        if self.is_quitting(contract):
            return

        if contract.collaborator != self.user:
            View.access_denied()
            return

        support_collab: Collaborator | str = self.find_collab(SUPPORT)
        if self.is_quitting(support_collab):
            return

        starting_date: datetime | str = self.create_specific_datetime()
        if self.is_quitting(starting_date):
            return
        ending_date: datetime | str = self.create_specific_datetime(is_starting=False)
        if self.is_quitting(ending_date):
            return

        print(starting_date)

        address: str = View.asks_event_address()
        if self.is_quitting(address):
            return

        attendant_participant = View.asks_number_of_participants()
        if self.is_quitting(attendant_participant):
            return

        comment = View.asks_info()

        Event.create(name=event_name, contract=contract, starting_time=starting_date,
                     ending_time=ending_date, support=support_collab, address=address,
                     attendant_number=attendant_participant, comment=comment)

        View.create_with_success(f"de l'événement {event_name}")

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
