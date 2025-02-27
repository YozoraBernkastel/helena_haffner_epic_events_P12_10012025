import bcrypt
from models.db_models import Collaborator, Client, Contract, Event
from view.generic_view import View
from view.management_view import ManagementView
from view.sales_view import SalesView
from view.support_view import SupportView
from Helper.jwt_helper import JwtHelper
from models.picture_encoding import PictureEncoding
from models.picture_decoding import PictureDecoding

class Controller:
    def __init__(self):
        self.user: Collaborator | None = None
        self.picture_encoding = PictureEncoding()
        self.picture_decoding = PictureDecoding()

        self.init_db()

    @staticmethod
    def init_db():
        Collaborator.create_table()
        Client.create_table()
        Contract.create_table()
        Event.create_table()

    @staticmethod
    def dress_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password=bytes(password, encoding="ascii"), salt=salt)
        return hashed

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

    def management_path(self) -> None:
        choice = ManagementView.menu()

        if choice == "1":
            ManagementView.users_db_menu()
        elif choice == "2":
            ManagementView.contracts_menu()
        elif choice == "3":
            ManagementView.events_menu()

    def support_path(self):
        pass

    def sales_path(self):
        pass

    def display_welcome_menu(self) -> None:
        token: str = self.picture_decoding.token_getter()
        last_user_id: int = JwtHelper.decode_jwt(token)

        if last_user_id is not None:
            self.user = self.find_last_user(last_user_id)

        if self.user is None:
            self.log_in()

        assert self.user is not None
        print(f"Bonjour {self.user.username} !!")
        print(self.user.role)

        if self.user.role == "management":
            self.management_path()
        elif self.user.role == "support":
            self.support_path()
        elif self.user.role == "sales":
            self.sales_path()
        else:
            print("Aucun accès aux données")





