# From Imports
from copy import deepcopy
from nanite import gensing

class baking_:

	def _bake_cake(
		self, cls, args, kwargs, _cutter=False, _after_cake=False
	):

		args, kwargs = self._set(cls, args, kwargs, _baking=True)

		_ = self._attach_command_args_kwargs(
			self.cake if _cutter else gensing(), args, kwargs
		)

		if _after_cake:
			cls.after_cake = _
		else:
			cls.cake = _

		return cls

	def __shell_cake(self, cls, _bake_bool):

		if _bake_bool:
			_after_cake_temp = False
		else:
			if cls._shell:
				_after_cake_temp = True
			else:
				_after_cake_temp = False

		return _after_cake_temp

	def bake_(self, *args, **kwargs):
		self._bake_cake(self, args, kwargs, _after_cake=False)

	def bake_after_(self, *args, **kwargs):
		self._bake_cake(self, args, kwargs, _after_cake=True)

	def dale_(self, *args, **kwargs):
		"""
			Create a new version of this instance with the given arguments baked in
		"""

		new_bakery = self.__class__(self.program)

		# TODO: Set up a way to set both the "_cake" and "_after_cake" values at the same time
		return self._bake_cake(
			new_bakery,
			args,
			kwargs,
			_after_cake=self.__shell_cake(
				self, kwargs.pop("_bake", False)
			),
		)

	def cutter_(self, *args, **kwargs):
		"""
			Create a copy of this instance with the original arguments plus the new arguments
		"""

		# Change these
		new_bakery = deepcopy(self)

		# TODO: Set up a way to set both the "_cake" and "_after_cake" values at the same time
		return self._bake_cake(
			new_bakery,
			args,
			kwargs,
			_cutter=True,
			_after_cake=self.__shell_cake(
				self, kwargs.pop("_bake", False)
			),
		)

	def splat_(self):
		"""

			Disable the default settings; refer to the "bake_" function for more information.

		"""
		# Reset the kwarg settings values; refer to the "_kwarg_settings" class variable for more
		# information.
		for key, value in self._kwarg_settings.items():
			setattr(self, f"_{key}", value)

		# Reset the cake values
		self.cake = gensing()
		self.after_cake = gensing()