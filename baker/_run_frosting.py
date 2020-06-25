# From Imports
from addict import Dict as D
from nanite import module_installed

# Debug Imports
pout = module_installed("pout")

class _run_frosting:
	def _run_frosting(self, args, kwargs):
		self._args = D({"old_args": args})
		self._kwargs = D({"old_kwargs": kwargs})
		args, kwargs = self._set(self, args, kwargs)
		self._args.new_args = args
		self._kwargs.new_kwargs = kwargs
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
			if pout:
				pout.v(output)
		        return output
		finally:
			self._reset_all()
