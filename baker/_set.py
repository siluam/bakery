# From Imports
from addict import Dict as D
from toml import load

class Error(Exception):
	pass


class cannot_set_multiple(Error):
	pass


class _set:
	def _set(
		self,
		*args,
		_cls = None,
		_baking = False,
		_calling = False,
		_final = False,
		_subcommand = "supercalifragilisticexpialidocious",
		_setup = False,
		_reset = False,
		_apply = False,
		**kwargs,
	):
		self.__args = args
		self.__kwargs = kwargs
		self.__cls = _cls if _cls is not None else self
		self.__subcommand = _subcommand
		self.__baking = _baking
		self.__calling = _calling
		self.__final = _final

		if _setup:

			self.__set_defaults()

		elif _reset:

			self.__cls._sub = D({})
			for c1 in ("_settings", "_command"):
				for c2 in ("called", "final"):
					getattr(self.__cls, c1)[c2] = D({})
			self.__set_defaults()

		elif _apply:

			for key, value in self.__cls._settings.final[self.__subcommand].items():
				setattr(self.__cls, key, value)

		else:
			self.__set()
			return self.__args, self.__kwargs, self.__cls

	def __set_defaults(self):
		for key, value in self.__cls._settings.defaults.items():
			setattr(self.__cls, key, value)

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

			_ = dict()

			for key in self.__kwargs.keys():
				if key[0] == "_":
					self.__cls._settings[
						"baked" if self.__baking else "called"
					][self.__subcommand][key] = self.__kwargs[key]
				else:
					_[key] = self.__kwargs[key]

			self.__kwargs = D(_)

		elif self.__final:
			self.__cls._settings.final[self.__subcommand].update(
				D(self.__cls._settings.defaults)
			)
			if self.__subcommand != "supercalifragilisticexpialidocious":
				self.__cls._settings.final[self.__subcommand].update(
					D(self.__cls._settings.baked.supercalifragilisticexpialidocious)
				)

			# Careful! The order of the categories here matters!
			for category in (
				"baked",
				"called",
			):
				self.__cls._settings.final[self.__subcommand].update(
					D(self.__cls._settings[category][self.__subcommand])
				)

	def __kwargs_mods(self):
		self.__kwargs_based()
		self.__subcommand_based()

	def __kwargs_based(self):
		self.__frosting()

		if self.__kwargs.get("_print", False):
			self.__kwargs["_str"] = bool(self.__kwargs.get("_print", False))

	def __frosting(self):
		if self.__cls._sub.unprocessed in ("frosting_", "f_"):
			if self.__kwargs.get("_frosting", False):
				self.__kwargs["_frosting"] = True
			self.__kwargs["_type"] = iter

	def __subcommand_based(self):
		if self.__cls._sub.unprocessed == "shell_":
			if self.__kwargs.get("_shell", False):
				self.__kwargs["_shell"] = True

		if self.__cls._sub.unprocessed == "str_":
			if self.__kwargs.get("_str", False):
				self.__kwargs["_str"] = True
