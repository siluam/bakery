# Imports
import weakref

# From Imports
from addict import Dict as D
from autoslot import SlotsMeta
from collections import defaultdict
from functools import partial, wraps
from gensing import tea, frosting
from itertools import chain
from nanite import (
	module_installed,
	fullpath,
	mixinport,
)
from os import environ
from textwrap import TextWrapper
from typing import (
	List,
	Tuple,
	Dict,
	MutableSequence as MS,
	Any,
	Generator,
	Union,
)

mixins: Generator[str, None, None] = (
	fullpath(f"{mixin}.py", f_back=2)
	for mixin in (
		"_alt_property_vars",
		"_create_command",
		"_funky_properties",
		"_long_property_vars",
		"_process_args_kwargs",
		"_return_output",
		"_run_frosting",
		"_set",
		"_short_property_vars",
		"baking_",
	)
)

class _melcery(SlotsMeta):
	"""
		Answer 1: https://stackoverflow.com/questions/128573/using-property-on-classmethods/1800999#1800999
		User 1: https://stackoverflow.com/users/36433/a-coady

		Answer 2: https://stackoverflow.com/questions/31379485/1-class-inherits-2-different-metaclasses-abcmeta-and-user-defined-meta/31537249#31537249
		User 2: https://stackoverflow.com/users/302343/timur
	"""

	@property
	def stores_(cls):
		return cls._stores

	@stores_.setter
	def stores_(cls, value):
		"""
			Answer: https://stackoverflow.com/questions/328851/printing-all-instances-of-a-class/328882#328882
			User: https://stackoverflow.com/users/9567/torsten-marek
		"""
		if isinstance(value, list):
			cls._stores = None
		else:
			if cls._stores is None:
				cls._stores = [value]
			else:
				cls._stores.append(value)

	def __init__(cls, *args, **kwargs):
		cls.stores_ = []

class _milcery(metaclass = _melcery, *(mixinport(mixins))):
	def __init__(
		self,
		*args,
		_program: str = None,
		_freezer: str = None,
		_baked_commands: Dict[str, Any] = None,
		_baked_settings: Dict[str, Any] = None,
		**kwargs,
	):
		"""
			Answer: https://stackoverflow.com/questions/26626653/class-variable-access-in-all-class-method/26626707#26626707
			User: https://stackoverflow.com/users/100297/martijn-pieters
		"""
		self.__class__.stores_ = weakref.ref(self, self)

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
		self._program: str = _program or ""
		self._freezer: str = _freezer or ""

		self._command = D({})
		self._command.baked = _baked_commands or D({})

		self._settings = D({})
		self._settings.baked = _baked_settings or D({})
		self._settings.defaults: Dict[str, Any] = {
			"_type": iter,
			"_capture": "stdout",
			"_run": False,
			"_shell": None,
			"_frosting": False,
			"_str": False,
			"_ignore_stderr": False,
			"_ignore_stdout": False,
			"_verbosity": int(environ.get("verbose_bakery", 0)),
			"_run_as": "",
			"_n_lines": D(
				{
					"ordinal": "first",
					"number": None,
					"std": "stdout",
				}
			),
			"_kwarg_one_dash": False,
			"_fixed_key": False,
			"_print": False,
			"_tiered": False,
			# This setting will use a single forward slash instead of a dash for options
			"_dos": False,
			# If set to True, _capture = "run" will wait for the process to finish before
			# returning an addict dictionary of values depending on "_return" and "_verbosity"
			# If set to False, _capture = "run" will return the sarge Pipeline object
			# If set to None, _capture = "run" will wait for the process to finish
			# before returning None
			"_wait": True,
			"_timeout": None,
			"_input": None,
			# Dict must be in the form {"i" : user} or {"s" : user}, to use or not use the
			# configuration files of the specified user
			"_sudo": dict(),
			# If "_frozen" has a truthy value, freeze this bakery object such that another bakery object
			# may act on it; else keep it active
			"_frozen": False,
			# A dictionary used to pass options to the subprocess Popen class
			"_popen": dict(),
			# Chunk size used when reading with _capture = "run"
			"_chunk_size": 512,
			"_regular_args": tuple(),
			"_decorator": False,
		}

		self._sub = D({})
		self._subcommand = "supercalifragilisticexpialidocious"

		self._is_bakery_object = True

		self._captures: Tuple[str] = (
			"stdout",
			"stderr",
			"both",
			"run",
		)

		# Update these
		self._return_categories: Tuple[str] = (
			"stdout",
			"stderr",
			"return_code",
			"return_codes",
			"command",
			"tea",
			"verbosity",
		)

		sa = kwargs.pop("_starter_args", [])
		ska = kwargs.pop("_starter_kwargs", dict())
		self._args = list(args) + list(
			[sa]
			if isinstance(sa, (str, bytes, bytearray))
			else list(sa)
		)
		kwargs.update(ska)
		self._kwargs = kwargs

	def _convert_to_generator(self, input):
		yield from input

	def _convert_to_type(self, input, _type=iter):

		if input is None:
			return "None" if _type.__name__ in ("str", "repr") else None

		if input and isinstance(input, frosting):
			if isinstance(input(), (str, bytes, bytearray)):
				input = [
					TextWrapper(
						break_long_words=False,
						break_on_hyphens=False,
					).fill(input())
				]
			elif input() is None:
				return "None" if _type.__name__ in ("str", "repr") else None
			elif isinstance(input(), int):
				if _type.__name__ in ("str", "repr"):
					return repr(input())
				else:
					return input()

		if _type.__name__ in ("str", "repr"):
			return "\n".join(input)
		elif _type.__name__ in ("generator", "iter", "chain"):
			return self._convert_to_generator(input)
		else:
			return _type(input)

	def _subcommand_check(self, subcommand):
		if subcommand[-1] == "_":
			self._sub.function = f"_{subcommand}"
			self._sub.unprocessed = (
				self._subcommand
			)
		elif subcommand == self._subcommand:
			self._sub.unprocessed = (
				self._subcommand
			)
		else:
			self._sub.unprocessed = subcommand
			self._sub.processed = subcommand.replace("_", "-")

	"""
		From: https://realpython.com/primer-on-python-decorators/
	"""
	def __call__(
		self,
		*dargs,
		_func = None,
		_partial = False,
		_rab = None,
		_raa = None,
		_sa = None,
		_sk = None,
		**dwargs,
	):
		_partial = self.__class__.__name__ == "i"
		if dwargs.get("_decorator", False) or dwargs.get("_d", False):
			def wrapper(func):
				@wraps(func)
				def wrapped(*args, **kwargs):
					return self._classes(
						_partial = _partial,
						_starter_args = _sa or [],
						_starter_kwargs = _sk or dict(),
						_regular_args = chain(
							_rab or [],
							[func(*args, **kwargs)],
							_raa or [],
						),
						_regular_kwargs = dwargs,
					)
				return wrapped
			if _func is None:
				return wrapper
			else:
				return wrapper(_func)
		else:
			for dwarg in (f"_{kw}" for kw in ("func", "rab", "raa", "sa", "sk")):
				dwargs.pop(dwarg, None)
			return self._classes(*dargs, _partial = _partial, **dwargs)

	def __getattr__(self, subcommand):
		def inner(
			*dargs,
			_func = None,
			_partial = False,
			_rab = None,
			_raa = None,
			_sa = None,
			_sk = None,
			**dwargs,
		):
			_partial = self.__class__.__name__ == "i"
			if dwargs.get("_decorator", False) or dwargs.get("_d", False):
				def wrapper(func):
					@wraps(func)
					def wrapped(*args, **kwargs):
						return self._classes(
							_partial = _partial,
							subcommand = subcommand,
							_starter_args = _sa or [],
							_starter_kwargs = _sk or dict(),
							_regular_args = chain(
								_rab or [],
								[func(*args, **kwargs)],
								_raa or [],
							),
							_regular_kwargs = dwargs,
						)
					return wrapped
				if _func is None:
					return wrapper
				else:
					return wrapper(_func)
			else:
				for dwarg in (f"_{kw}" for kw in ("func", "rab", "raa", "sa", "sk")):
					dwargs.pop(dwarg, None)
				return self._classes(*dargs, _partial = _partial, subcommand = subcommand, **dwargs)
		return inner

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		pass

	def _classes(
		self,
		*args,
		_partial = False,
		subcommand = "supercalifragilisticexpialidocious",
		**kwargs
	):
		if _partial:
			return partial(
				self.__class__,
				_program=self._program,
				*args,
				_baked_commands=D(self._command.baked),
				_baked_settings=D(self._settings.baked),
				**kwargs,
			)
		else:
			try:
				self._subcommand_check(
					kwargs.pop("_subcommand", subcommand)
				)
				self._set_and_process(*args, **kwargs)
				return self._return_frosted_output()
			finally:
				self._set(_reset=True)

	def _set_and_process(self, *args, **kwargs):

		self._set(_setup=True)

		set_with_sub = partial(
			self._set, _subcommand=self._sub.unprocessed
		)

		self._args, self._kwargs = set_with_sub(
			*self._args, _calling=True, **self._kwargs,
		)

		args, kwargs = set_with_sub(
			*args, _calling=True, **kwargs,
		)

		set_with_sub(_final=True,)

		set_with_sub(_apply=True,)

		process_with_sub = partial(
			self._process_args_kwargs,
			_subcommand=self._sub.unprocessed,
		)

		process_with_sub(
			*self._args,
			_calling=True,
			_starter_regular="starter",
			**self._kwargs,
		)

		process_with_sub(
			*args,
			_calling=True,
			_starter_regular="regular",
			**kwargs,
		)

		process_with_sub(_final=True,)

	def __deepcopy__(self):
		return self.__class__(
			_program=self._program,
			_freezer=self._freezer,
			_baked_commands=D(self._command.baked),
			_baked_settings=D(self._settings.baked),
		)

	def __iter__(self):
		self.n = 0

		self._subcommand_check(
			self._subcommand
		)
		self._set_and_process()

		if isinstance(
			output := self._return_frosted_output(), dict,
		):
			self.__next_output = list(
				output[
					"stderr"
					if self._capture == "stderr"
					else "stdout"
				]
			)
		elif isinstance(output, (str, bytes, bytearray)):
			self.__next_output = [output]
		else:
			self.__next_output = list(output)

		return self

	def __next__(self):
		if self.n < len(self.__next_output):
			self.n += 1
			return self.__next_output[self.n - 1]
		else:
			raise StopIteration

	def __str__(self):
		return self._classes(_type = str)

	def __repr__(self):
		return self._classes(_type = repr)

	def __assign_to_frozen(self, pr, value, reversed=False):

		# Remember: "value" has already had its "_program" attribute added with its full command
		# Since "value" has already been frozen, but is no longer so,
		# its own "_program" attribute has also already been modified
		
		frozen_dict = {
			"out" : self._settings.defaults["_ignore_stdout"],
			"err" : self._settings.defaults["_ignore_stderr"],
		}

		def inner(value):
			if isinstance(value, (str, bytes, bytearray)):
				return value
			elif isinstance(value, (tea, frosting)):
				return value()
			else:
				try:
					assert (
						getattr(value, "_is_bakery_object", False)
						is True
					)
				except AssertionError:
					raise TypeError(
						f"Sorry! {value} must be a string, bytes, bytearray, tea, frosting, or bakeriy object!"
					)
				else:
					# CAREFUL! The order of the categories in the top loop must not change here!
					# The values of "frozen_dict" are meant to be overwritten!
					for cat in ("planetary", "baked"):
						for std in ("out", "err"):
							if value._settings[cat][self._subcommand][f"_ignore_std{std}"]:
								frozen_dict[std] = value._settings[cat][self._subcommand][f"_ignore_std{std}"]
					return value._program

		if isinstance(value, tuple):
			if pr in ("<", ">", ">>"):
				if len(value) == 0:
					pass
				elif len(value) == 1:
					processed_value = inner(value[0])
				elif len(value) == 2:
					if isinstance(value[0], int) or "&" in value[0]:
						processed_value = inner(value[1])
						pr = str(value[0]) + pr
					else:
						processed_value = inner(value[0])
						pr += str(value[1])
				else:
					processed_value = inner(value[1])
					pr = f"{value[0]}{pr}{value[2]}"
		else:
			processed_value = inner(value)

		if "&>" in pr:
			frozen_dict["out"] = True
			frozen_dict["err"] = True
		elif "2>" in pr:
			frozen_dict["err"] = True
		elif (
			"1>" in pr or
			pr in (">", ">>", "<", "| tee", "| tee -a")
		):
			frozen_dict["out"] = True

		if ">&1" in pr:
			frozen_dict["out"] = True
		elif ">&2" in pr:
			frozen_dict["err"] = True

		partially_frozen = partial(
			self.__class__,
			_baked_settings=D({self._subcommand : dict(
				_ignore_stdout = frozen_dict["out"],
				_ignore_stderr = frozen_dict["err"],
			)}),
			_frozen = True,
		)

		program = [self._freezer, pr, processed_value]
		frozen = partially_frozen(
			_program = " ".join(program[::-1] if reversed else program)
		)

		return frozen(_partial = False)

	def __or__(self, value):
		return self.__assign_to_frozen("|", value)

	def __ror__(self, value):
		return self.__assign_to_frozen("|", value, reversed=True)

	def __xor__(self, value):
		return self.__assign_to_frozen("| tee", value)

	def __rxor__(self, value):
		return self.__assign_to_frozen("| tee", value, reversed=True)

	def __add__(self, value):
		return self.__assign_to_frozen("| tee -a", value)

	def __radd__(self, value):
		return self.__assign_to_frozen("| tee -a", value, reversed=True)

	def __lshift__(self, value):
		return self.__assign_to_frozen("<", value)

	def __lt__(self, value):
		return self.__assign_to_frozen("<", value)

	def __rlshift__(self, value):
		return self.__assign_to_frozen("<", value, reversed=True)

	def __rshift__(self, value):
		return self.__assign_to_frozen(">", value)

	def __gt__(self, value):
		return self.__assign_to_frozen(">", value)

	def __rrshift__(self, value):
		return self.__assign_to_frozen(">", value, reversed=True)

	def __matmul__(self, value):
		return self.__assign_to_frozen(">>", value)

	def __rmatmul__(self, value):
		return self.__assign_to_frozen(">>", value, reversed=True)
