# From Imports
from addict import Dict as D
from collections import namedtuple
from functools import partial
from itertools import chain
from nanite import module_installed, fullpath
from typing import MutableSequence as MS, Dict, Any, Tuple, Union

_milcery = module_installed(
	fullpath("_milcery.py", f_back=2)
)._milcery

default: Tuple[None] = namedtuple("default", "")

class i(_milcery):
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

	def __(self, *args, **kwargs):
		return self._classes(*args, **kwargs)

	@property
	def __call__(
		self,
		*args,
		_rab = None,
		_raa = None,
		_sa = None,
		_sk = None,
		_rk = None,
		**kwargs
	):

		def func_check(_func = None):
			return _func

		if (func := func_check()) is None:
			return self._classes(*args, _partial = True, **kwargs)
		else:
			def wrapper():
				@wraps(func)
				def wrapped():
					return self._classes(
						_partial = True,
						_starter_args = _sa or [],
						_starter_kwargs = _sk or dict(),
						_regular_args = chain(
							_rab or [],
							[func(*args, **kwargs)],
							_raa or [],
						),
						_regular_kwargs = _rk or dict(),
					)
				return wrapped
			return wrapper

ext_ = partial(
	module_installed(fullpath("extensions.py", f_back = 2)).ext_,
	i,
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

	try:
		return i(_program = _program)
	except Exception as e:
		return ("i", e)
