# From Imports
from addict import Dict as D
from toml import load

class Error(Exception):
	pass


class cannot_frost_and_run(Error):
	pass


class cannot_set_multiple(Error):
	pass


class _set:
	def _set(
		self,
		*args,
		_cls = self,
		_baking = False,
		_calling = False,
		_final = False,
		_subcommand = "command",
		_reset = False,
		_apply = False,
		**kwargs,
	):
		self.__args = args
		self.__kwargs = kwargs
		self.__cls = _cls
		self.__subcommand = _subcommand
		self.__baking = _baking
		self.__calling = _calling
		self.__final = _final

		if _reset:

			del self.__cls._sub
			for c1 in ("_settings", "_command"):
				for c2 in ("called", "final"):
					del getattr(self.__cls, c1)[c2]
			for key, value in self.__cls._settings.defaults.items():
				if getattr(self.__cls, key, None) != value:
					setattr(self.__cls, key, value)

		elif _apply:

			for key, value in self._settings.final[self.__subcommand].items():
				if getattr(self.__cls, key, None) != value:
					setattr(self.__cls, key, value)

		else:
			self.__set()
			return self.__args, self.__kwargs, self.__cls

	def __set(self):

		if (
			(self.__baking and self.__calling) or
			(self.__baking and self.__final) or
			(self.__calling and self.__final) or
			(self.__baking and self.__calling and self.__final)
		):
			raise cannot_set_multiple('Sorry! No combination of _baking, _calling, or _final may be used! Please choose only a single category!')

		self.__kwargs_mods()

		if self.__baking or self.__calling:

			for key in self.__kwargs.keys():
				if key[0] == "_":
					self.__cls._settings[
						"baked" if self.__baking else "called"
					][self.__subcommand][key] = self.__kwargs.pop(key)

		else:
			self.__cls._settings.final[self.__subcommand].extend(
				D(self.__cls._settings.defaults)
			)

			# Careful! The order of the categories here matters!
			for category in (
				"baked",
				"category",
			):
				self.__cls._settings.final[self.__subcommand].extend(
					D(self.__cls._settings[category][self.__subcommand])
				)

	def __kwargs_mods(self):
		self.__kwargs_based()
		self.__subcommand_based()

	def __kwargs_based(self):
		self.__frosting()

		if self.__kwargs.get("_print", False):
			self.__kwargs["_str"] = bool(self.__kwargs.get("_print", False))

		if self.__kwargs.get("_starter_args", []):
			self.__cls = self._process_args_kwargs(
				*self.__kwargs.pop("_starter_args"),
				_cls = self.__cls,
				_calling = True,
				_subcommand = self.__subcommand,
				_starter_regular = "starter",
			)

		if self.__kwargs.get("_starter_kwargs", {}):
			self.__cls = self._process_args_kwargs(
				_cls = self.__cls,
				_calling = True,
				_subcommand = self.__subcommand,
				_starter_regular = "starter",
				**self.__kwargs.pop("_starter_kwargs"),
			)

	def __frosting(self):
		if self.__cls._sub.unprocessed in ("frosting_", "f_"):
			if self.__kwargs.get("_frosting", False):
				self.__kwargs["_frosting"] = True

		if self.__kwargs.get("_frosting", False):
			if (
				self.__kwargs.get("_capture", "stdout") == "run" or
				self.__cls._capture == "run"
			):
				raise cannot_frost_and_run('Sorry! You can\'t use both the "capture = run" and "frosting" options!')

			self.__kwargs["_type"] = iter

	def __subcommand_based(self):
		if self.__cls._sub.unprocessed == "shell_":
			if self.__kwargs.get("_shell", False):
				self.__kwargs["_shell"] = True

		if self.__cls._sub.unprocessed == "str_":
			if self.__kwargs.get("_str", False):
				self.__kwargs["_str"] = True