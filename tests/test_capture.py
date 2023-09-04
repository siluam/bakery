from parametrized import parametrized
from pytest import fixture, mark, param


@mark.capture
class TestCapture:
    @fixture
    def ls(self):
        import bakery

        return bakery(program_="ls", a=True, _str=True)

    @parametrized
    def test_std(
        self,
        ls,
        opts=(dict(_capture="stdout"), dict(_capture="stderr", _stderr_stdout=True)),
    ):
        assert ls(**opts)

    @parametrized
    def test_empty(
        self,
        ls,
        opts=(dict(_capture="stderr"), dict(_capture="stdout", _stderr_stdout=True)),
    ):
        assert not ls(**opts)

    def test_stderr_stdout(self, ls):
        assert ls(_stderr_stdout=True)

    @parametrized.zip
    def test_both(
        self,
        ls,
        _stderr_stdout=(False, True),
        true=("stdout", "stderr"),
        false=("stderr", "stdout"),
    ):
        output = ls(_capture="both", _stderr_stdout=_stderr_stdout)
        assert getattr(output, true)
        assert not getattr(output, false)
