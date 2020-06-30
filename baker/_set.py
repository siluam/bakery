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
		_calling = True,
		_final = False,
		_subcommand = "command",
		_reset = False,
		**kwargs,
	):
		self.__args = args
		self.__kwargs = kwargs
		self.__cls = _cls
		self.__subcommand = _subcommand
		self.__add_replace = _add_replace
		self.__baking = _baking
		self.__calling = _calling
		self.__final = _final

		if _reset:
			self.__reset()
		else:
			self.__set()

	def __reset(self):
		for c1 in ("_settings", "_command"):
			for c2 in ("called", "final"):
				del getattr(self, c1)[c2]
		del self._sub
		for key, value in self._settings.defaults.items():
			if getattr(self.__cls, key, None) != value:
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

			for key in self.__kwargs.keys():
				if key[0] == "_":
					self._settings[
						"baked" if self.__baking else "called"
					][self.__subcommand][key] = self.__kwargs.pop(key)

		else:

			# for key, value in self._settings.defaults.items():
			# 	if getattr(self.__cls, key, None) != value:
			# 		setattr(self.__cls, key, value)

			# Careful! The order of the categories here matters!
			for category in (
				"defaults",
				"baked",
				"category",
			):
				self._settings.final[self.__subcommand].extend(D(self._settings[category]))

	def __kwargs_mods(self):
		self.__frosting()

		if self.__kwargs.get("_print", False):
			self.__kwargs["_str"] = bool(self.__kwargs.get("_print", False))

		if self._sub.unprocessed == "shell_":
			if self.__kwargs.get("_shell", False):
				self.__kwargs["_shell"] = True

		if self._sub.unprocessed == "str_":
			if self.__kwargs.get("_str", False):
				self.__kwargs["_str"] = True

	def __frosting(self):
		if self._sub.unprocessed in ("frosting_", "f_"):
			if self.__kwargs.get("_frosting", False):
				self.__kwargs["_frosting"] = True

		if self.__kwargs.get("_frosting", False):
			if (
				self.__kwargs.get("_capture", "stdout") == "run" or
				self._capture == "run"
			):
				raise cannot_frost_and_run('Sorry! You can\'t use both the "capture = run" and "frosting" options!')
			self.__kwargs["_type"] = iter