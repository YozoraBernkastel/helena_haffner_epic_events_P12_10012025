from view.generic_view import View
from models.db_models import Collaborator

class GenericController:
    @staticmethod
    def is_quitting(choice: str) -> bool:
        return choice.lower() == "q"

    @staticmethod
    def is_available_username(username: str) -> bool:
        return Collaborator.get_or_none(username=username) is not None

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
                Collaborator.update_password(user.username, new_password)
                return
        else:
            View.bad_password()

        View.modification_canceled()

    @classmethod
    def account_menu(cls, user):
        # todo à compléter avec le changement de nom d'utilisateur
        cls.change_password(user)
        pass