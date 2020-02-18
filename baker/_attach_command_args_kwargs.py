# From Imports
from itertools import chain
from typing import Union, Any

class Error(Exception):
	pass


class not_string_dict(Error):
	pass


class _attach_command_args_kwargs:

	def _attach_command_args_kwargs(self, command, args, kwargs):
		def quoting(quote_value: Union[bool, None], value: Any):
			if isinstance(value, dict):
				return value
			if quote_value is None:
				return value

			# Be Careful! The following two returns are NOT the same!
			# The first returns '{value}' and the second "{value}"!
			elif not quote_value:
				return f"'{value}'"
			else:
				return f'"{value}"'

		# print(args, type(args), bool(args))

		if args:
			for argument in args:
				if isinstance(argument, dict):
					command.append(
						quoting(
							argument.get("quotes", None),
							argument["value"],
						)
					)
				elif isinstance(
					argument, (str, bytes, bytearray, int)
				):
					command.append(argument)
				else:
					raise not_string_dict(
						f'Sorry! Value "{argument}" must be a string, integer, or dictionary!'
					)

		if kwargs:
			new_kwargs = {}
			for key, value in kwargs.items():
				"""

					For the condition directly below:
					If the boolean value is "False", don't put the argument in; for example,
					if "meltan.cmd([...], no_check = False)", then the result would be "meltan cmd [...]",
					i.e. without "--no-check"

				"""
				if bool(value):
					if isinstance(value, dict):
						new_kwargs[key] = {}
						new_kwargs[key]["value"] = quoting(
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
								new_kwargs[key][keyop] = value[
									keyop
								]
					elif isinstance(
						value, (str, bytes, bytearray, int)
					):
						new_kwargs[key] = value
					else:
						raise not_string_dict(
							"Sorry! Value must be a string, integer, or dictionary!"
						)
			for key, value in new_kwargs.items():
				if isinstance(value, dict):
					if value.get("dashes", None) is None:
						dash = "-" if len(key) == 1 or self._kwarg_one_dash else "--"
					else:
						dash = "-" if value["dashes"] else "--"
					final_key = f'{dash}{key if value.get("fixed", False) or self._fixed_key else key.replace("_", "-")}'
					if "repeat" in value.keys():
						command.append(
							[final_key] * value["repeat"]
						)
					elif "repeat_with_values" in value.keys():
						value_list = [
							quoting(
								value["quotes"], value["value"]
							)
							if isinstance(value, dict)
							else value
							for value in value[
								"repeat_with_values"
							]
						]
						command.append(
							chain(
								*zip(
									[final_key]
									* len(value_list),
									value_list,
								)
							)
						)
					else:
						command.append(final_key)
						command.append(
							""
							if isinstance(value["value"], bool)
							else value["value"]
						)
				else:
					command.append(
						(
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
					command.append(
						"" if isinstance(value, bool) else value
					)

		return command