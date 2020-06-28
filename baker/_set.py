# From Imports
from toml import load

class Error(Exception):
	pass


class cannot_frost_and_run(Error):
	pass


class cannot_set_multiple(Error):
	pass


################################################################################################

class _set:
	def _set(
		self,
		*args,
		_cls = self,
		_baking = False,
		_calling = True,
		_final = False,
		_subcommand = False,
		_bake_type = "scaka",
		_bake_add_replace = "add",
		**kwargs,
	):
		self.__args = args
		self.__kwargs = kwargs
		self.__cls = _cls
		self.__subcommand = _subcommand
		self.__bake_type = _bake_type

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
					self.settings.cakes[self.__bake_type].baked[key] = value
		elif _calling:
			for key, value in self.__kwargs.items():
				if key[0] == "_":
					self.settings.cakes[self.__bake_type].called[key] = value
		elif _final:
			for key, value in self.settings.defaults.items():
				setattr(self.__cls, key, value)
			for key, value in self.settings.cakes[self.__bake_type].baked.items():
				setattr(self.__cls, key, value)
			for key, value in self.settings.cakes[self.__bake_type].called.items():
				setattr(self.__cls, key, value)

	def _reset_all(self, _bt = "scaka"):
		for key in self.settings.cakes.keys():
			del self.settings.cakes[key].called
			del self.settings.cakes[key].final
		for key, value in self.settings.defaults.items():
			setattr(self.__cls, key, value)
		for key, value in self.settings.cakes[_bt].baked.items():
			setattr(self.__cls, key, value)

################################################################################################

# class _set:
# 	def _set(self, cls, args, kwargs, _baking=False):

# 		for key in self.__cls._kwarg_settings.keys():
# 			# TODO: Explain this
# 			_key = f"_{key}"
# 			__temp_key = f"__temp_{key}"
# 			if _key in self.__kwargs.keys():
# 				if not _baking:
# 					setattr(
# 						self.__cls,
# 						__temp_key,
# 						getattr(self.__cls, _key),
# 					)
# 				setattr(
# 					self.__cls,
# 					_key,
# 					self.__kwargs.pop(
# 						_key,
# 						getattr(
# 							self.__cls,
# 							_key if _baking else __temp_key,
# 						),
# 					),
# 				)
# 		return self.__args, self.__kwargs

# 	def _reset_all(self):
# 		for key in self._kwarg_settings.keys():

# 			__temp_key_value = getattr(self, __temp_key := f"__temp_{key}")

# 			if getattr(self, _key := f"_{key}") != __temp_key_value:
# 				if __temp_key_value is None:
# 					pass
# 				else:
# 					setattr(self, _key, __temp_key_value)

# 			setattr(self, __temp_key, None)
