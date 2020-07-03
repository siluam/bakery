# Imports
import pout

# From Imports
from addict import Dict as D
from nanite import module_installed
from gensing import tea, frosting

################################################################################################

class _run_frosting:

	def _run_frosting(self, *args, _cls = None, _subcommand = "command", **kwargs):

		self.__cls = _cls if _cls is not None else self
		self.__subcommand = _subcommand

		try:

			output = self.__cls._return_output(
				*args,
				_cls = _cls,
				_subcommand = _subcommand,
				**kwargs,
			)

			if self.__cls._print:
				print(output)

			if self.__cls._frosting:
				# for category in output:
				# 	if (
				# 		isinstance(output[category], int) or
				# 		isinstance(output[category], (str, bytes, bytearray)
				# 	):
				# 		print(f"{category}: {output[category]}")
				# 	else:
				# 		if category not in self.__cls._captures:
				# 			print(f"{category}: ")
				# 		if category == "return_codes":
				# 			print(output[category])
				# 		else:
				# 			for line in output[category]:
				# 				print(line)
				pout.v(output)

			# if self.__cls._verbosity > 0:
			# 	pout.v(output)

			if isinstance(output, (dict, tea, frosting)) and len(output) == 1:
				return next(iter(output.values()))
			else:
				return output
		finally:
			self._set(_reset = True)