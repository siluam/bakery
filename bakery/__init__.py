# Import Hy


# [[file:__init__.org::*Import Hy][Import Hy:1]]
import hy
# Import Hy:1 ends here

# Relative Import

# Adapted from [[https://stackoverflow.com/users/799163/remcogerlich][RemcoGerlich's]] answer [[https://stackoverflow.com/a/21139466][here]]:


# [[file:__init__.org::*Relative Import][Relative Import:1]]
from .bakery import milcery as notToBeConfusedWithMilcery
# Relative Import:1 ends here

# Rest of __init__


# [[file:__init__.org::*Rest of __init__][Rest of __init__:1]]
def __getattr__(program_):
    if program_ == "__path__":
        raise AttributeError
    elif program_ == "steakery":
        return notToBeConfusedWithMilcery
    else:
        return notToBeConfusedWithMilcery(program_ = program_)
# Rest of __init__:1 ends here
