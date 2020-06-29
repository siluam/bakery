# From Imports
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

		if _reset:
			self.__reset()
		else:
			self.__set()

	def __reset(self):
		del self._settings.current
		del self._command.current
		for key, value in self._settings.defaults.items():
			if getattr(self.__cls, key, None) != value:
				setattr(self.__cls, key, value)

	def __set(self):

		if (
			(_baking and _calling) or
			(_baking and _final) or
			(_calling and _final) or
			(_baking and _calling and _final)
		):
			raise cannot_set_multiple('Sorry! No combination of _baking, _calling, or _final may be used! Please choose only a single category!')

		self.__kwargs_mods()

		if _baking or _calling:
			for key in self.__kwargs.keys():
				if key[0] == "_":
					self._settings[
						"baked" if _baking else "called"
					][self.__subcommand] = self.__kwargs.pop(key)
		else:
			for key, value in self._settings.defaults.items():
				if getattr(self.__cls, key, None) != value:
					setattr(self.__cls, key, value)
			for key, value in self._settings.baked[self.__subcommand].items():
				if getattr(self.__cls, key, None) != value:
					setattr(self.__cls, key, value)
			for key, value in self._settings.called[self.__subcommand].items():
				if getattr(self.__cls, key, None) != value:
					setattr(self.__cls, key, value)

	def __kwargs_mods(self):
		self.__frosting()

		if self.__kwargs.get("_print", False):
			self.__kwargs["_str"] = bool(self.__kwargs.get("_print", False))

		if self._command.current.sub.unprocessed == "shell_":
			if self.__kwargs.get("_shell", False):
				self.__kwargs["_shell"] = True

		if self._command.current.sub.unprocessed == "str_":
			if self.__kwargs.get("_str", False):
				self.__kwargs["_str"] = True

	def __frosting(self):
		if self._command.current.sub.unprocessed in ("frosting_", "f_"):
			if self.__kwargs.get("_frosting", False):
				self.__kwargs["_frosting"] = True

		if self.__kwargs.get("_frosting", False):
			if (
				self.__kwargs.get("_capture", "stdout") == "run" or
				self._capture == "run"
			):
				raise cannot_frost_and_run('Sorry! You can\'t use both the "capture = run" and "frosting" options!')
			self.__kwargs["_type"] = iter