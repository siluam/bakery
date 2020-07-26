# From Imports
from addict import Dict as D
from collections import OrderedDict, ChainMap
from gensing import tea, frosting
from itertools import chain
from toml import load

class Error(Exception):
	pass


class cannot_set_multiple(Error):
	pass


class _set:
	def _set(
		self,
		*args,
		_cls = None,
		_global = False,
		_baking = False,
		_calling = False,
		_final = False,
		_subcommand = "supercalifragilisticexpialidocious",
		_setup = False,
		_reset = False,
		_apply = False,
		**kwargs,
	):

		self.__args = args
		self.__kwargs = kwargs
		self.__cls = self._cls_check(_cls)
		self.__subcommand = _subcommand
		self.__global = _global
		self.__baking = _baking
		self.__calling = _calling
		self.__final = _final

		if _setup:
			
			self.__set_defaults()

		elif _reset:

			self.__cls._sub = D({})
			for c1 in ("_settings", "_command"):
				for c2 in ("called", "final"):
					getattr(self.__cls, c1)[c2] = D({})
			self.__set_defaults()

		elif _apply:

			for key, value in self.__cls._settings.final[self.__subcommand].items():
				setattr(self.__cls, key, value)

		else:
			self.__set()

			if self.__cls == self:
				return self.__args, self.__kwargs
			else:
				return self.__args, self.__kwargs, self.__cls

	def __set_defaults(self):
		for key, value in self.__cls._settings.defaults.items():
			setattr(self.__cls, key, value)

	def __set(self):

		categories = OrderedDict({
			"planetary" : self.__global,
			"baked" : self.__baking,
			"called" : self.__calling,
			"final" : self.__final,
		})

		bategories = tuple(categories.values())

		c_count = bategories.count(True)

		if c_count != 1:
			raise cannot_set_multiple(f'Sorry! No combination of {", ".join(categories.keys())} may be used! Please choose only a single category!')

		self.__kwargs_mods()

		if any(bategories[:-1]):

			_ = dict()

			for key, value in tuple(categories.items())[:-1]:
				if value:
					cat = key

			for index, arg in enumerate(self.__args):
				if not isinstance(
					arg,
					(str, bytes, bytearray, int, dict, tea, frosting)
				) and not arg:
					self.__cls._settings[cat][self.__subcommand]._frozen = True
					self.__args = list(self.__args)
					del self.__args[index]

			for key in self.__kwargs.keys():
				if key[0] == "_":
					self.__cls._settings[cat][self.__subcommand][key] = self.__kwargs[key]
				else:
					_[key] = self.__kwargs[key]

			self.__kwargs = D(_)

		else:
			self.__cls._settings.final[self.__subcommand].update(
				D(self.__cls._settings.defaults)
			)
			if self.__subcommand != "supercalifragilisticexpialidocious":
				self.__cls._settings.final[self.__subcommand].update(D(ChainMap(
					self.__cls._settings.planetary.supercalifragilisticexpialidocious,
					self.__cls._settings.baked.supercalifragilisticexpialidocious,
				)))

			# Careful! The order of the categories here matters!
			for category in tuple(categories.keys())[:-1]:
				self.__cls._settings.final[self.__subcommand].update(
					D(self.__cls._settings[category][self.__subcommand])
				)

	def __kwargs_mods(self):

		if self.__cls._sub.function in ("frosting_", "f_"):
			self.__kwargs["_frosting"] = True

		if self.__cls._sub.function == "print_":
			self.__kwargs["_print"] = True