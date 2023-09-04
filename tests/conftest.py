from oreo import ls
from pytest import fixture
from valiant import SuperPath


@fixture
def cookies():
    return SuperPath(__file__).parent.parent / "cookies"


@fixture
def cookies_ls(cookies):
    return ls(cookies)


@fixture
def assorted_cookies(cookies):
    return ls(cookies, key=True)
