# From Imports
from itertools import chain
from os import name as os_name
from typing import Union, Any
from gensing import tea, frosting

class Error(Exception):
	pass


class not_string_dict(Error):
	pass


class cannot_set_multiple(Error):
	pass


class _process_args_kwargs:

	def _process_args_kwargs(
		self,
		*args,
		_cls = self,
		_baking = False,
		_calling = False,
		_subcommand = "command",
		_starter_regular = "regular",
		**kwargs,
	):
		self.__args = args
		self.__kwargs = kwargs
		self.__cls = _cls
		self.__baking = _baking
		self.__calling = _calling
		self.__boc = "baked" if self.__baking else "called"
		self.__subcommand = _subcommand
		self.__starter_regular = _starter_regular

		if _baking and _calling:
			raise cannot_set_multiple('Sorry! _baking and _calling may not be used together! Please choose only a single category!')

		for bc in ("baked", "called"):
			for ak in ("args", "kwargs"):
				for sr in ("starter", "regular"):
					if not self.__cls._command[bc][self.__subcommand].components[ak][sr]:
						self.__cls._command[bc][self.__subcommand].components[ak][sr] = tea()

		if self.__args:
			self.__process_args()
		if self.__kwargs:
			self.__add_kwargs()
			self.__process_kwargs()

		if self.__cls != self:
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
			(self.__baking and self.__add_replace == "replace") or
			self.__calling
		):
			self.__cls._command[self.__boc][self.__subcommand].components.args[self.__starter_regular] = tea()

		for arg in self.__args:
			if isinstance(arg, dict):
				self.__cls._command[self.__boc][self.__subcommand].components.args[
					self.__starter_regular
				].append(self.__quoting(
						arg.get("quotes", None),
						arg["value"],
					)
				)
			elif isinstance(arg, (str, bytes, bytearray, int)):
				self.__cls._command[self.__boc][self.__subcommand].components.args[
					self.__starter_regular
				].append(arg)
			else:
				raise not_string_dict(
					f'Sorry! Value "{arg}" must be a string, integer, or dictionary!'
				)

	def __add_kwargs(self):

		# Resets or initializes the unprocessed kwargs
		self.__cls._command[self.__boc][
			self.__subcommand
		].components.kwargs.unprocessed = tea()

		for key, value in self.__kwargs.items():
			"""

				For the condition directly below:
				If the boolean value is "False", don't put the argument in; for example,
				if "meltan.cmd([...], no_check = False)", then the result would be "meltan cmd [...]",
				i.e. without "--no-check"

			"""
			if bool(value):
				if isinstance(value, dict):
					self.__cls._command[self.__boc][
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
							self.__cls._command[self.__boc][
								self.__subcommand
							].components.kwargs.unprocessed[key][keyop] = value[keyop]
				elif isinstance(
					value, (str, bytes, bytearray, int)
				):
					self.__cls._command[self.__boc][
						self.__subcommand
					].components.kwargs.unprocessed[key] = value
				else:
					raise not_string_dict(
						"Sorry! Value must be a string, integer, or dictionary!"
					)

	def __process_kwargs(self):
		for key, value in self.__cls._command[self.__boc][
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
					self.__cls._command[self.__boc][self.__subcommand].components.kwargs[
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
					self.__cls._command[self.__boc][self.__subcommand].components.kwargs[
						self.__starter_regular
					].append(
						chain(
							*zip(
								[final_key]
								* len(value_list),
								value_list,
							)
						)
					)
				else:
					self.__cls._command[self.__boc][self.__subcommand].components.kwargs[
						self.__starter_regular
					].append(final_key)
					self.__cls._command[self.__boc][self.__subcommand].components.kwargs[
						self.__starter_regular
					].append(
						""
						if isinstance(value["value"], bool)
						else value["value"]
					)

			else:
				self.__cls._command[self.__boc][self.__subcommand].components.kwargs[
					self.__starter_regular
				].append(
					"/" if self.__cls._dos else (
						"-"
						if self.__cls._kwarg_one_dash
						or len(key) == 1
						else "--"
					)
					+ (
						key
						if self.__cls._fixed_key
						else key.replace("_", "-")
					)
				)
				self.__cls._command[self.__boc][self.__subcommand].components.kwargs[
					self.__starter_regular
				].append(
					"" if isinstance(value, bool) else value
				)