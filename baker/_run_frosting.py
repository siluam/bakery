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
			_ = self._return_output(args, kwargs)
			if self._frosting:
				for cat in (_):
					if isinstance(_[cat], int) or isinstance(
						_[cat], (str, bytes, bytearray)
					):
						print(f"{cat}: {_[cat]}")
					else:
						if cat not in self._captures:
							print(f"{cat}: ")
						if cat == "return_codes":
							print(_[cat])
						else:
							for line in _[cat]:
								print(line)
			if pout:
				pout.v(_)
			return _
		finally:
			self._reset_all()
