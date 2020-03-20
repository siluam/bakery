# Imports
import builtins

# From Imports
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
		_cake: Union[None, tea] = None,
		_soufle: Union[None, tea] = None,
		_after_cake: Union[None, tea] = None,
		_ignore_check: bool = False,
		_bake_args: MS[Any] = (),
		_bake_kwargs: Dict[str, Any] = default(),
		_bake_after_args: MS[Any] = (),
		_bake_after_kwargs: Dict[str, Any] = default(),
		sparse = False,
		**kwargs,
	):
		super().__init__(
			program,
			_cake,
			_soufle,
			_after_cake,
			_ignore_check,
			_bake_args,
			_bake_kwargs._asdict() if isinstance(_bake_kwargs, default) else _bake_kwargs,
			_bake_after_args,
			_bake_after_kwargs._asdict() if isinstance(_bake_after_kwargs, default) else _bake_after_kwargs,
			*args,
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

	@property
	def _(self):
		current_kwarg_settings: Dict[str, Any] = {}
		for key, value in self._kwarg_settings.items():
			if getattr(self, f"_{key}") != value:
				current_kwarg_settings[f"_{key}"] = getattr(self, f"_{key}")

		return partial(
			i,
			self.program,
			_cake = self.cake,
			_soufle = self.soufle,
			_after_cake = self.after_cake,
			_bake_kwargs = current_kwarg_settings,
		)

	def __call__(self, *args, **kwargs):
		return self._run_frosting(args, kwargs)

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
		return e