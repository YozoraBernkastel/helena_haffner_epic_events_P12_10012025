from view.generic_view import View
from models.db_models import Collaborator, Customer
from settings.settings import SALES


class GenericController:
    @staticmethod
    def is_quitting(choice: str) -> bool:
        return choice.lower() == "q"

    @staticmethod
    def is_available_username(username: str) -> bool:
        return Collaborator.get_or_none(username=username) is None

    @staticmethod
    def is_available_mail(new_mail: str) -> bool:
        return Customer.get_or_none(mail=new_mail) is None

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
        pass

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