# From Imports
from addict import Dict as D
from functools import partial
from nanite import peek, trim
from sarge import Pipeline, Capture
from typing import Dict, Any

class Error(Exception):
	pass


class stderr(Error):
	pass


class _return_output:
	def _return_output(self, _cls = None, _subcommand = "supercalifragilisticexpialidocious"):
		self.__cls = self._cls_check(_cls)
		self.__subcommand = _subcommand

		self.__command = self._create_command(
			_cls = self.__cls,
			_subcommand = self.__subcommand,
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

		stdout_capture = Capture(
			timeout=self.__cls._timeout_stdout,
			buffer_size=1 if self.__cls._capture = "run" else self.__cls._buffer_size_stdout
		)
		stderr_capture = Capture(
			timeout=self.__cls._timeout_stderr,
			buffer_size=1 if self.__cls._capture = "run" else self.__cls._buffer_size_stderr
		)

		p = Pipeline(self.__command(), stdout = stdout_capture, stderr = stderr_capture)
		p.run()

		if self.__cls._wait is None:

			p.close()

			return None

		elif self.__cls._wait:

			p.wait()

			_ = D({})

			if _capture in ("stdout", "stderr", "both"):
				_.stdout = p.stdout
				_.stderr = p.stderr
			else:
				_.return_code = p.returncode

			if self.__cls._verbosity > 0:
				if not _.stdout:
					_.stdout = p.stdout
				if not _.stderr:
					_.stderr = p.stderr
				if not _.return_code:
					_.return_code = p.returncode
				_.return_codes = p.returncodes
				_.command.bakeriy = self.__command()
				_.command.sarge = p.commands

			if self.__cls._verbosity > 1:
				_.tea = self.__command
				_.sub = self.__cls._sub
				_.final = D(self.__cls._command.final[self.__subcommand])
				_.baked = D(self.__cls._command.baked[self.__subcommand])
				_.called = D(self.__cls._command.called[self.__subcommand])

			p.close()

			return _

		else:

			return p

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
			self._convert_to_type(self.__decode_std(self.__stdout), self.__cls._type),
			self._convert_to_type(self.__decode_std(self.__stderr), self.__cls._type),
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
