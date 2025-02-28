from models.db_models import Collaborator, Client, Contract, Event
from control.generic_controller import GenericController
from control.management_controller import ManagementController
from control.sales_controller import SalesController
from control.support_controller import SupportController
from view.generic_view import View
from Helper.jwt_helper import JwtHelper
from models.picture_encoding import PictureEncoding
from models.picture_decoding import PictureDecoding
from settings.settings import MANAGEMENT, SALES, SUPPORT


class Controller(GenericController):
    def __init__(self):
        self.user: Collaborator | None = None
        self.picture_encoding = PictureEncoding()
        self.picture_decoding = PictureDecoding()

        self.init_db()

    @staticmethod
    def init_db():
        # todo permettre de créer un premier compte utilisateur (management seulement) si aucune db n'existe !!
        Collaborator.create_table()
        Client.create_table()
        Contract.create_table()
        Event.create_table()

    def log_in(self) -> None:
        while self.user is None:
            username, password = View.connection()
            self.user = Collaborator.find_collaborator(username, password)
            if self.user is None:
                View.unknown_user_or_password()

        if self.picture_encoding.are_all_pictures_exists() and View.remember_me():
            token = JwtHelper.generate_jwt(user_id=self.user.id)
            self.picture_encoding.crypt_token(token)

    @staticmethod
    def find_last_user(last_user_id):
        user = Collaborator.find_last_user_session(last_user_id)
        is_user: bool = View.is_that_you(user.username)

        return user if is_user else None

    def support_path(self):
        pass

    def sales_path(self):
        pass

    def new_password(self):
        while True:
            password1 = View.asks_password_template("Entrez votre nouveau mot de passe une première fois")

            if self.is_quitting(password1):
                return password1

            password2 = View.asks_password_template("Puis une seconde fois")

            if self.is_quitting(password2):
                return password2

            if password1 == password2:
                return password1

            View.different_passwords_prompt()

    def change_password(self) -> None:
        if not View.wants_to_change_password():
            return

        actual_password = View.asks_actual_password()
        if Collaborator.find_collaborator(username=self.user.username, password=actual_password):
            new_password = self.new_password()

            if not self.is_quitting(new_password):
                Collaborator.update_password(self.user.username, new_password)
                return
        else:
            View.bad_password()

        View.modification_canceled()

    def role_controller(self):
        if self.user.role == MANAGEMENT:
            return ManagementController
        if self.user.role == SUPPORT:
            return SupportController
        if self.user.role == SALES:
            return SalesController

    def display_welcome_menu(self) -> None:
        token: str = self.picture_decoding.token_getter()
        last_user_id: int = JwtHelper.decode_jwt(token)

        if last_user_id is not None:
            self.user = self.find_last_user(last_user_id)

        if self.user is None:
            self.log_in()

        assert self.user is not None
        View.hello_prompt(self.user.username)

        self.change_password()

        role_controller = self.role_controller()
        role_controller.home_menu()









