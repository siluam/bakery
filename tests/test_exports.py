from bakery import echo
from pytest import mark


@mark.exports
def test_exports():
    assert echo("$FOO", _exports=dict(FOO="bar"), _str=True) == "bar"
