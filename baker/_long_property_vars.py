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
	def program(self):
		return self._program

	@program.setter
	def program(self, value):
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
			self._program = value

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
			value["std"] = "both"

		self.__n_lines = D(value)

	@property
	def _return(self):
		return self.__return

	@_return.setter
	def _return(self, value):
		if isinstance(value, (str, bytes, bytearray)):
			if value not in self._return_categories:
				raise no_category(
					f'Sorry! {value} is not an acceptable category! Please choose from: [{", ".join(self._return_categories)}]'
				)
			else:
				self.__return = value
		else:
			try:
				iter(value)
			except TypeError:
				raise not_iterable(
					'Sorry! The given value is not an iterable! "_return" must be a string or an iterable!'
				)
			else:
				if "verbosity" in value:
					raise verbosity_invalid(
						f'Sorry! "verbosity" cannot be used with other category values! Please choose from [{", ".join((cat for cat in self._return_categories if cat != "verbosity"))}]'
					)
				if all(
					(i in self._return_categories for i in value)
				):
					self.__return = value
				else:
					raise no_category(
						f'Sorry! The given value contains an unacceptable category! Please choose from: [{", ".join((cat for cat in self._return_categories if cat != "verbosity"))}]'
					)