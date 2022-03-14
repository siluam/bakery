import rich.traceback as RichTraceback
RichTraceback.install(show_locals = True)

import hy
import sys

from oreo import ModuleCaller

from .bakery import milcery

class bakery(ModuleCaller):
    def __call__(self, *args, **kwargs):
        if args or kwargs:
            return milcery(*args, **kwargs)
        else:
            return milcery
    def __getattr__(self, program_):
        if program_.startswith("_"):
            raise AttributeError
        else:
            return milcery(program_ = program_)
    bakery = __call__
    __all__ = [ var for var in vars() if var not in ('__qualname__',) ]

sys.modules[__name__] = bakery()
