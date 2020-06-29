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


################################################################################################

class _process_args_kwargs:

	def _process_args_kwargs(
		self,
		*args,
		_cls = self,
		_baking = False,
		_calling = True,
		_subcommand = None,
		_bake_add_replace = "add",
		**kwargs,
	):
		self.__args = args
		self.__kwargs = kwargs
		self.__baking = _baking
		self.__calling = _calling
		self.__subcommand = _subcommand
		self.__bake_add_replace = _bake_add_replace

		if _baking and _calling:
			raise cannot_set_multiple('Sorry! _baking and _calling may not be used together! Please choose only a single category!')

		if self.__args:
			self.__process_args()
		if self.__kwargs:
			self.__if_kwargs()

	def __quoting(self, quote_value: Union[bool, None], value: Any):
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
		sub = self.__subcommand if self.__subcommand else "command"

		if self.__baking:
			boc = "baked"
			if self.__bake_add_replace == "replace":
				self.__command[sub].components.baked = tea()
		else:
			boc = "called"
			self.__command[sub].components.called = tea()

		for arg in self.__args:
			if isinstance(arg, dict):
				self.__command[sub].components[boc].append(
					self.__quoting(
						arg.get("quotes", None),
						arg["value"],
					)
				)
			elif isinstance(arg, (str, bytes, bytearray, int)):
				self.__command[sub].components[boc].append(arg)
			else:
				raise not_string_dict(
					f'Sorry! Value "{arg}" must be a string, integer, or dictionary!'
				)

################################################################################################

class _attach_command_args_kwargs:

	def __if_kwargs(self):
		self.__new_kwargs = {}
		self.__add_kwargs()
		self.__process_kwargs()

	def __add_kwargs(self):
		for key, value in self.__kwargs.items():
			"""

				For the condition directly below:
				If the boolean value is "False", don't put the argument in; for example,
				if "meltan.cmd([...], no_check = False)", then the result would be "meltan cmd [...]",
				i.e. without "--no-check"

			"""
			if bool(value):
				if isinstance(value, dict):
					self.__new_kwargs[key] = {}
					self.__new_kwargs[key]["value"] = self.__quoting(
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
							self.__new_kwargs[key][keyop] = value[
								keyop
							]
				elif isinstance(
					value, (str, bytes, bytearray, int)
				):
					self.__new_kwargs[key] = value
				else:
					raise not_string_dict(
						"Sorry! Value must be a string, integer, or dictionary!"
					)

	def __process_kwargs(self):
		for key, value in self.__new_kwargs.items():
			if isinstance(value, dict):

				if os_name == "nt":
					dash = "/"
				else:
					if value.get("dashes", None) is None:
						dash = "-" if len(key) == 1 or self._kwarg_one_dash else "--"
					else:
						dash = "-" if value["dashes"] else "--"
				final_key = f'{dash}{key if value.get("fixed", False) or self._fixed_key else key.replace("_", "-")}'

				if "repeat" in value.keys():
					self.__command.append(
						[final_key] * value["repeat"]
					)
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
					self.__command.append(
						chain(
							*zip(
								[final_key]
								* len(value_list),
								value_list,
							)
						)
					)
				else:
					self.__command.append(final_key)
					self.__command.append(
						""
						if isinstance(value["value"], bool)
						else value["value"]
					)

			else:
				self.__command.append(
					"/" if os_name == "nt" else (
						"-"
						if self._kwarg_one_dash
						or len(key) == 1
						else "--"
					)
					+ (
						key
						if self._fixed_key
						else key.replace("_", "-")
					)
				)
				self.__command.append(
					"" if isinstance(value, bool) else value
				)