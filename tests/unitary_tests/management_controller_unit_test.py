from models.db_models import Collaborator
from settings.settings import SALES
from tests.mock import TO_CHANGE_COLLAB, q, mock_get_pass


def test_role_change(management_controller, monkeypatch):
    collab: Collaborator = Collaborator.get(username=TO_CHANGE_COLLAB["username"])

    assert collab.role != SALES
    monkeypatch.setattr('builtins.input', lambda _: "3")
    management_controller.role_change(collab)

    # check if the object is updated
    assert collab.role == SALES

    # check if the database is updated
    collab_from_db: Collaborator = Collaborator.get(username=TO_CHANGE_COLLAB["username"])
    assert collab_from_db.role == SALES


def test_username_change(management_controller, monkeypatch):
    collab: Collaborator = Collaborator.get(username=TO_CHANGE_COLLAB["username"])

    old_username: str = collab.username
    monkeypatch.setattr('builtins.input', lambda _: q)
    management_controller.username_change(collab)

    # check quit works
    assert Collaborator.get_or_none(username=old_username) is not None

    new_username: str = "Newt Naim"
    monkeypatch.setattr('builtins.input', lambda _: new_username)
    management_controller.username_change(collab)

    # check if the object is updated
    assert collab.username != old_username
    assert collab.username == new_username

    # check if the database is updated
    assert Collaborator.get_or_none(username=old_username) is None
    assert Collaborator.get_or_none(username=new_username) is not None


def test_check_user_password(management_controller, monkeypatch):
    monkeypatch.setattr('getpass.getpass', mock_get_pass)
    assert management_controller.check_user_password() is not None
