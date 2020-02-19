# From Imports
from addict import Dict as D
from copy import deepcopy


class _funky_properties:

	@property
	def chip_(self):
		"""
			Create an exact copy / snapshot of this instance
		"""

		# Change these
		return deepcopy(self)

	@property
	def cv_(self):
		"""

			Return an addict dictionary with all the current values for the class variables;
			can be used for debugging purposes or otherwise.

		"""

		return D({
			key.replace(
				"_bakery__",
				"_"
				if key.lstrip("_bakery__")
				in self._kwarg_settings.keys()
				else (
					""
					if key.lstrip("_bakery__")
					in self._non_underscored_properties
					else "__"
				),
			): value
			for key, value in vars(self).items()
		})