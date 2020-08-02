# From Imports
from addict import Dict as D
from collections import namedtuple
from functools import partial, wraps
from nanite import module_installed, fullpath
from subprocess import Popen
from typing import MutableSequence as MS, Dict, Any, Tuple, Union

_milcery = module_installed(fullpath("_milcery.py", f_back = 2))._milcery

i = module_installed(fullpath("i.py", f_back = 2)).i

default: Tuple[None] = namedtuple("default", "")

class y(_milcery):
	def __init__(
		self,
		*args,
		_program: str = None,
		_baked_commands: Dict[str, Any] = None,
		_baked_settings: Dict[str, Any] = None,
		**kwargs,
	):
		super().__init__(
			*args,
			_program = _program or "",
			_baked_commands = _baked_commands or D({}),
			_baked_settings = _baked_settings or D({}),
			**kwargs,
		)

	def __call__(self, *args, **kwargs):
		def wrapper(func = None):
			@wraps(func)
			def wrapped():
				if func is None:
					return self._classes(*args, **kwargs)
				else:
					return self._classes(func(*args, **kwargs))
			return wrapped
		return wrapper

	@property
	def __(self, *args, **kwargs):
		return self._classes(*args, _partial = True, **kwargs)

ext_ = partial(
	module_installed(fullpath("extensions.py", f_back = 2)).ext_,
	y,
)

def __getattr__(_program):
	"""
		Answer 1: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56786875#56786875
		User 1:   https://stackoverflow.com/users/1016216/l3viathan

		Answer 2: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56795585#56795585
		User 2:   https://stackoverflow.com/users/3830997/matthias-fripp
	"""
	if _program == "__path__":
		raise AttributeError

	bakeri_menu = (
        "git",
    )

	bakeriy = i if _program in bakeri_menu else y

	try:
		return bakeriy(_program = _program)
	except Exception as e:
		return ("y sent to i" if _program in bakeri_menu else "y", e)