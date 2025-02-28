from view.management_view import ManagementView as View
from models.db_models import Collaborator


class ManagementController:
    @staticmethod
    def collab_creation() -> None:
        is_username_already_use: bool = True
        username: str = ""

        while is_username_already_use:
            username = View.asks_username()

            if View.is_quitting(username):
                return

            is_username_already_use = Collaborator.get_or_none(username=username) is None

        password: str = View.asks_password()
        role = View.asks_role()

        if View.is_quitting(password) or View.is_quitting(role):
            return

        Collaborator.create_collab(username, password, role)
        print(f"Collaborateur {username} créé !")

    @staticmethod
    def collab_modification():
        username = View.asks_username("à modifier")
        collaborator = Collaborator.get_or_none(username=username)

        if collaborator is None:
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
