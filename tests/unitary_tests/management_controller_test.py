from control.management_controller import ManagementController
from models.db_models import Collaborator
from settings.settings import MANAGEMENT, SUPPORT, SALES
from tests.conftest import management_controller
from tests.mock import TO_CHANGE_COLLAB, q, MANAGEMENT_1


def test_role_change(management_controller, monkeypatch):
    controller: ManagementController = management_controller
    collab: Collaborator = Collaborator.get(username=TO_CHANGE_COLLAB["username"])

    assert collab.role != SALES
    monkeypatch.setattr('builtins.input', lambda _: "3")
    controller.role_change(collab)

    # check if the object is updated
    assert collab.role == SALES

    # check if the database is updated
    collab_from_db: Collaborator = Collaborator.get(username=TO_CHANGE_COLLAB["username"])
    assert collab_from_db.role == SALES

def test_username_change(management_controller, monkeypatch):
    controller: ManagementController = management_controller
    collab: Collaborator = Collaborator.get(username=TO_CHANGE_COLLAB["username"])

    old_username: str = collab.username
    monkeypatch.setattr('builtins.input', lambda _: q)
    controller.username_change(collab)

    # check quit works
    assert Collaborator.get_or_none(username=old_username) is not None

    new_username: str = "Newt Naim"
    monkeypatch.setattr('builtins.input', lambda _: new_username)
    controller.username_change(collab)

    # check if the object is updated
    assert collab.username != old_username
    assert collab.username == new_username

    # check if the database is updated
    assert Collaborator.get_or_none(username=old_username) is None
    assert Collaborator.get_or_none(username=new_username) is not None

# def test_check_user_password(management_controller, monkeypatch):
#     controller: ManagementController = management_controller
#     monkeypatch.setattr('builtins.input', lambda _: MANAGEMENT_1["password"])
#     assert controller.check_user_password()

