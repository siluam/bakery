"""
	Inspired by https://amoffat.github.io/sh/
"""

# From Imports
from functools import partial
from nanite import module_installed, fullpath

i = module_installed(fullpath("i.py", f_back = 2))
y = module_installed(fullpath("y.py", f_back = 2))

def __getattr__(_program):
	"""
		Answer 1: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56786875#56786875
		User 1:   https://stackoverflow.com/users/1016216/l3viathan

		Answer 2: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56795585#56795585
		User 2:   https://stackoverflow.com/users/3830997/matthias-fripp
	"""
	if _program == "__path__":
		raise AttributeError

	try:
		return y.y(_program = _program)
	except Exception as e:
		return e