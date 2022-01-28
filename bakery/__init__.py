# Bakery Frontend

# Adapted from the entirety of [[https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet][this question]]:


# [[file:__init__.org::*Bakery Frontend][Bakery Frontend:1]]
import hy
from bakery import bakery

def __getattr__(program_):
    if program_ == "__path__":
        raise AttributeError
    return bakery(program_ = program_)
# Bakery Frontend:1 ends here
