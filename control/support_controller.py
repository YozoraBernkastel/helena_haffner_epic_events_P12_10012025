from view.support_view import SupportView as View
from control.generic_controller import GenericController
from models.db_models import Collaborator


class SupportController(GenericController):
    def __init__(self, user: Collaborator):
        self.user: Collaborator = user

    @classmethod
    def home_menu(cls) -> None:
        pass
