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
		_sc = "command",
		_sr = "regular",
		**kwargs
	):
		"""

			_akar: args and kwargs add or replace
				* add: adds to the currently baked args and kwargs
				* replace: replaces the currently baked args and kwargs

			_sar: settings add or replace
				* add: adds to the currently baked settings
				* replace: replaces the currently baked settings

			_sc: subcommand
				* command: will act on the main command
			
			_sr: starter or regular args and / or kwargs

		"""

		if _akar == "replace":
			_cls._command.baked[_subcommand] = tea()

		if _sar == "replace":
			_cls._settings.baked[_subcommand] = tea()

		args, kwargs, _cls = self._set(
			*args,
			_cls = _cls,
			_baking = True,
			_subcommand = _sc,
			**kwargs,
		)

		_cls = self._process_args_kwargs(
			*args,
			_cls = _cls,
			_baking = True,
			_subcommand = _sc,
			_starter_regular = _sr,
			**kwargs,
		)

		return _cls

	def bake_all_(
		self,
		*args,
		_cls = self,
		_akar = "add",
		_sar = "add",
		_sc = "command",
		_sr = "regular",
		**kwargs
	):
		for store in self.stores:
			store.bake_(
				*args,
				_cls = _cls,
				_akar = _akar,
				_sar = _sar,
				_sc = "command",
				_sr = "regular",
				**kwargs
			)

	def splat_(
		self,
		_all = False,
		_all_subcommands = False,
		_subcommands = ["command"],
		_settings = False,
		_args_kwargs = False,
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
		_args_kwargs = False,
	):
		for store in self.stores:
			store.splat_(
				_all = _all,
				_all_subcommands = _all_subcommands,
				_subcommands = _subcommands,
				_settings = _settings,
				_args_kwargs = _args_kwargs,
			)

	def fresh_(
		self,
		*args,
		_akar = "add",
		_sar = "add",
		_sc = "command",
		_sr = "regular",
		**kwargs
	):
		"""
			Create a new version of this instance with the given args, kwargs, and settings
			baked in
		"""

		new_bakery = self.__class__(self.program)

		return self.bake_(
			*args,
			_cls = new_bakery,
			_akar = _akar,
			_sar = _sar,
			_sc = _sc,
			_sr = _sr,
			**kwargs,
		)

	def duped_(
		self,
		*args,
		_akar = "add",
		_sar = "add",
		_sc = "command",
		_sr = "regular",
		**kwargs
	):
		"""
			Create a copy of this instance with the original arguments plus the new arguments
		"""

		new_bakery = deepcopy(self)

		return self.bake_(
			*args,
			_cls = new_bakery,
			_akar = _akar,
			_sar = _sar,
			_sc = _sc,
			_sr = _sr,
			**kwargs,
		)

################################################################################################

class baking_:

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

	# DONE
	def bake_all_replacement_(self, *args, **kwargs):
		for store in self.stores:
			store.bake_replacement_(*args, **kwargs)

	# DONE
	def remove_all_slices_(self, *args, **kwargs):
		for store in self.stores:
			store.remove_slice_(*args, **kwargs)