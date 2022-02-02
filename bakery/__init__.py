import rich.traceback
rich.traceback.install()

import hy

from shutil import which as notToBeConfusedWithWhich

from .bakery import milcery as notToBeConfusedWithMilcery

def __getattr__(program_):
    if program_ == "__path__":
        raise AttributeError
    elif program_ == "steakery":
        return notToBeConfusedWithMilcery
    elif notToBeConfusedWithWhich(program_):
        return notToBeConfusedWithMilcery(program_ = program_)
    else:
        raise AttributeError
