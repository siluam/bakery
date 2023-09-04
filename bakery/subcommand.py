from autoslot import Slots


class Subcommand(Slots):
    __slots__ = ("_unprocessed", "processed")
    default = "a1454c95-afbf-4c1a-ad12-0b6be7cc9768"

    @property
    def unprocessed(self):
        return self._unprocessed

    @unprocessed.setter
    def unprocessed(self, value):
        self._unprocessed = value
        self.process()

    def __init__(self, subcommand=None, intact=False):
        if isinstance(subcommand, self.__class__):
            self.intact = subcommand.intact
            setattr(self, "unprocessed", subcommand.unprocessed)
        else:
            self.intact = intact
            setattr(self, "unprocessed", subcommand or self.default)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.processed == other.processed
        return self.processed == other

    def process(self):
        if self.intact:
            self.processed = self._unprocessed
        else:
            self.processed = self._unprocessed.replace("_", "-")

    def extract(self, **kwargs):
        self.intact = kwargs.get("_intact_subcommand", False)
        subcommand = kwargs.get("_subcommand", self.default)
        if subcommand != self.default:
            self.unprocessed = subcommand

    def __rich_repr__(self):
        yield self.__str__()

    def __repr__(self):
        return repr(self.processed)

    def __str__(self):
        return repr(self.processed)
