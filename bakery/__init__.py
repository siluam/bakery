import rich.traceback
rich.traceback.install()

import hy

from shutil import which as which_

from .bakery import milcery as milcery_

def __getattr__(program_):
    if program_ == "__path__":
        raise AttributeError
    elif program_ == "steakery":
        return milcery_
    elif which_(program_):
        return milcery_(program_ = program_)
    else:
        raise AttributeError
