from oreo import is_hidden, is_nots
from pytest import fixture, mark


@mark.bakery
class TestBakery:
    @fixture
    def ls(self, cookies, scope="class"):
        from bakery import ls

        return ls.deepcopy_(cookies)

    def test_bakery(self, assorted_cookies, ls):
        assert assorted_cookies == ls(_list=True, _sort=None, _filter=(True, is_hidden))

    def test_program_options(self, assorted_cookies, ls):
        assert assorted_cookies == ls(_list=True, a=True, _sort=None, _filter=is_nots)
