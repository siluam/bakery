from bakery import ls, env, grep, tail
from oreo import is_nots, first_last_n
from pytest import mark


@mark.piping
class TestPiping:
    def test_first(self, assorted_cookies, cookies):
        tails = (
            ls(
                ...,
                cookies,
                a=True,
                _list=True,
                _sort=None,
                _filter=is_nots,
            )
            | tail
        )
        assert (
            first_last_n(assorted_cookies, last=True, number=10, type_=list) == tails()
        )

    def test_both(self):
        egrep = env(..., _exports=dict(FOO="bar"), _str=True) | grep(..., "FOO")
        assert egrep() == "FOO=bar"
