from view.generic_view import View
from models.db_models import Collaborator, Customer, Event, Contract
from settings.settings import MANAGEMENT, SALES, SUPPORT
from datetime import datetime


class GenericController:
    @staticmethod
    def is_quitting(choice: str) -> bool:
        return isinstance(choice, str) and choice.lower().strip() == "q"

    @staticmethod
    def is_available_username(username: str) -> bool:
        return Collaborator.get_or_none(username=username) is None

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

        customer.collaborator = collaborator
        customer.save()
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

            #todo mettre un message pour dire que le contrat n'a pas été trouvé

    @staticmethod
    def all_contracts_list():
        all_contracts = Contract.select()
        [View.contract_display(contract) for contract in all_contracts]

    @classmethod
    def contract_detail_modification(cls):
        contract: Contract | str = cls.find_contract()
        if cls.is_quitting(contract):
            return

        View.contract_display(contract)
        View.contract_modification_prompt()

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

            support_collab = Collaborator.get_or_none(username=collab_name, role=role)
            if isinstance(support_collab, Collaborator):
                return support_collab

    @classmethod
    def find_customer(cls, collaborator: Collaborator) -> Customer | str:
        while True:
            customer_mail = View.asks_customer_mail()
            if cls.is_quitting(customer_mail):
                return customer_mail

            customer = Customer.get_or_none(mail=customer_mail, collaborator=collaborator)
            if customer is not None:
                return customer

            View.unknown_customer()
