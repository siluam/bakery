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
	def _return_output(self, *args, _cls = None, _subcommand = "command", **kwargs):
		self.__cls = _cls if _cls is not None else self
		self.__subcommand = _subcommand

		self.__command = self._create_command(
			*args,
			_cls = self.__cls,
			_subcommand = self.__subcommand,
			**kwargs
		)

		if self.__cls._str:
			return self.__command()

		output = self.__capture_output()

		if output is None:
			_peek_value, self.__stderr = peek(
				self.__decode_std(self.__stderr), return_first=2
			)

			if _peek_value and not self.__cls._ignore_stderr:
				raise stderr("\n".join(self.__decode_std(self.__stderr)))
			else:
				return self.__verbose_return() if self.__cls._return == "verbosity" else self.__regular_return()
		else:
			return output

	def __capture_output(self):

		if self.__cls._capture == "run":

			run(self.__command())
			_ = D({})
			_.command = self.__command()
			_.tea = self.__command
			_.sub = self.__cls._sub
			if self.__cls._verbosity > 0:
				_.final = D(self.__cls._command.final[self.__subcommand])
			if self.__cls._verbosity > 1:
				_.baked = D(self.__cls._command.baked[self.__subcommand])
				_.called = D(self.__cls._command.called[self.__subcommand])
			return _

		else:

			_output = getattr(
				__import__("sarge"), f"capture_{self.__cls._capture}"
			)(self.__command())

			self.__return_code = _output.returncode
			self.__return_codes = _output.returncodes

			if self.__cls._capture == "stdout":
				self.__stdout = _output.stdout
				self.__stderr = ()
			elif self.__cls._capture == "stderr":
				self.__stdout = ()
				self.__stderr = _output.stderr
			else:
				self.__stdout = _output.stdout
				self.__stderr = _output.stderr
			
			return None

	def __decode_std(self, _std):
		yield from (
			line.decode("utf-8").rstrip()
			if isinstance(line, bytes)
			else line
			for line in _std
		)

	def __verbose_return(self):

		_: Dict[str, Any] = D({
			"stdout": self.__cls._convert_to_type(
				self.__decode_std(self.__stdout),
				self.__cls._type
			),
		})

		if self.__cls._verbosity > 0:
			_.stderr = self.__cls._convert_to_type(
				self.__decode_std(self.__stderr),
				self.__cls._type
			)
			_.return_code = self.__return_code
			_.return_codes = self.__return_codes
			_.command = self.__command()
			_.tea = self.__command
			_.sub = self.__cls._sub

		if self.__cls._verbosity > 1:
			_.baked = D(self.__cls._command.baked[self.__subcommand])
			_.called = D(self.__cls._command.called[self.__subcommand])
			_.final = D(self.__cls._command.final[self.__subcommand])

		if (
			self.__cls._n_lines.number is not None and
			self.__cls._type.__name__ != "str"
		):
			trim_part = partial(
				trim,
				ordinal=self.__cls._n_lines.ordinal,
				number=self.__cls._n_lines.number,
				_type=self.__cls._type,
				ignore_check=True,
			)

			if self.__cls._n_lines.std in ("out", "both"):
				_.stdout = trim_part(iterable=_.stdout)

			if (
				self.__cls._n_lines.std in ("err", "both")
				and self.__cls._verbosity > 0
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
