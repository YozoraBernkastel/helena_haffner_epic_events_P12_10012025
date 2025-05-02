from models.db_models import Collaborator
from tests.mock import MANAGEMENT_1, SUPPORT_1


def test_find_collaborator(db_connection):
    collab = Collaborator.find_collaborator(MANAGEMENT_1["username"], MANAGEMENT_1["password"])
    assert isinstance(collab, Collaborator)
    assert collab.username == MANAGEMENT_1["username"]

    collab = Collaborator.find_collaborator(SUPPORT_1["username"], MANAGEMENT_1["password"])
    assert collab is None



