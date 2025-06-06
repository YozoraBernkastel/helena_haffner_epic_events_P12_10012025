from models.db_models import Collaborator
from tests.mock import TO_CREATE_COLLAB, q


def test_collab_interactions(management_controller, monkeypatch):
    def mock_password(*args, **kwargs):
        return TO_CREATE_COLLAB["password"]

    blabla = ["1", "1", TO_CREATE_COLLAB["username"], "2", q,
              "1", "2", TO_CREATE_COLLAB["username"], "2", "1", q,
              "1", "3", TO_CREATE_COLLAB["username"], "1", q]
    monkeypatch.setattr('builtins.input', lambda _: blabla.pop(0))
    monkeypatch.setattr('getpass.getpass', mock_password)

    # create collab
    collab = Collaborator.get_or_none(username=TO_CREATE_COLLAB["username"])
    assert collab is None
    management_controller.home_menu()
    new_collab = Collaborator.get_or_none(username=TO_CREATE_COLLAB["username"])
    first_role: str = new_collab.role
    assert isinstance(new_collab, Collaborator)

    # role modified
    management_controller.home_menu()
    new_collab = Collaborator.get_or_none(username=TO_CREATE_COLLAB["username"])
    assert first_role != new_collab.role

    # delete collab
    management_controller.home_menu()
    new_collab = Collaborator.get_or_none(username=TO_CREATE_COLLAB["username"])
    assert new_collab is None
