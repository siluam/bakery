# From Imports
from addict import Dict as D
from box import Box
from gensing import tea, frosting
from itertools import chain
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
	"_create_command",
	"_funky_properties",
	"_long_property_vars",
	"_process_args_kwargs",
	"_return_output",
	"_run_frosting",
	"_set",
	"_short_property_vars",
	"baking_",
	"tier_",
))

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
		_partial = False,
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

			A good way to debug commands is to see what the command actually was, using the "_str"
			keyword argument.
		"""
		self._ignore_check: bool = _ignore_check

		self._command = D({})

		"""

		"""
		self._settings = D({})
		self._settings.defaults: Dict[str, Any] = Box({
			"_type": iter,
			"_capture": "stdout",
			"_command_kwargs": {},
			"_starter_args": [],
			"_shell": False,
			"_frosting": False,
			"_str": False,
			"_ignore_stderr": False,
			"_kwargs": {},
			"_args": [],
			"_verbosity": int(
				environ.get("verbose_bakery", 0)
			),
			"_run_as": "",
			"_n_lines": D(
				{
					"ordinal": "first",
					"number": None,
					"std": "out",
				}
			),
			"_kwarg_one_dash": False,
			"_fixed_key": False,
			"_return": "verbosity",
			"_print": False,
		}, frozen_box = True)
		for key, value in self._settings.defaults.items():
			if getattr(self.__cls, key, None) != value:
				setattr(self.__cls, key, value)
		self._settings.functions = (
			"frosting_",
			"f_",
			"shell_",
			"str_",
		)

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
		if _partial:
			self.remove_slice_(*args, **kwargs)
			# self.remove_souslice_(*args, **kwargs)

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

		self._command_kwargs = kwargs

	def _debug_output(self, _key, __temp_key):
		print(_key, ":", getattr(self, _key))
		print(__temp_key, ":", getattr(self, __temp_key))

	# DONE: Something's wrong with this, or returning the generator created by this
	# DONE: Always remember a generator is used up
	def __convert_to_generator(self, input):
		yield from input

	def _convert_to_type(self, input, _type):
		if _type.__name__ == "str":
			return " ".join(input)
		if _type.__name__ in ("generator", "iter"):
			return self.__convert_to_generator(input)
		else:
			return _type(input)

	def __getattr__(self, subcommand):
		def inner(*args, **kwargs):
			self._command.current.sub.unprocessed = subcommand
			# if subcommand == "pipe_":
			# 	args = [f"| {_}" for _ in args]
			if subcommand in self._settings.functions:
				pass
			else:
				new_sub = subcommand.replace("_", "-")
				if self._shell:
					self._command.current.sub.processed = (
						new_sub
						if kwargs.get("_sub_before_shell", False)
						else f"-c '{new_sub}"
					)
				else:
					self._command.current.sub.processed = new_sub
				if subcommand in chain(self._command.baked.keys(), self._settings.baked.keys()):
					self._command.current.sub.baked = True

			# DONE: Change to account for the new return methods
			if isinstance(output := self._run_frosting(args, kwargs), (dict, tea, frosting)):
				return frosting(output, self._capture)
			else:
				# DONE: _convert_to_type isn't working here because _run_frosting resets
				#  all properties, including _type; find an alternative
				return self._convert_to_type(frosting(output), type(output))

		return inner

	def __iter__(self):
		self.n = 0

		# TODO: Change to account for the new return methods
		if isinstance(output := self._run_frosting([], {}), (dict, tea, frosting)):
			self.__next_output = list(getattr(
				output,
				"stderr" if self._capture == "stderr" else "stdout"
			))
		else:
			self.__next_output = list(output)

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
