import bakery

from bakery import ls
from pytest import mark


@mark.freezing
def test_freezing():
    assert isinstance(ls(...), bakery())
