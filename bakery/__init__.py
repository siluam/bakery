import rich.traceback as RichTraceback

RichTraceback.install(show_locals=True)

# Adapted From:
# Question: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet
# User: https://stackoverflow.com/users/10827766/shadowrylander

import sys

from oreo import ModuleCaller

from bakery.frosting import frosting
from bakery.milcery import milcery
from bakery.order_cancelled import get_exc_from_name


class bakery(ModuleCaller):
    def __call__(self, *args, **kwargs):
        if args or kwargs:
            return milcery(*args, **kwargs)
        else:
            return milcery

    def __getattr__(self, program_):
        if program_.startswith("_"):
            raise AttributeError(program_)
        else:
            try:
                if program_ in ("frosting",):
                    return eval(program_)
                elif program_.startswith("OrderCancelled"):
                    return get_exc_from_name(program_)
                    # return getattr(OrderCancelled, program_)
                    # exec(f"class {program_}(OrderCancelled): pass")
                    # return eval(program_)
                else:
                    return milcery(program_=program_)
            except Exception as e:
                raise e.__class__(e) from e

    bakery = __call__
    __all__ = [var for var in vars() if var not in ("__qualname__",)]


sys.modules[__name__] = bakery()
