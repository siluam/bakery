# From Imports
from addict import Dict as D
from copy import deepcopy
from functools import partial
from gensing import tea
from itertools import chain
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
		_sc = "supercalifragilisticexpialidocious",
		_sr = "regular",
		_g = False,
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
				* supercalifragilisticexpialidocious: will act on the main command
			
			_sr: starter or regular args and / or kwargs

			_g: whether to affect the global args, kwargs, or settings

		"""

		_cls = self._cls_check(_cls)

		if _akar == "replace":
			_cls._command["planetary" if _g else "baked"][_subcommand] = D({})

		if _sar == "replace":
			_cls._settings["planetary" if _g else "baked"][_subcommand] = D({})

		self._set(_setup = True)

		self_set = partial(
			self._set,
			*args,
			_cls = _cls,
			_baking = not(_g),
			_global = _g,
			_subcommand = _sc,
			**kwargs,
		)

		# Since args, kwargs, and potentially _cls are modified, and then unpacked into the following
		# partial, this and the similar check below said partial must remain separate.
		if _cls == self:
			args, kwargs = self_set()
		else:
			args, kwargs, _cls = self_set()

		self_pak = partial(
			self._process_args_kwargs,
			*args,
			_cls = _cls,
			_baking = not(_g),
			_global = _g,
			_subcommand = _sc,
			_starter_regular = _sr,
			**kwargs,
		)

		if _cls == self:
			self_pak()
		else:
			_cls = self_pak()
			return _cls

	def bake_all_(
		self,
		*args,
		_akar = "add",
		_sar = "add",
		_sr = "regular",
		**kwargs
	):
		for store in self.chain_:
			store.bake_(
				*args,
				_g = True,
				_cls = store,
				_akar = _akar,
				_sar = _sar,
				_sr = _sr,
				**kwargs
			)

	def splat_(
		self,
		_cls = None,
		_all = False,
		_all_subcommands = False,
		_subcommands = ["supercalifragilisticexpialidocious"],
		_settings = False,
		_args_kwargs = False,
		_global = False,
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

			splat(_subcommands = ["supercalifragilisticexpialidocious"]):
				The default; removes all baked args, kwargs, and settings for the main command
				Eg: git.splat_(_subcommands = ["supercalifragilisticexpialidocious"])

		"""

		_cls = self._cls_check(_cls)

		def inner(category):
			if _all:
				getattr(_cls, category)["planetary" if _global else "baked"] = D({})
			elif _all_subcommands:
				for key in getattr(_cls, category)["planetary" if _global else "baked"].keys():
					if key != "supercalifragilisticexpialidocious":
						getattr(_cls, category)["planetary" if _global else "baked"][key] = D({})
			else:
				for sub in _subcommands:
					getattr(_cls, category)["planetary" if _global else "baked"][sub] = D({})

		if _settings and _args_kwargs:
			for category in ("_settings", "_command"):
				inner(category)
		else:
			inner("_settings" if _settings else "_command")

	def splat_all_(
		self,
		_all = False,
		_all_subcommands = False,
		_settings = False,
		_args_kwargs = False,
	):
		for store in self.chain_:
			store.splat_(
				_cls = store,
				_all = _all,
				_all_subcommands = _all_subcommands,
				_settings = _settings,
				_args_kwargs = _args_kwargs,
				_global = True,
			)

	def _cls_check(self, _cls):
		return _cls or self
