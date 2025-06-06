from datetime import datetime
from peewee import ModelSelect
from settings.settings import SUPPORT
from view.role_views.sales_view import SalesView as View
from models.db_models import Collaborator, Customer, Event, Contract
from control.generic_controller import GenericController


class SalesController(GenericController):
    """
    Controller class use if the user is a seller
    """

    def __init__(self, user: Collaborator):
        self.user: Collaborator = user

    def my_customers_list(self) -> None:
        """
        Display list of the user's Customers.
        :return:
        """
        my_customers_list = Customer.select().where(Customer.collaborator == self.user).execute()
        View.display_customers_detail(my_customers_list)

    def customer_creation(self):
        """
        Create a customer which will be assigned to the user. The mail need to be unique in the database.
        :return:
        """
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

    def customer_modification_detail(self, customer: Customer):
        """
        Update an attribue of a Customer object.
        :param customer: Customer object.
        :return:
        """
        choice = View.customer_modification_menu(customer.full_name)

        if choice == "1":
            new_name = View.rename_customer_prompt(customer.full_name)
            self.modify_obj(customer, "full_name", new_name)
        elif choice == "2":
            new_mail = View.new_mail_customer_prompt(customer.full_name)
            self.modify_obj(customer, "mail", new_mail)
        elif choice == "3":
            new_phone = View.new_phone_customer_prompt(customer.full_name)
            self.modify_obj(customer, "phone", new_phone)
        elif choice == "4":
            new_company_name = View.new_company_prompt(customer.full_name)
            self.modify_obj(customer, "company_name", new_company_name)
        elif choice == "5":
            self.customer_collaborator_modification(customer)
        elif choice == "6":
            self.information_modification(customer)
        else:
            return

    def customer_detail_modification(self) -> None:
        """
        Find the wanted customer. If the input correspond to the quit string, return,
         else go to the customer modification detail menu.
        :return:
        """
        customer = self.find_customer(collaborator=self.user)
        if self.is_quitting(customer):
            return

        self.customer_modification_detail(customer)

    @staticmethod
    def search_event(contract: Contract):
        """
        Return all the event of a given contract.
        :param contract: contract object.
        :return: a list of Event objects.
        """
        return Event.select().where(Event.contract == contract).execute()

    def customer_detail(self) -> None:
        """
        Display Customer profil and their Events.
        :return:
        """
        customer: Customer = self.find_customer(collaborator=self.user)
        if self.is_quitting(customer):
            return

        View.display_customer_detail(customer)
        customer_events: list = Event.select().join(Contract, on=(Event.contract == Contract)).where(
            Contract.customer == customer).execute()
        [View.event_display(event) for event in customer_events]

    def delete_customer(self) -> None:
        """
        Delete a Customer
        :return:
        """
        customer = self.find_customer(collaborator=self.user)
        if self.is_quitting(customer):
            return
        customer.delete_instance()

    def customers_list(self):
        """
        User choose to display all the customers or their Customers.
        :return:
        """
        choice = View.customer_choice()

        if choice == "1":
            self.all_customers_list()
        elif choice == "2":
            self.my_customers_list()
        else:
            return

    def customers_menu(self) -> None:
        """
        Menu to interact with the Customer model.
        :return:
        """
        choice = View.customer_menu()

        if choice == "1":
            self.customer_creation()
        elif choice == "2":
            self.customer_detail_modification()
        elif choice == "3":
            self.customers_list()
        elif choice == "4":
            self.customer_detail()
        elif choice == "5":
            self.delete_customer()
        else:
            return

    def my_contracts_detail(self, my_contract_list: ModelSelect) -> None:
        """
        Display all the Contracts of the user.
        :param my_contract_list: list of Contracts objects.
        :return:
        """
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
        """
        Menu to interact with the Contracts linked to the user.
        :return:
        """
        choice = View.sales_collab_contract_menu()

        if choice == "5":
            self.all_contracts_list()
        else:
            my_contracts: ModelSelect = Contract.select().where(Contract.collaborator == self.user).execute()
            if choice == "1":
                [View.contract_display(contract) for contract in my_contracts]
            elif choice == "2":
                without_event = [contract for contract in my_contracts if Event.get_or_none(contract=contract) is None]
                [View.no_event_contract(contract) for contract in without_event]
            elif choice == "3":
                self.my_contracts_detail(my_contracts)
            elif choice == "4":
                self.contract_detail_modification(self.user)
            else:
                return

    def event_name(self) -> str:
        """
        While loop used to give a name to an Event.
        :return: event_name or quit str.
        """
        while True:
            event_name = View.asks_event_name()
            if self.is_quitting(event_name) or self.is_available_event_name(event_name):
                return event_name

    def events_creation(self) -> None:
        """
        Creation of an Event.
        :return:
        """
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

        address: str = View.asks_event_address()
        if self.is_quitting(address):
            return

        attendant_participant = View.asks_number_of_participants()
        if self.is_quitting(attendant_participant):
            return

        information = View.asks_info()

        Event.create(name=event_name, contract=contract, starting_time=starting_date,
                     ending_time=ending_date, support=support_collab, address=address,
                     attendant_number=attendant_participant, information=information)

        View.create_with_success(f"de l'événement {event_name}")

    def all_events_without_support_list(self) -> None:
        """
        Display of all the Events obj which have no support (Collaborator)
        :return:
        """
        without_support_events = Event.select().join(Contract).where(
            Contract.collaborator == self.user and Event.support.is_null(True)).execute()

        if without_support_events:
            [View.event_display(event) for event in without_support_events]
            return

        View.all_event_have_support()

    def display_event(self) -> None:
        """
        Display the chosen Event details.
        :return:
        """
        event = self.find_event()
        if not self.is_quitting(event):
            View.event_display(event)

    def event_menu(self):
        """
        Menu to interact with the Event Model.
        :return:
        """
        choice = View.events_menu()

        if choice == "1":
            self.events_creation()
        elif choice == "2":
            self.all_events_list()
        elif choice == "3":
            self.all_events_without_support_list()
        elif choice == "4":
            self.display_event()
        else:
            return

    def home_menu(self) -> None:
        """
        First menu of a Collaborator identified with the role of "sales"
        :return:
        """
        while True:
            choice = View.menu()

            if choice == "1":
                self.customers_menu()
            elif choice == "2":
                self.contracts_menu()
            elif choice == "3":
                self.event_menu()
            elif choice == "4":
                self.account_menu(self.user)
            else:
                return
