from control.main_controller import Controller, ManagementController, SalesController, SupportController
from models.db_models import Collaborator
from settings.settings import MANAGEMENT, SALES, SUPPORT
from tests.mock import MANAGEMENT_1, SALES_1, SUPPORT_1, mock_get_pass


def test_role_controller():
    controller = Controller()

    controller.user = Collaborator.get(username=MANAGEMENT_1["username"])
    assert isinstance(controller.user, Collaborator)
    assert controller.user.role == MANAGEMENT
    specific_controller = controller.role_controller()
    assert isinstance(specific_controller, ManagementController)

    controller.user = Collaborator.get(username=SALES_1["username"])
    assert isinstance(controller.user, Collaborator)
    assert controller.user.role == SALES
    specific_controller = controller.role_controller()
    assert isinstance(specific_controller, SalesController)

    controller.user = Collaborator.get(username=SUPPORT_1["username"])
    assert isinstance(controller.user, Collaborator)
    assert controller.user.role == SUPPORT
    specific_controller = controller.role_controller()
    assert isinstance(specific_controller, SupportController)


def test_log_in(monkeypatch):
    controller = Controller()

    monkeypatch.setattr('builtins.input', lambda _: MANAGEMENT_1["username"])
    monkeypatch.setattr('getpass.getpass', mock_get_pass)

    controller.log_in()
    assert controller.user.username == MANAGEMENT_1["username"]


