from view.management_view import ManagementView as View
from control.generic_controller import GenericController
from models.db_models import Collaborator


class ManagementController(GenericController):
    @classmethod
    def collab_creation(cls) -> None:
        is_username_already_use: bool = True
        username: str = ""

        while is_username_already_use:
            username = View.asks_username()

            if cls.is_quitting(username):
                return

            is_username_already_use = Collaborator.get_or_none(username=username) is None

        password: str = View.asks_password()
        role = View.asks_role()

        if cls.is_quitting(password) or cls.is_quitting(role):
            return

        Collaborator.create_collab(username, password, role)
        print(f"Collaborateur {username} créé !")

    @classmethod
    def collab_modification(cls):
        username = View.asks_username("à modifier")
        collaborator = Collaborator.get_or_none(username=username)

        if collaborator is None:
            View.missing_collaborator(username)
            return

        choice = View.which_info_change()

        if choice == "1":
            cls.username_modif()
        elif choice == "2":
            cls.role_modif()
        elif choice == "3":
            cls.password_change()
        else:
            return

    @staticmethod
    def collab_deletion():
        pass

    @classmethod
    def collab_menu(cls) -> None:
        choice = View.collab_menu()

        if choice == "1":
            cls.collab_creation()
        elif choice == "2":
            cls.collab_modification()
        elif choice == "3":
            cls.collab_deletion()
        else:
            return

    @classmethod
    def home_menu(cls) -> None:
        choice = View.menu()

        if choice == "1":
            cls.collab_menu()
        elif choice == "2":
            View.contracts_menu()
        elif choice == "3":
            View.events_menu()
        else:
            return
