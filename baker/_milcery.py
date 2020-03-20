# From Imports
from addict import Dict as D
from autoslot import Slots
from gensing import tea
from nanite import (
	check_type,
	module_installed,
	fullpath,
	mixinport,
)
from os import environ
from typing import (
	List,
	Tuple,
	Dict,
	MutableSequence as MS,
	Any,
	Generator,
	Union,
)

mixins: Generator[str, None, None] = (fullpath(f"{mixin}.py", f_back = 2) for mixin in (
	"_attach_command_args_kwargs",
	"_create_command",
	"_funky_properties",
	"_long_property_vars",
	"_return_output",
	"_run_frosting",
	"_set",
	"_short_property_vars",
	"baking_",
	"tier_",
))

class _getattr_(tea, Slots):
	def __init__(self, output, capture = "stdout"):
		super().__init__(output)
		self.output = self.items(whole = True, addict = True)
		self.capture = "stderr" if capture == "stderr" else "stdout"
	def __iter__(self):
		self.n = 0
		self.next_output = tuple(getattr(self.output, self.capture))
		return self
	def __next__(self):
		if self.n < len(self.next_output):
			self.n += 1
			return self.next_output[self.n - 1]
		else:
			raise StopIteration
	@property
	def __getattr__(self, attr):
		return getattr(self.output, attr)
	def __repr__(self):
		return repr(self.output)
	def __call__(self):
		return self.output

class _milcery(*(mixinport(mixins))):

	"""
		Answer: https://stackoverflow.com/questions/26315584/apply-a-function-to-all-instances-of-a-class/26315625#26315625
		User: https://stackoverflow.com/users/625914/behzad-nouri
	"""

	def __init__(
		self,
		program: str,
		_cake: Union[None, tea],
		_soufle: Union[None, tea],
		_after_cake: Union[None, tea],
		_ignore_check: bool,
		_bake_args: MS[Any],
		_bake_kwargs: Dict[str, Any],
		_bake_after_args: MS[Any],
		_bake_after_kwargs: Dict[str, Any],
		*args,
		**kwargs,
	):
		"""
			_type can be any type, such as:
			* iter
			* list
			* tuple
			* set
			* frozenset
			
			There are two ways to put arguments at the end of the command:
			1. Use the "_end_args" keyword argument in the function call
			2. Bake them in using any of the baking methods below

			A good way to debug commands is to see what the command actually was, using the "_str"
			keyword argument.
		"""
		self._ignore_check: bool = _ignore_check

		"""

		"""
		self._kwarg_settings: Dict[str, Any] = {
			"type": iter,
			"capture": "both",
			"before_args": [],
			"before_kwargs": {},
			"end_args": [],
			"end_kwargs": {},
			"shell": False,
			"frosting": False,
			"str": False,
			"ignore_stderr": False,
			"kwargs": {},
			"args": [],
			"verbosity": int(
				environ.get("verbose_bakery", 0)
			),
			"from_file": "",
			"run_as": "",
			"n_lines": D(
				{
					"ordinal": "first",
					"number": None,
					"std": "both",
				}
			),
			"kwarg_one_dash": False,
			"fixed_key": False,
			"return": "verbosity",
			"print": False,
		}
		self._non_underscored_properties: Tuple[str] = (
			"program",
			"stores",
		)

		# Returns the default allowed types and adds "str" as well
		self._allowed_type_names: List[str] = check_type(
			lst=True
		) + ["str"]

		self._captures: Tuple[str] = (
			"stdout",
			"stderr",
			"both",
			"run",
		)
		self._shells: List[str] = [
			"zsh",
			"bash",
			"sh",
			"fish",
			"xonsh",
			"elvish",
			"tcsh",
			"powershell",
			"cmd",
		]
		self._return_categories: Tuple[str] = (
			"stdout",
			"stderr",
			"return_code",
			"return_codes",
			"command",
			"args",
			"kwargs",
			"gensing",
			"verbosity",
		)
		self.program: str = program
		self.cake: type = tea() if _cake is None else _cake
		self.soufle: type = tea() if _soufle is None else _soufle
		self.after_cake: type = tea() if _after_cake is None else _after_cake
		self.tiered: type = tea()

		for key, value in self._kwarg_settings.items():
			setattr(self, f"_{key}", value)
			setattr(self, f"__temp_{key}", None)
		self._shell = (
			True if self.program in self._shells else False
		)

		if isinstance(_bake_args, (str, bytes, bytearray)):
			_bake_args = (_bake_args,)
		if isinstance(_bake_after_args, (str, bytes, bytearray)):
			_bake_after_args = (_bake_after_args,)
		self.bake_(*_bake_args, **_bake_kwargs)
		self.bake_after_(*_bake_after_args, **_bake_after_kwargs)

		self._before_args = args
		self._before_kwargs = kwargs

	def _debug_output(self, _key, __temp_key):
		print(_key, ":", getattr(self, _key))
		print(__temp_key, ":", getattr(self, __temp_key))

	def _reset_all(self):
		for key in self._kwarg_settings.keys():

			__temp_key_value = getattr(self, __temp_key := f"__temp_{key}")

			if getattr(self, _key := f"_{key}") != __temp_key_value:
				if __temp_key_value is None:
					pass
				else:
					setattr(self, _key, __temp_key_value)

			setattr(self, __temp_key, None)

	def __getattr__(self, subcommand):
		def inner(*args, **kwargs):
			if subcommand == "shell_":
				if "_shell" not in kwargs.keys():
					kwargs["_shell"] = True
			elif subcommand == "str_":
				if "_str" not in kwargs.keys():
					kwargs["_str"] = True
			elif subcommand in ["frosting_", "f_"]:
				if "_frosting" not in kwargs.keys():
					kwargs["_frosting"] = True
			elif subcommand == "pipe_":
				args = [f"| {_}" for _ in args]
			else:
				new_sub = subcommand.replace("_", "-")
				if self._shell:
					kwargs["_end_command"] = (
						new_sub
						if kwargs.get("_sub_before_shell", False)
						else f"-c '{new_sub}"
					)
				else:
					kwargs["_end_command"] = new_sub
				kwargs["_subcommand"] = True
			return _getattr_(self._run_frosting(args, kwargs), self._capture)
		return inner

	def __iter__(self):
		self.n = 0
		self.__next_output = tuple(getattr(
			self._run_frosting([], {}),
			"stderr" if self._capture == "stderr" else "stdout"
		))
		return self

	def __next__(self):
		if self.n < len(self.__next_output):
			self.n += 1
			return self.__next_output[self.n - 1]
		else:
			raise StopIteration

	def redirect_(self, last_arg, *args, redr_in=None, **kwargs):
		"""
			("[command]", "[redirect_type]")
			redirect types cannot include "<" types, such as "here-documents", "here-strings", etc.
		"""

		args, kwargs = self._set(self, args, kwargs)

		new_args = [f" {_[0]} {_[1]}" for _ in args]
		new_args.append(f" {last_arg}")
		new_kwargs = {
			key: value
			for key, value in kwargs.items()
			if key in self._kwarg_settings
		}
		# if using run, convert this to use feeding
		_redr_in = f"cat {redr_in} | " if redr_in else ""
		new_kwargs["_beg_command"] = _redr_in
		return self._run_frosting(new_args, new_kwargs)

	def add_types_(self, *args):
		self._allowed_type_names = (
			self._allowed_type_names + list(args)
		)

	def add_shells_(self, *args):
		self._shells = self._shells + list(args)
