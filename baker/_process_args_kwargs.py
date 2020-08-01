# From Imports
from addict import Dict as D
from collections import OrderedDict
from itertools import chain
from os import name as os_name
from typing import Union, Any
from gensing import tea, frosting

class _process_args_kwargs:

	def _process_args_kwargs(
		self,
		*args,
		_cls = None,
		_global = False,
		_baking = False,
		_calling = False,
		_final = False,
		_subcommand = "supercalifragilisticexpialidocious",
		_starter_regular = "regular",
		**kwargs,
	):
		self.__args = args
		self.__kwargs = kwargs
		self.__cls = self._cls_check(_cls)
		self.__global = _global
		self.__baking = _baking
		self.__calling = _calling
		self.__final = _final
		self.__subcommand = _subcommand
		self.__starter_regular = _starter_regular

		self.__categories = OrderedDict({
			"planetary" : self.__global,
			"baked" : self.__baking,
			"called" : self.__calling,
			"final" : self.__final,
		})

		for key, value in tuple(self.__categories.items())[:-1]:
			if value:
				self.__cat = key

		c_count = tuple(value for value in self.__categories.values()).count(True)

		if c_count != 1:
			raise TypeError(
				f'Sorry! No combination of {", ".join(self.__categories.keys())} may be used! Please choose only a single category!'
			)

		for cat in self.__categories.keys():
			for ak in ("args", "kwargs"):
				for sr in ("starter", "regular"):
					if not self.__cls._command[cat][self.__subcommand].components[ak][sr]:
						self.__cls._command[cat][self.__subcommand].components[ak][sr] = tea()

		if self.__final:
			for ak in ("args", "kwargs"):
				for sr in ("starter", "regular"):
					for cat in tuple(self.__categories.keys())[:-1]:
						self.__cls._command.final[self.__subcommand].components[ak][sr].extend(
							*self.__cls._command[cat][self.__subcommand].components[ak][sr]
						)

			if self.__subcommand != "supercalifragilisticexpialidocious":
				if not self.__cls._command.planetary.supercalifragilisticexpialidocious.components.kwargs.starter:
					self.__cls._command.planetary.supercalifragilisticexpialidocious.components.kwargs.starter = tea()
				if not self.__cls._command.baked.supercalifragilisticexpialidocious.components.kwargs.starter:
					self.__cls._command.baked.supercalifragilisticexpialidocious.components.kwargs.starter = tea()
				self.__cls._command.final[self.__subcommand].components.kwargs.starter.extend(
					*self.__cls._command.planetary.supercalifragilisticexpialidocious.components.kwargs.starter,
					*self.__cls._command.baked.supercalifragilisticexpialidocious.components.kwargs.starter,
				)
		else:
			if self.__args:
				self.__process_args()
			if self.__kwargs:
				self.__add_kwargs()
				self.__process_kwargs()

		return self.__cls

	def __quoting(self, quote_value: Union[bool, None], value: Any):
		"""

			quote_value:
				* True: double quoting
				* False: single quoting
				* None: no quoting

		"""
		if isinstance(value, dict) or quote_value is None:
			return value

		# Be Careful! Mind the quotes on the values below!
		# The following two returns are NOT the same!
		# The first returns '{value}' and the second "{value}"!
		elif not quote_value:
			return f"'{value}'"
		else:
			return f'"{value}"'

	def __process_args(self):
		if (
			(any((self.__baking, self.__global)) and self.__add_replace == "replace") or
			self.__calling
		):
			self.__cls._command[self.__cat][self.__subcommand].components.args[self.__starter_regular] = tea()

		for arg in self.__args:
			if isinstance(arg, dict):
				self.__cls._command[self.__cat][self.__subcommand].components.args[
					self.__starter_regular
				].append(self.__quoting(
						arg.get("quotes", None),
						arg["value"],
					)
				)
			elif isinstance(arg, (str, bytes, bytearray, int)):
				self.__cls._command[self.__cat][self.__subcommand].components.args[
					self.__starter_regular
				].append(arg)
			else:
				raise TypeError(
					f'Sorry! Value "{arg}" must be a string, integer, or dictionary!'
				)

	def __add_kwargs(self):

		# Resets or initializes the unprocessed kwargs
		self.__cls._command[self.__cat][
			self.__subcommand
		].components.kwargs.unprocessed = D({})

		for key, value in self.__kwargs.items():
			"""

				For the condition directly below:
				If the boolean value is "False", don't put the argument in; for example,
				if "meltan.cmd([...], no_check = False)", then the result would be "meltan cmd [...]",
				i.e. without "--no-check"

			"""
			if bool(value):
				if isinstance(value, dict):
					self.__cls._command[self.__cat][
						self.__subcommand
					].components.kwargs.unprocessed[key]["value"] = self.__quoting(
						value.get("quotes", None),
						value.get("value", ""),
					)
					for keyop in (
						"dashes",
						"fixed",
						"repeat",
						"repeat_with_values",
					):
						if keyop in value.keys():
							self.__cls._command[self.__cat][
								self.__subcommand
							].components.kwargs.unprocessed[key][keyop] = value[keyop]
				elif isinstance(
					value, (str, bytes, bytearray, int)
				):
					self.__cls._command[self.__cat][
						self.__subcommand
					].components.kwargs.unprocessed[key] = value
				else:
					raise TypeError(
						f'Sorry! Value "{value}" must be a string, integer, or dictionary!'
					)

	def __process_kwargs(self):
		for key, value in self.__cls._command[self.__cat][
			self.__subcommand
		].components.kwargs.unprocessed.items():
			if isinstance(value, dict):

				if self.__cls._dos:
					dash = "/"
				else:
					if value.get("dashes", None) is None:
						dash = "-" if (len(key) == 1 or self.__cls._kwarg_one_dash) else "--"
					else:
						dash = "-" if value["dashes"] else "--"
				final_key = f'{dash}{key if value.get("fixed", False) or self.__cls._fixed_key else key.replace("_", "-")}'

				if "repeat" in value.keys():
					self.__cls._command[self.__cat][self.__subcommand].components.kwargs[
						self.__starter_regular
					].append([final_key] * value["repeat"])
				elif "repeat_with_values" in value.keys():
					value_list = [
						self.__quoting(
							value["quotes"], value["value"]
						)
						if isinstance(value, dict)
						else value
						for value in value[
							"repeat_with_values"
						]
					]
					self.__cls._command[self.__cat][self.__subcommand].components.kwargs[
						self.__starter_regular
					].extend(
						chain(
							*zip(
								[final_key]
								* len(value_list),
								value_list,
							)
						)
					)
				else:
					self.__cls._command[self.__cat][self.__subcommand].components.kwargs[
						self.__starter_regular
					].append(final_key)
					self.__cls._command[self.__cat][self.__subcommand].components.kwargs[
						self.__starter_regular
					].append(
						""
						if isinstance(value["value"], bool)
						else value["value"]
					)

			else:
				if self.__cls._dos:
					dash = "/"
				else:
					dash = "-" if self.__cls._kwarg_one_dash or len(key) == 1 else "--"

				final_key = key if self.__cls._fixed_key else key.replace("_", "-")

				self.__cls._command[self.__cat][self.__subcommand].components.kwargs[
					self.__starter_regular
				].append(dash + final_key)

				self.__cls._command[self.__cat][self.__subcommand].components.kwargs[
					self.__starter_regular
				].append(
					"" if isinstance(value, bool) else value
				)