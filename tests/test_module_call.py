import bakery
from oreo import is_nots
from pytest import mark, fixture


@mark.module_call
class TestModuleCall:
    @fixture
    def options(self):
        return dict(a=True, _list=True, _sort=None, _filter=is_nots)

    def test_module(self, assorted_cookies, cookies, options):
        assert assorted_cookies == bakery(program_="ls")(cookies, **options)

    def test_attr(self, assorted_cookies, cookies, options):
        assert assorted_cookies == bakery.ls(cookies, **options)
