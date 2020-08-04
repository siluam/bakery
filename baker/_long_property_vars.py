# Imports
import os

# From Imports
from addict import Dict as D
from subprocess import Popen, PIPE

class _long_property_vars:

	@property
	def _n_lines(self):
		return self.__n_lines

	@_n_lines.setter
	def _n_lines(self, value):
		if value.get("ordinal", False):
			if value["ordinal"] not in (ordinals := ("first", "last")):
				raise TypeError(
					f'Sorry! You must choose from: [{", ".join(ordinals)}]'
				)
		else:
			value["ordinal"] = "first"

		if value.get("number", False):
			if value["number"] is None:
				pass
			elif int(value["number"]) < 1:
				raise ValueError(
					'Sorry! "n" must be greater than 0!'
				)
		else:
			value["number"] = None

		if value.get("std", False):
			if value["std"] not in (stds := ("stdout", "stderr", "both")):
				raise TypeError(
					f'Sorry! You must choose from: [{(", ").join(stds)}]'
				)
		else:
			value["std"] = "stdout"

		self.__n_lines = D(value)