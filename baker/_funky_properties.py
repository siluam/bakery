# Imports
import pout

# From Imports
from addict import Dict as D
from copy import deepcopy

class _funky_properties:

	@property
	def debug_(self):
		pout.v(self.cv_)

	@property
	def cv_(self):
		"""

			Return an addict dictionary with all the current values for the class variables;
			can be used for debugging purposes or otherwise.

		"""

		_ = D({})

		_.program = self.program
		_.attrs.self_class = f"{type(self)=}"
		_.attrs.type_self = f"{self.__class__=}"
		_._settings.defaults = self._settings.defaults
		_._settings.baked = self._settings.baked
		_._command.baked = self._command.baked

		return _