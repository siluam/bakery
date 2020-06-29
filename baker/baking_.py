# Imports
import builtins

# From Imports
from copy import deepcopy
from gensing import tea
from typing import Dict, Union, Tuple

genstring = Union[str, tea]

class Error(Exception):
	pass


class not_same_type(Error):
	pass

################################################################################################

class baking_:

	def bake_(
		self,
		*args,
		_cls = self,
		_akar = "add",
		_sar = "add",
		_subcommand = "command",
		**kwargs
	):
		"""

			_ct: command type
				* ck: command kwargs
				* scaa: any subcommand args
				* scba: linked subcommand args
				* scaka: any subcommand kwargs, then args
				* scbka: linked subcommand kwargs, then args

			_akar: args and kwargs add or replace
				* add: adds to the currently baked args and kwargs
				* replace: replaces the currently baked args and kwargs

			_sar: settings add or replace
				* add: adds to the currently baked settings
				* replace: replaces the currently baked settings

		"""

		if _sar == "add":
			pass
		elif _sar == "replace":
			self._settings.current.baked[sub].baked = tea()

		if _akar == "add":
			pass
		elif _akar == "replace":
			self._command.current.baked[sub].baked = tea()

	def splat_(
		self,
		_all = False,
		_all_subcommands = False,
		_subcommands = ["command"],
		_settings = False,
		_args_kwargs = True
	):
		"""

			splat_(_all = True):
				Removes all baked args, kwargs, and settings for both the main command and
				subcommands
				Eg: git.splat_(_all = True)

			splat(_subcommands = ["subcommand"]):
				Removes all baked args, kwargs, and settings for just the subcommands
				in the list
				Eg: git.splat_(_subcommands = ["status"])

			splat(_subcommands = ["command"]):
				The default; removes all baked args, kwargs, and settings for the main command
				Eg: git.splat_(_subcommands = ["command"])

		"""
		def inner(category):
			if _all:
				delattr(getattr(self, category), baked)
			elif _all_subcommands:
				for key in getattr(self, category).baked.keys():
					if key != "command":
						delattr(getattr(self, category).baked, key)
			else:
				for sub in _subcommands:
					delattr(getattr(self, category).baked, sub)

		if _settings and _args_kwargs:
			for category in ("_settings", "_command"):
				inner(category)
		else:
			inner(_settings if _settings else _args_kwargs)

	def splat_all_(
		self,
		_all = False,
		_all_subcommands = False,
		_subcommands = ["command"],
		_settings = False,
		_args_kwargs = True
	):
		for store in self.stores:
			store.splat_(_all, _all_subcommands, _subcommands, _settings, _args_kwargs)

################################################################################################

class baking_:

	def _bake_cake(
		self, cls, args, kwargs, _after_cake=False, _keep=True
	):
		args, kwargs = self._set(cls, args, kwargs, _baking=True)

		_ = self._attach_command_args_kwargs(
			(
				self.after_cake if _after_cake else self.cake
			) if _keep else tea(), args, kwargs
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

	# DONE
	def bake_replacement_(self, *args, **kwargs):
		replacement: type = self._attach_command_args_kwargs(tea(), args, kwargs)
		for index, kv in self.cake.items(indexed = True).items():
			if kv.value == replacement[0].value:
				self.cake[f"values:{index}":] = replacement.values()

	# DONE
	def remove_slice_(self, *args, **kwargs):
		replacement: type = self._attach_command_args_kwargs(tea(), args, kwargs)
		for index, kv in self.cake.items(indexed = True).items():
			if kv.value == replacement[0].value:
				del self.cake[index:]

	def bake_all_(self, *args, **kwargs):
		for store in self.stores:
			store.bake_(*args, **kwargs)

	# DONE
	def bake_all_replacement_(self, *args, **kwargs):
		for store in self.stores:
			store.bake_replacement_(*args, **kwargs)

	# DONE
	def remove_all_slices_(self, *args, **kwargs):
		for store in self.stores:
			store.remove_slice_(*args, **kwargs)

	def bake_after_(self, *args, **kwargs):
		self._bake_cake(self, args, kwargs, _after_cake=True)

	# DONE
	def bake_after_replacement_(self, *args, **kwargs):
		replacement: type = self._attach_command_args_kwargs(tea(), args, kwargs)
		for index, kv in self.after_cake.items(indexed = True).items():
			if kv.value == replacement[0].value:
				self.after_cake[f"values:{index}":] = replacement.values()

	# DONE
	def remove_after_slice_(self, *args, **kwargs):
		replacement: type = self._attach_command_args_kwargs(tea(), args, kwargs)
		for index, kv in self.after_cake.items(indexed = True).items():
			if kv.value == replacement[0].value:
				del self.after_cake[index:]

	def bake_after_all_(self, *args, **kwargs):
		for store in self.stores:
			store.bake_after_(*args, **kwargs)

	# DONE
	def bake_after_all_replacement_(self, *args, **kwargs):
		for store in self.stores:
			store.bake_after_replacement_(*args, **kwargs)

	# DONE
	def remove_after_all_slices_(self, *args, **kwargs):
		for store in self.stores:
			store.remove_after_slice_(*args, **kwargs)

	def soubake_(
		self,
		*args: Tuple[Dict[genstring, genstring]],
		**kwargs: Dict[genstring, genstring]
	):
		"""

			Bake a subcommand; whenever that subcommand is used, it will be replaced by the command provided instead.

		"""
		# Merge a tuple of dictionaries and a single dictionary kwargs
		if args and not all(isinstance(argument, (dict, tea)) for argument in args):
			raise not_same_type("Sorry! All arguments must be dictionaries or gensings!")
		total_args = (argument if isinstance(argument, dict) else argument.items(whole = True) for argument in args)
		self.soufle = tea(*total_args, kwargs)

	# DONE
	def soubake_replacement_(self, *args, **kwargs):
		replacement: type = self._attach_command_args_kwargs(tea(), args, kwargs)
		for index, kv in self.soufle.items(indexed = True).items():
			if kv.value == replacement[0].value:
				self.soufle[f"values:{index}":] = replacement.values()

	# DONE
	def remove_souslice_(self, *args, **kwargs):
		replacement: type = self._attach_command_args_kwargs(tea(), args, kwargs)
		for index, kv in self.soufle.items(indexed = True).items():
			if kv.value == replacement[0].value:
				del self.soufle[index:]

	def soubake_all_(self, *args, **kwargs):
		for store in self.stores:
			store.soubake_(*args, **kwargs)

	# DONE
	def soubake_all_replacement_(self, *args, **kwargs):
		for store in self.stores:
			store.soubake_replacement_(*args, **kwargs)

	# DONE
	def remove_all_souslices_(self, *args, **kwargs):
		for store in self.stores:
			store.remove_souslice_(*args, **kwargs)

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
			keep=False,
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
			_after_cake=self.__shell_cake(
				self, kwargs.pop("_bake", False)
			),
			_keep=True,
		)