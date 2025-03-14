from view.management_view import ManagementView as View
from control.generic_controller import GenericController
from models.db_models import Collaborator


class ManagementController(GenericController):
    def __init__(self, user: Collaborator):
        self.user: Collaborator = user

    @classmethod
    def collab_creation(cls) -> None:
        is_username_already_use: bool = True
        username: str = ""

        while is_username_already_use:
            username = View.asks_username()

            if cls.is_quitting(username):
                return

            if cls.is_available_username(username):
                break
            View.username_already_used(username)

        password: str = View.asks_password()

        if cls.is_quitting(password):
            return

        role = View.asks_role()

        if cls.is_quitting(role):
            return

        Collaborator.create_collab(username, password, role)
        print(f"Collaborateur {username} créé !")

    @classmethod
    def username_change(cls, collaborator: Collaborator) -> None:
        while True:
            new_username = View.asks_username("à partir de maintenant")

            if cls.is_quitting(new_username):
                return

            if cls.is_available_username(new_username):
                collaborator.update_username(new_username=new_username)
                return

            View.username_already_used(new_username)

    @classmethod
    def role_change(cls, collaborator: Collaborator) -> None:
        View.actual_role(collaborator)
        new_role = View.asks_role(modification=True)
        print(f"{new_role = }")

    @classmethod
    def collab_modification(cls) -> None:
        username = View.asks_username("à modifier")
        if cls.is_quitting(username):
            return

        collaborator = Collaborator.get_or_none(username=username)

        if collaborator is None:
            View.missing_collaborator(username)
            return

        choice = View.which_info_change()

        if choice == "1":
            cls.username_change(collaborator)
        elif choice == "2":
            cls.role_change(collaborator)
        elif choice == "3":
            cls.password_reset(collaborator)
        else:
            return

    @staticmethod
    def collab_deletion():
        pass

    @staticmethod
    def collab_list():
        # todo menu choix de role puis afficher la liste des employés possédant ce rôle j'imagine
        pass

    @classmethod
    def collab_menu(cls) -> None:
        while True:
            choice = View.collab_menu()

            if choice == "1":
                cls.collab_creation()
            elif choice == "2":
                cls.collab_modification()
            elif choice == "3":
                cls.collab_deletion()
            elif choice == "4":
                cls.collab_list()
            else:
                return

    def home_menu(self) -> None:
        choice = View.menu()

        if choice == "1":
            self.collab_menu()
        elif choice == "2":
            self.contracts_menu()
        elif choice == "3":
            self.events_menu()
        elif choice == "4":
            self.account_menu(self.user)
        else:
            return
