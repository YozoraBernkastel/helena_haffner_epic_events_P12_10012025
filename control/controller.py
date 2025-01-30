import bcrypt
from models.db_models import Collaborator, Client, Contract, Event
from view.view import View
from control.jwt_helper import JwtHelper

class Controller:
    def __init__(self):
        self.user: Collaborator | None = None

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

    @staticmethod
    def create_jwt():
        pass

    def display_welcome_menu(self) -> None:
        # if JwtHelper.decode_jwt(token)
        while self.user is None:
            username, password = View.connection()
            self.user = Collaborator.find_collaborator(username, password)
            if self.user is None:
                print("Utilisateur ou mot de passe inconnu.")

        if View.remember_me():
            JwtHelper.generate(self.user.id)

        print(f"{self.user.username = }")
        print(f"{self.user.role = }")


        # todo penser à sauvegarder l'id de l'utilisateur par exemple.
