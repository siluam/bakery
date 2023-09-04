from pytest import fixture, mark


@mark.string_output
class TestStringOutput:
    @fixture
    def echo(self, scope="class"):
        from bakery import echo

        return echo.deepcopy_("Hello!")

    def test_short(self, echo):
        assert echo(_str=True) == "Hello!"

    def test_long(self, echo):
        assert echo(_type=str) == "Hello!"
