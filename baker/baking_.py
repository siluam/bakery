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


class baking_:

	def bake_(
		self,
		*args,
		_cls = None,
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

		_cls = _cls if _cls is not None else self

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
		_cls = None,
		_akar = "add",
		_sar = "add",
		_sc = "command",
		_sr = "regular",
		**kwargs
	):
		for store in _cls.stores:
			store.bake_(
				*args,
				_cls = _cls,
				_akar = _akar,
				_sar = _sar,
				_sc = _sc,
				_sr = _sr,
				**kwargs
			)

	def splat_(
		self,
		_cls = None,
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

		_cls = _cls if _cls is not None else self

		def inner(category):
			if _all:
				getattr(_cls, category).baked = D({})
			elif _all_subcommands:
				for key in getattr(_cls, category).baked.keys():
					if key != "command":
						getattr(_cls, category).baked[key] = D({})
			else:
				for sub in _subcommands:
					getattr(_cls, category).baked[sub] = D({})

		if _settings and _args_kwargs:
			for category in ("_settings", "_command"):
				inner(category)
		else:
			inner(_settings if _settings else _args_kwargs)

	def splat_all_(
		self,
		_cls = None,
		_all = False,
		_all_subcommands = False,
		_subcommands = ["command"],
		_settings = False,
		_args_kwargs = False,
	):
		for store in _cls.stores:
			store.splat_(
				_cls = _cls,
				_all = _all,
				_all_subcommands = _all_subcommands,
				_subcommands = _subcommands,
				_settings = _settings,
				_args_kwargs = _args_kwargs,
			)