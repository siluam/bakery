# Imports
import pout

# From Imports
from addict import Dict as D
from nanite import module_installed
from gensing import tea, frosting

################################################################################################

class _run_frosting:
	def _run_frosting(self):
		pass

################################################################################################

class _run_frosting:
	def _run_frosting(self, args, kwargs):
		try:
			output = self._return_output(args, kwargs)
			if self._print:
				print(output)
			if self._frosting:
				for cat in (output):
					if isinstance(output[cat], int) or isinstance(
						output[cat], (str, bytes, bytearray)
					):
						print(f"{cat}: {output[cat]}")
					else:
						if cat not in self._captures:
							print(f"{cat}: ")
						if cat == "return_codes":
							print(output[cat])
						else:
							for line in output[cat]:
								print(line)
			pout.v(output)
			if isinstance(output, (dict, tea, frosting)) and len(output) == 1:
				return next(iter(output.values()))
			else:
				return output
		finally:
			self._set(_reset = True)
