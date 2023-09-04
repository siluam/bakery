from pytest import fixture, mark


def is_not_zero(i):
    return i.isnumeric() and (not "0" in i)


@mark.filtered_output
class TestFilteredOutput:
    @fixture
    def ls(self, cookies, scope="class"):
        from bakery import ls

        return ls.deepcopy_(cookies, _list=True, _sort=None)

    def test_function(self, cookies_ls, ls):
        assert ls(_filter=is_not_zero) == sorted(
            (i for i in cookies_ls if is_not_zero(i))
        )

    def test_collection(self, cookies_ls, ls):
        assert ls(_filter=(True, is_not_zero)) == sorted(
            (i for i in cookies_ls if not is_not_zero(i))
        )
