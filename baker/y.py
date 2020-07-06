# Imports
import builtins

# From Imports
from addict import Dict as D
from collections import namedtuple
from functools import partial
from gensing import tea
from nanite import module_installed, fullpath
from typing import MutableSequence as MS, Dict, Any, Tuple, Union

_milcery = module_installed(fullpath("_milcery.py", f_back = 2))._milcery
i = module_installed(fullpath("i.py", f_back = 2)).i

default: Tuple[None] = namedtuple("default", "")

class y(_milcery):
	def __init__(
		self,
		program: str,
		*args,
		_baked_commands = D({}),
		_baked_settings = D({}),
		**kwargs,
	):
		super().__init__(
			program,
			*args,
			_baked_commands = _baked_commands,
			_baked_settings = _baked_settings,
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

	def __call__(self, *args, **kwargs):
		self._subcommand_check(kwargs.pop("_subcommand", "supercalifragilisticexpialidocious"))
		self._set_and_process(*args, **kwargs)
		return self._return_frosted_output()

	@property
	def _(self, *args, **kwargs):
		return partial(
			self.__class__,
			self.program,
			*args,
			_baked_commands = D(self._command.baked),
			_baked_settings = D(self._settings.baked),
			**kwargs,
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

	bakeri_menu = (
        "git",
    )

	bakeriy = i if program in bakeri_menu else y

	try:
		return bakeriy(program)
	except Exception as e:
		return ("y sent to i" if program in bakeri_menu else "y", e)