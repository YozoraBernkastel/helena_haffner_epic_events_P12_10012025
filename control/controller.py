import bcrypt
from models.db_models import Collaborator, Client, Contract, Event
from view.view import View
from Helper.jwt_helper import JwtHelper

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

    def log_in(self) -> None:
        while self.user is None:
            username, password = View.connection()
            self.user = Collaborator.find_collaborator(username, password)
            if self.user is None:
                print("Utilisateur ou mot de passe inconnu.")

        if View.remember_me():
            token = JwtHelper.generate_jwt(user_id=self.user.id)
            print(f"{token = }")

    @staticmethod
    def get_last_token():
        # todo remplacer le token en dur par une récupération dans un fichier (ini ?)
        token = None

        return token

    def display_welcome_menu(self) -> None:
        token = self.get_last_token()
        last_user_id = JwtHelper.decode_jwt(token)

        if last_user_id is not None:
            self.user = Collaborator.find_last_user_session(last_user_id)

        if self.user is None:
            self.log_in()
        else:
            # todo demander à l'utilisateur s'il s'agit bien de lui probablement
            pass

        assert self.user is not None
        print(f"Bravo {self.user.username} !! Vous venez de vous connecter !!!!!")


