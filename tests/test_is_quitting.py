from control.generic_controller import GenericController


def test_is_quitting():
    assert GenericController.is_quitting("q")


def test_is_not_quitting():
    assert not GenericController.is_quitting("a")
