from view.generic_view import View
from models.db_models import Collaborator, Customer, Event, Contract
from settings.settings import MANAGEMENT, SALES
from datetime import datetime


class GenericController:
    @staticmethod
    def is_quitting(choice: any) -> bool:
        return isinstance(choice, str) and choice.lower().strip() == "q"

    @staticmethod
    def is_available_username(username: str) -> bool:
        return Collaborator.get_or_none(username=username) is None

    def choose_username_and_password(self) -> tuple[str, str]:
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
        return Customer.get_or_none(mail=new_mail) is None

    @staticmethod
    def is_available_event_name(new_event_name: str) -> bool:
        return Event.get_or_none(name=new_event_name) is None

    @staticmethod
    def is_available_contract_name(new_contract_name) -> bool:
        return Contract.get_or_none(name=new_contract_name) is None

    @classmethod
    def new_password(cls):
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
        # todo à compléter avec le changement de nom d'utilisateur
        cls.change_password(user)

    def customer_collaborator_modification(self, customer) -> None:
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
        date: list = date_str.split("/")
        hour: list = hour_str.split("h")
        try:
            date = [int(num) for num in date]
            hour = [int(num) for num in hour]
            return datetime(date[2], date[1], date[0], hour[0], hour[1])
        except:
            print("Cette date n'existe pas.")
            return None

    @classmethod
    def find_contract(cls) -> Contract | str:
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
        all_collaborators = Collaborator.select()
        [View.collab_display(collab) for collab in all_collaborators]

    @staticmethod
    def all_customers_list():
        all_customers = Customer.select()
        View.display_customers_detail(all_customers)

    @staticmethod
    def all_contracts_list():
        all_contracts = Contract.select()
        [View.contract_display(contract) for contract in all_contracts]

    @staticmethod
    def all_events_list():
        all_events = Event.select()
        [View.event_display(event) for event in all_events]

    @classmethod
    def change_contract_collaborator(cls, contract_name: str) -> Collaborator | str:
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
        while True:
            event_name = View.asks_event_name()
            if cls.is_quitting(event_name):
                return event_name

            event = Event.get_or_none(name=event_name)
            if event is not None:
                return event

            View.unknown_event()

    def event_display(self):
        event = self.find_event()

        if isinstance(event, Event):
            View.event_display(event)

    @staticmethod
    def add_customer_info(old_info: str = "") -> str:
        new_info = View.add_info_prompt()
        return f"{old_info} {new_info} "

    def information_modification(self, obj: Customer | Event) -> None:
        choice = View.info_menu()

        if choice == "1":
            obj.information = self.add_customer_info(obj.information)
        elif choice == "2":
            obj.information = self.add_customer_info()
        elif choice == "3":
            obj.information = ""
        else:
            return

        obj.save()
        View.modification_done()

    def modify_obj(self, obj, attribute: str, new_data: str) -> None:
        if self.is_quitting(new_data):
            View.modification_canceled()
            return

        setattr(obj, attribute, new_data)
        if isinstance(obj, Customer):
            obj.last_update = datetime.now()
        obj.save()
        View.modification_done()

    def create_specific_datetime(self, is_starting=True) -> datetime | str:
        while True:
            date, hour = View.asks_event_date(is_starting)

            if self.is_quitting(date) or self.is_quitting(hour):
                return "q"

            formated_date = self.convert_str_in_datetime(date, hour)

            if isinstance(formated_date, datetime):
                return formated_date
