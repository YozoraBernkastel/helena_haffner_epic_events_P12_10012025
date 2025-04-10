from view.management_view import ManagementView as View
from control.generic_controller import GenericController
from models.db_models import Collaborator, Contract, Event
from settings.settings import SALES, MANAGEMENT, SUPPORT


class ManagementController(GenericController):
    def __init__(self, user: Collaborator):
        self.user: Collaborator = user

    def collab_creation(self) -> None:
        is_username_already_use: bool = True
        username: str = ""

        while is_username_already_use:
            username = View.asks_username()

            if self.is_quitting(username):
                return

            if self.is_available_username(username):
                break
            View.username_already_used(username)

        password: str = View.asks_collab_password()

        if self.is_quitting(password):
            return

        role = View.asks_role()

        if self.is_quitting(role):
            return

        Collaborator.create_collab(username, password, role)
        View.create_with_success(f"du collaborateur {username}")

    def username_change(self, collaborator: Collaborator) -> None:
        while True:
            new_username = View.asks_username("à partir de maintenant")

            if self.is_quitting(new_username):
                return

            if self.is_available_username(new_username):
                collaborator.update_username(new_username=new_username)
                View.modification_done()
                return

            View.username_already_used(new_username)

    def role_change(self, collaborator: Collaborator) -> None:
        new_role = View.asks_role(modification=True)

        if not self.is_quitting(new_role):
            collaborator.update_role(new_role=new_role)
            View.modification_done()

    def check_user_password(self):
        user_password = View.asks_actual_password()
        return Collaborator.find_collaborator(self.user.username, user_password) is not None

    def password_reset(self, collaborator: Collaborator) -> None:
        if not View.reset_collab_password(collaborator.username):
            return

        if self.check_user_password():
            new_password = View.asks_collab_password()
            collaborator.update_password(new_password=new_password)
            View.password_updated()

    def collab_modification(self) -> None:
        username = View.asks_username("à modifier")
        if self.is_quitting(username):
            return

        collaborator = Collaborator.get_or_none(username=username)

        if collaborator is None:
            View.missing_collaborator(username)
            return

        choice = View.which_info_change()

        if choice == "1":
            self.username_change(collaborator)
        elif choice == "2":
            self.role_change(collaborator)
        elif choice == "3":
            self.password_reset(collaborator)
        else:
            return

    def collab_deletion(self):
        # todo si le collaborateur a des clients par exemple, il faut peut-être demander à réattribuer les clients à quelqu'un d'autre avant la suppression, non ?
        username = View.asks_username("à supprimer")
        if self.is_quitting(username):
            return

        collaborator = Collaborator.get_or_none(username=username)

        if collaborator is None:
            View.missing_collaborator(username)
            return

        if View.asks_collab_delete_confirmation(collaborator.username):
            collaborator.delete_instance()
            View.deletion_complete()

    def choose_role_menu(self):
        role = View.which_role()
        if self.is_quitting(role):
            return

        collab_list = Collaborator.select().where(Collaborator.role == role).execute()
        [View.collab_display(collab) for collab in collab_list]

    def collab_list(self):
        choice = View.collab_list_menu()
        if choice == "1":
            self.all_collab_list()
        elif choice == "2":
            self.choose_role_menu()
        else:
            return

    def collab_menu(self) -> None:
        choice = View.collab_menu()

        if choice == "1":
            self.collab_creation()
        elif choice == "2":
            self.collab_modification()
        elif choice == "3":
            self.collab_deletion()
        elif choice == "4":
            self.collab_list()
        else:
            return

    def contract_creation(self):
        while True:
            contract_name: str = View.asks_contract_name()
            if self.is_quitting(contract_name):
                return
            if self.is_available_contract_name(contract_name):
                break

        sales_collab = self.find_collab(SALES)
        if self.is_quitting(sales_collab):
            return
        customer = self.find_customer(sales_collab)
        if self.is_quitting(customer):
            return
        total_value = View.asks_contract_total_value()

        Contract.create(name=contract_name, customer=customer, collaborator=sales_collab, total_value=total_value,
                        remains_to_be_paid=total_value)

        View.create_with_success(f"du contrat {contract_name}")

    @classmethod
    def delete_contract(cls, user: Collaborator) -> None:
        contract: Contract | str = cls.find_contract()
        if cls.is_quitting(contract):
            return

        if user.role == MANAGEMENT:
            contract.delete_instance()
            View.deletion_complete()

    def contracts_menu(self) -> None:
        choice = View.contract_menu()

        if choice == "1":
            self.contract_creation()
        elif choice == "2":
            self.contract_detail_modification(self.user)
        elif choice == "3":
            self.all_contracts_list()
        elif choice == "4":
            contract = self.find_contract()
            View.contract_display(contract)
        elif choice == "5":
            self.delete_contract(self.user)
        else:
            return

    def change_event_collab(self):
        event: Event | str = self.find_event()
        if self.is_quitting(event):
            return

        collab: Collaborator | str = self.find_collab(SUPPORT)
        if self.is_quitting(collab):
            return

        event.support = collab
        event.save()
        View.modification_done()

    def event_menu(self):
        choice = View.event_menu_display()

        if choice == "1":
            self.all_events_list()
        if choice == "2":
            self.event_display()
        if choice == "3":
            self.change_event_collab()

    def home_menu(self) -> None:
        while True:
            choice = View.menu()

            if choice == "1":
                self.collab_menu()
            elif choice == "2":
                self.contracts_menu()
            elif choice == "3":
                self.event_menu()
            elif choice == "4":
                self.all_customers_list()
            elif choice == "5":
                self.account_menu(self.user)
            else:
                return

