import oreo

from bakery import frosting
from parametrized import parametrized
from pytest import fixture, mark


def sort_func(item):
    return int(item) if item.isnumeric() else ord(item[0])


@mark.sorted_output
class TestSortedOutput:
    @fixture
    def ls(self, cookies, scope="class"):
        from bakery import ls

        return ls.deepcopy_(cookies)

    @parametrized
    def test_output(
        self,
        assorted_cookies,
        ls,
        opts=(dict(_list=True), dict(_type=frosting), dict(_frosting=True)),
    ):
        assert assorted_cookies == ls(_sort=None, **opts)

    def test_sorted_key_output(self, cookies, ls):
        assert oreo.ls(cookies, key=sort_func) == ls(_list=True, _sort=sort_func)

    def test_sorted_reversed_output(self, assorted_cookies, ls):
        assert assorted_cookies[::-1] == ls(_list=True, _sort=True)

    def test_sorted_dict_keyword(self, cookies, ls):
        assert oreo.ls(cookies, key=sort_func, reverse=True) == ls(
            _list=True, _sort=dict(key=sort_func, reverse=True)
        )
