from pytest import fixture, mark

bulbasaur = sorted(("001: Bulbasaur", "002: Ivysaur", "003: Venusaur"))
last_three = sorted(("058: Growlithe", "059: Arcanine", "060: Poliwag"))


@mark.trim
class TestTrim:
    @fixture
    def cat(self, cookies, scope="class"):
        from bakery import cat

        return cat.deepcopy_(cookies / "01", _list=True, _sort=None)

    def test_int(self, cat):
        assert cat(_n_lines=3) == bulbasaur

    def test_tuple(self, cat):
        assert cat(_n_lines=(3,)) == bulbasaur

    def test_dict(self, cat):
        assert cat(_n_lines=dict(number=3)) == bulbasaur

    def test_last_tuple(self, cat):
        assert cat(_n_lines=(True, 3)) == last_three

    def test_last_dict(self, cat):
        assert cat(_n_lines=dict(last=True, number=3)) == last_three
