from view.management_view import ManagementView as View
from control.generic_controller import GenericController
from models.db_models import Collaborator


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
        print(f"Collaborateur {username} créé !")

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

    @staticmethod
    def objects_list():
        # todo menu choix de role puis afficher la liste des employés possédant ce rôle j'imagine
        # todo peut aussi accéder aux events, clients, etc en liste seule
        pass

    def collab_menu(self) -> None:

        choice = View.collab_menu()

        if choice == "1":
            self.collab_creation()
        elif choice == "2":
            self.collab_modification()
        elif choice == "3":
            self.collab_deletion()
        elif choice == "4":
            self.objects_list()
        else:
            return

    def home_menu(self) -> None:
        while True:
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

