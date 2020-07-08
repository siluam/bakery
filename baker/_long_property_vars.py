# Imports
import os

# From Imports
from addict import Dict as D
from sarge import get_stdout

class Error(Exception):
	pass


class no_prog(Error):
	pass


class n_lines_ordinal(Error):
	pass


class n_lines_number(Error):
	pass


class n_lines_std(Error):
	pass


class no_category(Error):
	pass


class not_iterable(Error):
	pass


class verbosity_invalid(Error):
	pass


class _long_property_vars:

	@property
	def _program(self):
		return self.__program

	@_program.setter
	def _program(self, value):
		if isinstance(value, dict):
			if not value["fixed"]:
				value = value.replace("_", "-")
		else:
			value = value.replace("_", "-")
		if (
			not get_stdout(
				f'{"where.exe" if os.name == "nt" else "which"} {value}'
			)
			and not self._ignore_check
		):
			raise no_prog(
				f'Sorry! "{value}" does not seem to exist in the path!'
			)
		else:
			self.__program = value

	@property
	def _n_lines(self):
		return self.__n_lines

	@_n_lines.setter
	def _n_lines(self, value):
		if value.get("ordinal", False):
			if value["ordinal"] not in (ordinals := ("first", "last")):
				raise n_lines_ordinal(
					f'Sorry! You must choose from: [{", ".join(ordinals)}]'
				)
		else:
			value["ordinal"] = "first"

		if value.get("number", False):
			if value["number"] is None:
				pass
			elif int(value["number"]) < 1:
				raise n_lines_number(
					'Sorry! "n" must be greater than 0!'
				)
		else:
			value["number"] = None

		if value.get("std", False):
			if value["std"] not in (stds := ("out", "err", "both")):
				raise n_lines_std(
					f'Sorry! You must choose from: [{(", ").join(stds)}]'
				)
		else:
			value["std"] = "out"

		self.__n_lines = D(value)