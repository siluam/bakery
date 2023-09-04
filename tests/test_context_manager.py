from oreo import is_hidden, is_nots
from parametrized import parametrized
from pytest import fixture, mark
from rich.pretty import pprint


@mark.context_manager
class TestContextManager:
    @fixture
    def ls(self):
        import bakery

        return bakery(program_="ls", _list=True, _sort=None)

    @parametrized
    def test_context(
        self,
        assorted_cookies,
        cookies,
        ls,
        opts=({"_" + opt: True} for opt in ("context", "c")),
    ):
        with ls(cookies, a=True, _filter=is_nots, **opts) as lsa:
            assert assorted_cookies == lsa()
        assert ls(cookies, _filter=(True, is_hidden)) == assorted_cookies

    @parametrized
    def test_new(
        self,
        assorted_cookies,
        cookies,
        ls,
        opts=({"_" + opt: True} for opt in ("new_context", "nc")),
    ):
        with ls(cookies, a=True, _filter=is_nots, **opts) as lsa:
            output = lsa()
            assert not isinstance(output, list)
            assert assorted_cookies == list(output)
        assert ls(cookies, _filter=(True, is_hidden)) == assorted_cookies
