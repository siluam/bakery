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


class _short_property_vars:

	@property
	def _stores(self):
		return builtins.bakeriy_stores

	@property
	def _type(self):
		return self.__type

	@_type.setter
	def _type(self, value):
		self.__type = check_type(
			_type=value,
			allowed_type_names=self._allowed_type_names,
		)

	@property
	def _capture(self):
		return self.__capture

	@_capture.setter
	def _capture(self, value):
		if value not in self._captures:
			raise no_caps(
				f'Sorry! Type "{value}" is not permitted! Choose from one of: [{(", ").join(self._captures)}]'
			)
		self.__capture = value

	@property
	def _print(self):
		return self.__print

	@_print.setter
	def _print(self, value):
		self.__print = bool(value)
		if value:
			self.__str = True

	@property
	def _frosting(self):
		return self.__frosting

	@_frosting.setter
	def _frosting(self, value):
		self.__frosting = bool(value)
		if value:
			self.__type = iter

	@property
	def _starter_kwargs(self):
		return self.__starter_args

	@_starter_kwargs.setter
	def _starter_kwargs(self, value):
		if not isinstance(value, (dict, tea, frosting)):
			raise need_dict('Sorry! "_starter_kwargs" needs to be a tea, frosting, or dict-like object!')
		self.__starter_kwargs = value