from models.db_models import Collaborator, Client, Contract, Event
from view.view import View

class Controller:
    def __init__(self):
        self.user: Collaborator | None = None
        # todo utilisateur persistant, pour a utiliser JWToken (voir compte rendu)

        self.init_db()

    @staticmethod
    def init_db():
        # todo if no db (file or table) --> need to check if each table exists ?
        Collaborator.create_table()
        Client.create_table()
        Contract.create_table()
        Event.create_table()

    def display_welcome_menu(self):

        while self.user is None:
            username, password = View.connection()
            self.user = Collaborator.find_collaborator(username, password)
            if self.user is None:
                print("Utilisateur ou mot de passe inconnu.")

        # todo générer JWToken ici !! Possibilité de se déconnecter ? Comment ?
        print(f"{self.user.username = }")

        # todo penser à sauvegarder l'id de l'utilisateur par exemple.
