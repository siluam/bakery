from bakery import ls
from pytest import mark


@mark.split
def test_split(cookies):
    assert ls(
        cookies, _list=True, _split=1, _sort=True, _filter=lambda item: item.isnumeric()
    ) == [
        "6",
        "5",
        "4",
        "3",
        "2",
        "09",
        "08",
        "07",
        "06",
        "05",
        "04",
        "03",
        "02",
        "00",
        "0",
        "0",
    ]
