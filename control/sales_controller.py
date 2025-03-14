from view.sales_view import SalesView as View
from models.db_models import Collaborator
from control.generic_controller import GenericController


class SalesController(GenericController):
    def __init__(self, user: Collaborator):
        self.user: Collaborator = user

    @classmethod
    def home_menu(cls) -> None:
        pass

