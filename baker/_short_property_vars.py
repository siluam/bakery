# Imports
import builtins

# From Imports
from gensing import tea, frosting
from nanite import check_type, fullpath
from toml import load

class Error(Exception):
	pass


class no_caps(Error):
	pass


class too_verbose(Error):
	pass


class need_dict(Error):
	pass


class too_many_items(Error):
	pass


class no_is(Error):
	pass


class _short_property_vars:

	@property
	def _stores(self):
		return builtins.bakeriy_stores

	@property
	def _capture(self):
		return self.__capture

	@_capture.setter
	def _capture(self, value):
		if value not in self._captures:
			raise no_caps(
				f'Sorry! Capture type "{value}" is not permitted! Choose from one of: [{(", ").join(self._captures)}]'
			)
		self.__capture = value

	@property
	def _print(self):
		return self.__print

	@_print.setter
	def _print(self, value):
		self.__print = bool(value)
		if value:
			self._str = True

	@property
	def _frosting(self):
		return self.__frosting

	@_frosting.setter
	def _frosting(self, value):
		self.__frosting = bool(value)
		if value:
			self._type = iter

	@property
	def _sudo(self):
		return self.__sudo

	@_sudo.setter
	def _sudo(self, value):
		if not isinstance(value, (dict, tea, frosting)):
			raise need_dict('Sorry! "_sudo" needs to be a tea, frosting, or dict-like object!')
		if len(value) > 1:
			raise too_many_items('Sorry! The "_sudo" object can only have a single key-value item!')
		if (
			value and
			next(iter(value.keys())) not in ("i", "s")
		):
			raise no_is('Sorry! The "_sudo" object can only take "i" or "s" as a key!')
		self.__sudo = value

	@property
	def _starter_kwargs(self):
		return self.__starter_args

	@_starter_kwargs.setter
	def _starter_kwargs(self, value):
		if not isinstance(value, (dict, tea, frosting)):
			raise need_dict('Sorry! "_starter_kwargs" needs to be a tea, frosting, or dict-like object!')
		self.__starter_kwargs = value