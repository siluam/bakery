# From Imports
from toml import load

class Error(Exception):
	pass


class cannot_frost_and_run(Error):
	pass


class _set:
	def _set(self, cls, args, kwargs, _baking=False):

		self.__cls = cls
		self.__args = args
		self.__kwargs = kwargs

		# if "_drive_through" in self.__kwargs.keys():
		if self.__kwargs.get("_drive_through", False):
			self.__drive_through()

		if "_frosting" in self.__kwargs.keys():
			self.__frosting()

		if "_print" in self.__kwargs.keys():
			self.__print()

		# if "_from_file" in self.__kwargs.keys():
		if self.__kwargs.get("_from_file", ""):
			self.__from_file()

		for key in self.__cls._kwarg_settings.keys():
			# TODO: Explain this
			_key = f"_{key}"
			__temp_key = f"__temp_{key}"
			if _key in self.__kwargs.keys():
				if not _baking:
					setattr(
						self.__cls,
						__temp_key,
						getattr(self.__cls, _key),
					)
				setattr(
					self.__cls,
					_key,
					self.__kwargs.pop(
						_key,
						getattr(
							self.__cls,
							_key if _baking else __temp_key,
						),
					),
				)
		return self.__args, self.__kwargs

	def __drive_through(self):
		"""
			Drive Through:
				Allows for baking and running the command in one go;
				for users who don't want to write that one extra line.

			TODO: Give an example of this
		"""
		_ = self.__kwargs.pop("_drive_through")
		_args = _.pop("args", ())
		_kwargs = _.pop("kwargs", {})
		_after_args = _.pop("after_args", ())
		_after_kwargs = _.pop("after_kwargs", {})
		self._bake_cake(self, _args, _kwargs, _after_cake=False)
		self._bake_cake(
			self, _after_args, _after_kwargs, _after_cake=True
		)

	def __from_file(self):
		"""
			Uses a toml file

			TODO: Create an example of this
		"""
		self.__args = list(self.__args)
		self._from_file = load(self.__kwargs.pop("_from_file"))
		for arg in self._from_file["args"]:
			self.__args.append(arg)
		for key, value in self._from_file["kwargs"].items():
			if key not in self.__kwargs.keys():
				self.__kwargs[key] = value

	def __frosting(self):
		# Can't be put in a property as it needs "kwargs", which is local to this scope only
		if self.__kwargs.get("_frosting", False):
			if (
				self.__kwargs.get("_capture", "stdout") == "run" or
				self._capture == "run"
			):
				raise cannot_frost_and_run('Sorry! You can\'t use both the "capture = run" and "frosting" options!')
			self.__kwargs["_type"] = iter
		else:
			self.__kwargs.get("_type", iter)

	def __print(self):
		self.__kwargs["_str"] = bool(self.__kwargs.get("_print", False))
