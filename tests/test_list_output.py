from pytest import fixture, mark


@mark.list_output
class TestListOutput:
    @fixture
    def ls(self, cookies, scope="class"):
        from bakery import ls

        return ls.deepcopy_(cookies)

    def test_short(self, ls):
        assert isinstance(ls(_list=True), list)

    def test_long(self, ls):
        assert isinstance(ls(_type=list), list)
