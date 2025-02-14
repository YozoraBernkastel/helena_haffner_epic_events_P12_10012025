import bcrypt
from models.db_models import Collaborator, Client, Contract, Event
from view.view import View
from Helper.jwt_helper import JwtHelper
from models.encod_picture import PictureManipulation

class Controller:
    def __init__(self):
        self.user: Collaborator | None = None
        self.pitcure_manip = PictureManipulation()

        self.init_db()

    @staticmethod
    def init_db():
        # todo if no db (file or table) --> need to check if each table exists ?
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

        if View.remember_me():
            token = JwtHelper.generate_jwt(user_id=self.user.id)
            self.pitcure_manip.crypt_token(token)

            print(f"{token = }")

    @staticmethod
    def get_last_token() -> str:
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsImV4cCI6MTczODQ5MDY3MX0.YfH47ok4D-bs5SaSrGXQcCmTWl4CQrQcfT3WwbYbSM0"

        return token

    @staticmethod
    def find_last_user(last_user_id):
        user = Collaborator.find_last_user_session(last_user_id)
        is_user: bool = View.is_that_you(user.username)

        return user if is_user else None

    def display_welcome_menu(self) -> None:
        token: str = self.get_last_token()
        last_user_id: int = JwtHelper.decode_jwt(token)

        if last_user_id is not None:
            self.user = self.find_last_user(last_user_id)

        if self.user is None:
            self.log_in()

        assert self.user is not None
        print(f"Bonjour {self.user.username} !!")


