from bakery import ls
from pytest import mark


@mark.loop
def test_loop(cookies, cookies_ls):
    with cookies:
        for item in ls:
            assert item in cookies_ls
