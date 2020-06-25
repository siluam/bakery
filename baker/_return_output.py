# From Imports
from addict import Dict as D
from functools import partial
from nanite import peek, trim
from sarge import run
from typing import Dict, Any

class Error(Exception):
	pass


class stderr(Error):
	pass


class _return_output:

	def _return_output(self, args, kwargs):

		self.__command = self._create_command(args, kwargs)

		if self._str:
			return self.__command()

		output = self.__capture_output()

		if self._capture == "run":
			return self.__command() if output == 0 else output
		else:
			_peek_value, self.__stderr = peek(
				self.__decode_std(self.__stderr), return_first=2
			)

			if _peek_value and not self._ignore_stderr:
				raise stderr("\n".join(self.__decode_std(self.__stderr)))
			else:
				return self.__verbose_return() if self._return == "verbosity" else self.__regular_return()

	def __capture_output(self):

		if self._capture == "run":
			run(self.__command())
			return (
				D(
					{
						"command" : self.__command(),
						"gensing" : self.__command,
						"args" : self._args,
						"kwargs" : self._kwargs,
					}
				)
				if self._verbosity in (1, 2)
				else 0
			)
		else:

			_output = getattr(
				__import__("sarge"), f"capture_{self._capture}"
			)(self.__command())

			self.__return_code = _output.returncode
			self.__return_codes = _output.returncodes

			if self._capture == "stdout":
				self.__stdout = _output.stdout
				self.__stderr = ()
			elif self._capture == "stderr":
				self.__stdout = ()
				self.__stderr = _output.stderr
			else:
				self.__stdout = _output.stdout
				self.__stderr = _output.stderr

	def __decode_std(self, _std):
		yield from (
			line.decode("utf-8").rstrip()
			if isinstance(line, bytes)
			else line
			for line in _std
		)

	def __verbose_return(self):

		_: Dict[str, Any] = D({
			"stdout": self._convert_to_type(self.__decode_std(self.__stdout), self._type)
		})

		if self._verbosity > 0:
			_.stderr = self._convert_to_type(self.__decode_std(self.__stderr), self._type)
			_.return_code = self.__return_code
			_.return_codes = self.__return_codes
			_.command = self.__command()

		if self._verbosity > 1:
			_.args = self._args
			_.kwargs = self._kwargs
			_.gensing = self.__command

		if (
			self._n_lines.number is not None
			and self._type.__name__ != "str"
		):
			trim_part = partial(
				trim,
				ordinal=self._n_lines.ordinal,
				number=self._n_lines.number,
				_type=self._type,
				ignore_check=True,
			)

			if self._n_lines.std in ("out", "both"):
				_.stdout = trim_part(iterable=_.stdout)

			if (
				self._n_lines.std in ("err", "both")
				and self._verbosity > 0
			):
				_.stderr = trim_part(iterable=_.stderr)

		return _

	def __regular_return(self):

		_tup = (
			self._convert_to_type(self.__decode_std(self.__stdout), self._type),
			self._convert_to_type(self.__decode_std(self.__stderr), self._type),
			self.__return_code,
			self.__return_codes,
			self.__command(),
			self._args,
			self._kwargs,
			self.__command,
		)

		_dict = dict(zip(self._return_categories[:-1], _tup))

		if isinstance(
			self._return, (str, bytes, bytearray)
		):
			return _dict[self._return]
		else:
			return D(
				{
					key: value
					for key, value in _dict.items()
					if key in self._return
				}
			)