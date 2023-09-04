from addict import Dict
from autoslot import Slots
from oreo import is_coll, tea


class frosting(tea, Slots):
    def __init__(self, output, capture="stdout"):
        self.capture = "stderr" if capture == "stderr" else "stdout"
        self.dict_like = isinstance(output, dict)
        self.iterable = is_coll(output)
        self.output = output
        if self.dict_like:
            super().__init__(**self.output)
        elif self.iterable:
            super().__init__(*self.output)
        else:
            super().__init__(self.output)

    # NOTE: This is a tea / dict subclass; `get' works here,
    #       but it normally doesn't work for attribute access,
    #       as the former uses `__getitem__',
    #       while the latter uses `__getattr__'.
    def __iter__(self):
        yield from (self[self.capture] if self.dict_like else self.values())

    def __call__(self):
        if not self.iterable:
            return self.output
        if self.dict_like:
            return Dict(self.items())
        return self.values()
