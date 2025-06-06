from os import path
from models.db_models import db_name, Collaborator, Customer, Contract, Event
from control.generic_controller import GenericController
from control.management_controller import ManagementController
from control.sales_controller import SalesController
from control.support_controller import SupportController
from view.generic_view import View
from Helper.jwt_helper import JwtHelper
from models.picture_encoding import PictureEncoding
from models.picture_decoding import PictureDecoding
from settings.settings import MANAGEMENT, SALES


class Controller(GenericController):
    """
    Controller use as long as the user is unknown.
    """

    def __init__(self):
        self.user: Collaborator | None = None
        self.picture_encoding = PictureEncoding()
        self.picture_decoding = PictureDecoding()

        self.init_db()

    def first_user_creation(self):
        """
        If the dabase is empty, create a first collaborator with the management's role.
        :return:
        """
        if Collaborator.select().count() > 0:
            return

        View.create_first_user_warning()
        username, password = self.choose_username_and_password()

        if self.is_quitting(username):
            return

        Collaborator.create_collab(username, password, MANAGEMENT)
        View.create_with_success()

    def init_db(self):
        """
        Create the database if there is none.
        :return:
        """
        if not path.exists(db_name):
            Collaborator.create_table()
            Customer.create_table()
            Contract.create_table()
            Event.create_table()
            self.first_user_creation()

    def log_in(self) -> None:
        """
        Ask the user their username and password and get the matching Collaborator from the database
        :return:
        """
        while self.user is None:
            username, password = View.connection()
            self.user = Collaborator.find_collaborator(username, password)
            if self.user is None:
                View.unknown_user_or_password()

        if self.picture_encoding.are_all_pictures_exists() and View.remember_me():
            token = JwtHelper.generate_jwt(user_id=self.user.id)
            self.picture_encoding.crypt_token(token)

    @staticmethod
    def find_last_user(last_user_id) -> Collaborator | None:
        """
        Check the last registered user and, if there is one, asks the current user if it's their account
        :param last_user_id:
        :return:
        """
        user = Collaborator.find_last_user_session(last_user_id)

        if user is None:
            return None

        is_user: bool = View.is_that_you(user.username)

        return user if is_user else None

    def role_controller(self):
        """
        Return the controller's class corresponding to the role of the user.
        :return:
        """
        if self.user.role == MANAGEMENT:
            return ManagementController(self.user)
        if self.user.role == SALES:
            return SalesController(self.user)

        return SupportController(self.user)

    def display_welcome_menu(self) -> None:
        """
        Check if there is an existing token. If it's the case, ask user if it's their account.
        If there is no token or if it's not the user's account, asks their username and password to find the
        user corresponding.
        Finally redirect the user to controller corresponding to their role.
        :return:
        """
        token: str = self.picture_decoding.token_getter()
        last_user_id: int = JwtHelper.decode_jwt(token)

        if last_user_id is not None:
            self.user = self.find_last_user(last_user_id)

        if self.user is None:
            self.log_in()

        assert self.user is not None
        View.hello_prompt(self.user.username)

        role_controller = self.role_controller()
        role_controller.home_menu()
