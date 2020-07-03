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
	def __init__(self, program: str):
		super().__init__(program)
		"""
			Answer: https://stackoverflow.com/questions/11813287/insert-variable-into-global-namespace-from-within-a-function/39937010#39937010
			User: https://stackoverflow.com/users/1397061/1
		"""
		try:
			builtins.bakeriy_stores.append(self)
		except AttributeError:
			builtins.bakeriy_stores = [self]

	def _(self, *args, **kwargs):
		self._sub.unprocessed = "command"
		args, kwargs = self._set_and_process(*args, **kwargs)
		return self._return_frosted_output(*args, **kwargs)

	@property
	def __call__(self, *args, **kwargs):
		return partial(
			self.__class__,
			self.program,
			*self._args,
			_baked_commands = D(self._command.baked),
			_baked_settings = D(self._settings.baked),
			**self._kwargs,
		)

def __getattr__(program):
	"""
		Answer 1: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56786875#56786875
		User 1:   https://stackoverflow.com/users/1016216/l3viathan

		Answer 2: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56795585#56795585
		User 2:   https://stackoverflow.com/users/3830997/matthias-fripp

		Modified by me
	"""
	if program == "__path__":
		raise AttributeError

	try:
		return i(program)
	except Exception as e:
		return e
