import rich.traceback as _rt
_rt.install()

import hy

from .bakery import milcery as _milcery

def __getattr__(program_):
    if program_ == "__path__":
        raise AttributeError
    elif program_ == "steakery":
        return _milcery
    else:
        return _milcery(program_ = program_)
