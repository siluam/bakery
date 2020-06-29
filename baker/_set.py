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
		_subcommand = False,
		_command_type = "scaka",
		_bake_add_replace = "add",
		_reset = False,
		**kwargs,
	):
		self.__args = args
		self.__kwargs = kwargs
		self.__cls = _cls
		self.__subcommand = _subcommand
		self.__command_type = _command_type

		if _reset:
			self.__reset()
		else:
			self.__set()

	def __reset(self):
		for key in self._settings.cakes.keys():
			del self._settings.cakes[key].called
			del self._settings.cakes[key].final
		for key, value in self._settings.defaults.items():
			if getattr(self.__cls, key, None) != value:
				setattr(self.__cls, key, value)
		for key, value in self._settings.cakes[self.__command_type].baked.items():
			if getattr(self.__cls, key, None) != value:
				setattr(self.__cls, key, value)
		del self._command.sub.bool
		del self._command.sub.baked

	def __set(self):

		if (
			(_baking and _calling) or
			(_baking and _final) or
			(_calling and _final) or
			(_baking and _calling and _final)
		):
			raise cannot_set_multiple('Sorry! No combination of _baking, _calling, or _final may be used! Please choose only a single category!')

		if self.__kwargs.get("_frosting", False):
			if (
				self.__kwargs.get("_capture", "stdout") == "run" or
				self._capture == "run"
			):
				raise cannot_frost_and_run('Sorry! You can\'t use both the "capture = run" and "frosting" options!')
			self.__kwargs["_type"] = iter

		if self.__kwargs.get("_print", False):
			self.__kwargs["_str"] = bool(self.__kwargs.get("_print", False))

		if _baking:
			for key, value in self.__kwargs.items():
				if key[0] == "_":
					self._settings.cakes[self.__command_type].baked[key] = value
		elif _calling:
			for key, value in self.__kwargs.items():
				if key[0] == "_":
					self._settings.cakes[self.__command_type].called[key] = value
		elif _final:
			for key, value in self._settings.defaults.items():
				if getattr(self.__cls, key, None) != value:
					setattr(self.__cls, key, value)
			for key, value in self._settings.cakes[self.__command_type].baked.items():
				if getattr(self.__cls, key, None) != value:
					setattr(self.__cls, key, value)
			for key, value in self._settings.cakes[self.__command_type].called.items():
				if getattr(self.__cls, key, None) != value:
					setattr(self.__cls, key, value)