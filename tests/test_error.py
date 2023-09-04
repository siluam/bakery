from bakery import OrderCancelled, OrderCancelled_1, OrderCancelled_2
from os import environ
from parametrized import parametrized
from pytest import fixture, mark

# NOTE: While building in nix, `ls' returns an error code of 1.

pure = environ.get("NIX_ENFORCE_PURITY", 0)


@mark.error
class TestError:
    @fixture
    def ls(self, scope="class"):
        import bakery

        return bakery(program_="ls", j=True)

    @mark.xfail(raises=OrderCancelled)
    def test_error(self, ls):
        assert ls()

    def test_ignore(self, ls):
        assert ls(_ignore_stderr=True)

    @mark.xfail(raises=OrderCancelled_2 if pure else OrderCancelled_1)
    def test_not_accepted(self, ls):
        assert ls(_returncodes=1 if pure else 2)

    @parametrized
    def test_accepted(
        self,
        ls,
        _returncodes=(2 if pure else 1, (1, 2)),
    ):
        assert ls(_returncodes=_returncodes)

    def test_OrderCancelled(self, ls):
        try:
            ls()
        except (
            OrderCancelled_2
            if environ.get("NIX_ENFORCE_PURITY", 0)
            else OrderCancelled_1
        ):
            pass

    @mark.trim
    def test_stdout(self, ls):
        assert (
            ls(_stdout_stderr=True, _ignore_stderr=True, _str=True, _n_lines=1)
            == "ls: invalid option -- 'j'"
        )

    def test_false(self, ls):
        assert not ls(_false_stderr=True)

    def test_replace_bool(self, ls):
        assert ls(_replace_stderr=True)

    def test_replace_string(self, ls):
        replacement = "replace error test"
        assert ls(_replace_stderr=replacement) == replacement
