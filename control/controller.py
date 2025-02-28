from models.db_models import Collaborator, Client, Contract, Event
from control.management_controller import ManagementController
from control.sales_controller import SalesController
from control.support_controller import SupportController
from view.generic_view import View
from Helper.jwt_helper import JwtHelper
from models.picture_encoding import PictureEncoding
from models.picture_decoding import PictureDecoding
from settings.settings import MANAGEMENT, SALES, SUPPORT


class Controller:
    def __init__(self):
        self.user: Collaborator | None = None
        self.picture_encoding = PictureEncoding()
        self.picture_decoding = PictureDecoding()

        self.init_db()

    @staticmethod
    def init_db():
        # todo permettre de créer un premier compte utilsiateur (management seulement) si aucune db n'existe !!
        Collaborator.create_table()
        Client.create_table()
        Contract.create_table()
        Event.create_table()

    def log_in(self) -> None:
        while self.user is None:
            username, password = View.connection()
            self.user = Collaborator.find_collaborator(username, password)
            if self.user is None:
                print("Utilisateur ou mot de passe inconnu.")

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

    def change_password(self) -> bool:
        if View.wants_to_change_password():
            actual_password = View.asks_actual_password()
            if actual_password.lower() != "q" and Collaborator.find_collaborator(username=self.user.username,
                                                                                 password=actual_password):
                new_password = View.asks_new_password()
                if not View.is_quitting(new_password):
                    Collaborator.update_password(self.user.username, new_password)
                    return True

        return False

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
        print(f"Bonjour {self.user.username} !!")

        if self.change_password():
            print("Le mot de passe a été modifié avec succès !\n")

        role_controller = self.role_controller()
        role_controller.home_menu()









