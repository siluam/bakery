# Imports
import builtins

# From Imports
from addict import Dict as D
from collections import namedtuple
from functools import partial
from gensing import tea
from nanite import module_installed, fullpath
from typing import MutableSequence as MS, Dict, Any, Tuple, Union

_milcery = module_installed(
	fullpath("_milcery.py", f_back=2)
)._milcery

default: Tuple[None] = namedtuple("default", "")

class i(_milcery):
	def __init__(
		self,
		_program: str,
		*args,
		_baked_commands = None,
		_baked_settings = None,
		**kwargs,
	):
		super().__init__(
			_program,
			*args,
			_baked_commands = _baked_commands or D({}),
			_baked_settings = _baked_settings or D({}),
			**kwargs,
		)
		"""
			Answer: https://stackoverflow.com/questions/11813287/insert-variable-into-global-namespace-from-within-a-function/39937010#39937010
			User: https://stackoverflow.com/users/1397061/1
		"""
		try:
			builtins.bakeriy_stores.append(self)
		except AttributeError:
			builtins.bakeriy_stores = [self]

		self.__output = None

	def __enter__(self):
		return self.__output := self.__partial_class(*args, **kwargs)

	def __exit__(self, exc_type, exc_val, exc_tb):
		try:
			pass
		finally:
			self.__output = None

	def _(self, *args, **kwargs):
		try:
			return self.__class(*args, **kwargs)
		finally:
			self._set(_reset = True)

	@property
	def __call__(self, *args, **kwargs):
		return self.__partial_class(*args, **kwargs)

def __getattr__(_program):
	"""
		Answer 1: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56786875#56786875
		User 1:   https://stackoverflow.com/users/1016216/l3viathan

		Answer 2: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56795585#56795585
		User 2:   https://stackoverflow.com/users/3830997/matthias-fripp

		Modified by me
	"""
	if _program == "__path__":
		raise AttributeError

	try:
		return i(_program)
	except Exception as e:
		return ("i", e)
