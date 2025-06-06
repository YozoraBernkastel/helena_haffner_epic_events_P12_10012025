from view.generic_view import View
from models.db_models import Collaborator, Customer, Event, Contract
from settings.settings import MANAGEMENT, SALES
from datetime import datetime


class GenericController:
    """
    Virtual Controller used as parent for the other controllers.
    """

    @staticmethod
    def is_quitting(choice: any) -> bool:
        """
        Check if the user wants to quit.
        :param choice:
        :return:
        """
        return isinstance(choice, str) and choice.lower().strip() == "q"

    @staticmethod
    def is_available_username(username: str) -> bool:
        """
        Check if the username is already used.
        :param username: the wanted username
        :return: return True if the username is not already used for a collaborator.
        """
        return Collaborator.get_or_none(username=username) is None

    def choose_username_and_password(self) -> tuple[str, str]:
        """
        Asks the user to choose a valid username and a password.
        :return: the valid username and the chosen password.
        """
        while True:
            username = View.asks_username()

            if self.is_quitting(username):
                return username, username

            if self.is_available_username(username):
                break

            View.username_already_used(username)

        password: str = View.asks_collab_password()

        if self.is_quitting(password):
            return password, password

        return username, password

    @staticmethod
    def is_available_mail(new_mail: str) -> bool:
        """
        Check is the mail is already used by a Customer.
        :param new_mail: the wanted mail
        :return: bool returning True if the mail is missing in the Customer objects' list.
        """
        return Customer.get_or_none(mail=new_mail) is None

    @staticmethod
    def is_available_event_name(new_event_name: str) -> bool:
        """
        Check if the name is already used for an Event object in the database.
        :param new_event_name: the wanted name
        :return: True if the name is not used by an existing Event.
        """
        return Event.get_or_none(name=new_event_name) is None

    @staticmethod
    def is_available_contract_name(new_contract_name) -> bool:
        """
        Check if the name is already used for a Contract object in the database.
        :param new_contract_name: the wanted name
        :return: True if the name is not used by an existing contract.
        """
        return Contract.get_or_none(name=new_contract_name) is None

    @classmethod
    def new_password(cls):
        """
        asks the user a new password.
        :return: the new password or the str to quit.
        """
        while True:
            password1 = View.asks_password_template("Entrez votre nouveau mot de passe une première fois")

            if cls.is_quitting(password1):
                return password1

            password2 = View.asks_password_template("Puis une seconde fois")

            if cls.is_quitting(password2):
                return password2

            if password1 == password2:
                return password1

            View.different_passwords_prompt()

    @classmethod
    def change_password(cls, user: Collaborator) -> None:
        """
        Modify the user's password.
        :return: the new password or the str to quit.
        """
        if not View.wants_to_change_password():
            return

        actual_password = View.asks_actual_password()
        if Collaborator.find_collaborator(username=user.username, password=actual_password):
            new_password = cls.new_password()

            if not cls.is_quitting(new_password):
                user.update_password(new_password)
                View.password_updated()
                return
        else:
            View.bad_password()

        View.modification_canceled()

    @classmethod
    def account_menu(cls, user):
        """
        Account Menu.
        :param user: the Collaborator's object corresponding to the user.
        :return:
        """
        cls.change_password(user)

    def customer_collaborator_modification(self, customer) -> None:
        """
        Change the collaborator linked to the customer in argument.
        :param customer: Customer object
        :return:
        """
        collab_name = View.asks_username(complete=f"auquel donner le client {customer.full_name}")

        if self.is_quitting(collab_name):
            View.modification_canceled()
            return

        collaborator = Collaborator.get_or_none(username=collab_name, role=SALES)

        if collaborator is None:
            View.unknown_sales_collaborator(collab_name)
            return

        customer.change_collab(collaborator)
        View.modification_done()

    @staticmethod
    def convert_str_in_datetime(date_str: str, hour_str: str) -> datetime | None:
        """
        Convert two strings into a datetime object if the string have the wanted format.
        :param date_str: string corresponding to a day, month and year.
        :param hour_str: string corresponding to an hour.
        :return:
        """
        date: list = date_str.split("/")
        hour: list = hour_str.split("h")
        try:
            date = [int(num) for num in date]
            hour = [int(num) for num in hour]
            return datetime(date[2], date[1], date[0], hour[0], hour[1])
        except Exception:
            print("Cette date n'existe pas.")
            return None

    @classmethod
    def find_contract(cls) -> Contract | str:
        """
        Find a Contract object in the database based on its name.
        :return: the Contract object or the string corresponding to the quit option.
        """
        while True:
            contract_name = View.asks_contract_name()
            if cls.is_quitting(contract_name):
                return contract_name

            contract = Contract.get_or_none(name=contract_name)
            if isinstance(contract, Contract):
                return contract

            View.unknown_contract(contract_name)

    @staticmethod
    def all_collab_list():
        """
        Display a list of all the collaborators.
        :return:
        """
        all_collaborators = Collaborator.select()
        [View.collab_display(collab) for collab in all_collaborators]

    @staticmethod
    def all_customers_list():
        """
        Display a list of all the customers.
        :return:
        """
        all_customers = Customer.select()
        View.display_customers_detail(all_customers)

    @staticmethod
    def all_contracts_list():
        """
        Display a list of all the contracts.
        :return:
        """
        all_contracts = Contract.select()
        [View.contract_display(contract) for contract in all_contracts]

    @staticmethod
    def all_events_list():
        """
        Display a list of all the events.
        :return:
        """
        all_events = Event.select()
        [View.event_display(event) for event in all_events]

    @classmethod
    def change_contract_collaborator(cls, contract_name: str) -> Collaborator | str:
        """
        Change the Collaborator of a Contract
        :param contract_name: name of the contract
        :return:
        """
        while True:
            collab_username = View.asks_username(f"qui s'occupera désormais du contrat {contract_name}")
            if cls.is_quitting(collab_username):
                return collab_username

            collab: Collaborator | None = Collaborator.get_or_none(username=collab_username)
            if collab is not None and collab.role == SALES:
                return collab

            View.unknown_sales_collaborator(collab_username)

    @classmethod
    def contract_detail_modification(cls, collaborator: Collaborator) -> None:
        """
        Change a value of a contract.
        :param collaborator:
        :return:
        """
        contract: Contract | str = cls.find_contract()
        if cls.is_quitting(contract):
            return

        if contract.collaborator != collaborator and collaborator.role != MANAGEMENT:
            View.access_denied()
            return

        View.contract_display(contract)
        choice = View.contract_modification_prompt(collaborator.role, contract.signed)

        if choice == "1":
            contract.name = View.asks_contract_new_name(contract.name)
        elif choice == "2":
            contract.remains_to_be_paid = View.update_contract_remain(contract.remains_to_be_paid)
        elif choice == "3" and not contract.signed:
            contract.signed = View.signed_contract_prompt()
        elif collaborator.role == MANAGEMENT:
            if choice == "4" and not contract.signed or choice == "3":
                collaborator = cls.change_contract_collaborator(contract.name)
                if cls.is_quitting(collaborator):
                    return
                contract.collaborator = collaborator
        else:
            return

        contract.save()
        View.modification_done()

    @staticmethod
    def choose_role_context(role: str) -> str:
        if role == MANAGEMENT:
            return "de la gestion"
        if role == SALES:
            return "du département commercial"
        return "du support"

    @classmethod
    def find_collab(cls, role: str) -> Collaborator | str:
        """
        Check if a collaborator with the wanted role exist. If it's the case, return the collaborator.
        :param role:
        :return: the wanted Collaborator or the quit str.
        """
        context = cls.choose_role_context(role)
        while True:
            collab_name: str = View.asks_username(context)
            if cls.is_quitting(collab_name):
                return collab_name

            collab = Collaborator.get_or_none(username=collab_name, role=role)
            if isinstance(collab, Collaborator):
                return collab

            View.unknown_support_collaborator(collab_name)

    @classmethod
    def find_customer(cls, collaborator: Collaborator) -> Customer | str:
        """
        Find a customer of the user in argument based on the mail.
        :param collaborator: Collaborator obj.
        :return: Customer object or quit str.
        """
        while True:
            customer_mail = View.asks_customer_mail()
            if cls.is_quitting(customer_mail):
                return customer_mail

            customer = Customer.get_or_none(mail=customer_mail, collaborator=collaborator)
            if isinstance(customer, Customer):
                return customer

            View.unknown_customer()

    @classmethod
    def find_event(cls) -> Event | str:
        """
        Find an Event corresponding to the given name.
        :return: Event obj or quit str.
        """
        while True:
            event_name = View.asks_event_name()
            if cls.is_quitting(event_name):
                return event_name

            event = Event.get_or_none(name=event_name)
            if event is not None:
                return event

            View.unknown_event()

    @classmethod
    def event_display(cls):
        """
        Display an event
        :return:
        """
        event = cls.find_event()

        if isinstance(event, Event):
            View.event_display(event)

    @staticmethod
    def add_customer_info(old_info: str = "") -> str:
        """
        Merge the string in param with a new one written by the user.
        :param old_info: string corresponding to a customer information attribute. Empty by default.
        :return:
        """
        new_info = View.add_info_prompt()
        return f"{old_info} {new_info} "

    @classmethod
    def information_modification(cls, obj: Customer | Event) -> None:
        """
        Update the attribute "information" of an object Customer or Event in the database.
        :param obj: a Customer object or an Event object.
        :return:
        """
        choice = View.info_menu()

        if choice == "1":
            obj.information = cls.add_customer_info(obj.information)
        elif choice == "2":
            obj.information = cls.add_customer_info()
        elif choice == "3":
            obj.information = ""
        else:
            return

        obj.save()
        View.modification_done()

    @classmethod
    def modify_obj(cls, obj, attribute: str, new_data: str) -> None:
        """
        Update the attribute of an object with the new data.
        :param obj: the object to update.
        :param attribute: the attribute of the object we want to update.
        :param new_data: the new value of the attribute.
        :return:
        """
        if cls.is_quitting(new_data):
            View.modification_canceled()
            return

        setattr(obj, attribute, new_data)
        if isinstance(obj, Customer):
            obj.last_update = datetime.now()
        obj.save()
        View.modification_done()

    @classmethod
    def create_specific_datetime(cls, is_starting=True) -> datetime | str:
        """
        Create a datetime object corresponding to the user's inputs.
        :param is_starting: bool to specify if the datetime is about the start or the end of an Event.
        :return:
        """
        while True:
            date, hour = View.asks_event_date(is_starting)

            if cls.is_quitting(date) or cls.is_quitting(hour):
                return "q"

            formated_date = cls.convert_str_in_datetime(date, hour)

            if isinstance(formated_date, datetime):
                return formated_date
