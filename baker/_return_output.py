# From Imports
from addict import Dict as D
from functools import partial
from itertools import chain
from nanite import peek, trim
from shlex import split, quote
from subprocess import Popen, PIPE, DEVNULL
from typing import Dict, Any


class Error(Exception):
	pass


class stderr(Error):
	pass


class _return_output:
	def _return_output(
		self,
		_cls=None,
		_subcommand="supercalifragilisticexpialidocious",
	):
		self.__cls = self._cls_check(_cls)
		self.__subcommand = _subcommand

		self.__command = self._create_command(
			_cls=self.__cls, _subcommand=self.__subcommand,
		)

		if self.__cls._frozen:

			self.__cls._freezer = self.__command()
			return self.__cls

		else:

			if self.__cls._str:
				return self.__command()

			if isinstance((output := self.__return()), dict):
				_peek_value, output.stderr = peek(
					output.stderr, return_first=2
				)
				if _peek_value and not self.__cls._ignore_stderr:
					raise stderr("".join(output.stderr))

				conversion_partial = partial(
					self.__cls._convert_to_type,
					_type=self.__cls._type,
				)

				if self.__cls._capture == "stdout":
					if self.__cls._verbosity < 1:
						del output.stderr
					output.stdout = conversion_partial(
						output.stdout
					)
				elif self.__cls._capture == "stderr":
					if self.__cls._verbosity > 0:
						del output.stdout
					output.stderr = conversion_partial(
						output.stderr
					)
				else:
					output.stdout = conversion_partial(
						output.stdout
					)
					output.stderr = conversion_partial(
						output.stderr
					)

			return output

	def __return(self):

		process = self.__set_popen_partial()

		if self.__cls._wait is None:

			with process(stdout=DEVNULL, stderr=DEVNULL,) as p:
				return (
					"None"
					if self.__cls._type.__name__
					in ("str", "repr")
					else None
				)

		elif self.__cls._wait:

			with process() as p:

				_ = D({})

				p.wait(self.__cls._timeout)

				_.stdout = self.__capture(p, "out")
				_.stderr = self.__capture(p, "err")

				if self.__cls._verbosity > 0:
					_.returns.code = p.returncode
					# _.returns.codes = p.returncodes
					_.command.bakeriy = self.__command()
					_.command.subprocess = p.args
					_.pid = p.pid

				if self.__cls._verbosity > 1:
					_.tea = self.__command
					_.sub = self.__cls._sub
					_.final = D(
						self.__cls._command.final[
							self.__subcommand
						]
					)
					_.baked = D(
						self.__cls._command.baked[
							self.__subcommand
						]
					)
					_.planetary = D(
						self.__cls._command.planetary[
							self.__subcommand
						]
					)
					_.called = D(
						self.__cls._command.called[
							self.__subcommand
						]
					)

				if (
					self.__cls._n_lines.number is not None
					and not self.__cls._type.__name__
					in ("str", "repr")
				):
					trim_part = partial(
						trim,
						ordinal=self.__cls._n_lines.ordinal,
						number=self.__cls._n_lines.number,
						_type=self.__cls._type,
						ignore_check=True,
					)

					if self.__cls._n_lines.std in (
						"stdout",
						"both",
					):
						_.stdout = trim_part(iterable=_.stdout)

					if self.__cls._n_lines.std in (
						"stderr",
						"both",
					):
						_.stderr = trim_part(iterable=_.stderr)

				return _

		else:

			return process()

	def __set_popen_partial(self):

		if self.__cls._capture == "stderr":
			stdout = DEVNULL
		else:
			stdout = (
				self.__cls._popen.get("stdout", DEVNULL)
				if self.__cls._ignore_stdout
				else self.__cls._popen.get("stdout", PIPE)
			)
		stderr = (
			self.__cls._popen.get("stderr", DEVNULL)
			if self.__cls._ignore_stderr
			else self.__cls._popen.get("stderr", PIPE)
		)

		return partial(
			Popen,
			quote(self.__command())
			if self.__cls._popen.get("shell", False)
			else split(self.__command()),
			bufsize=self.__cls._popen.get("bufsize", -1),
			stdin=self.__cls._popen.get("stdin", None),
			stdout=stdout,
			stderr=stderr,
			executable=self.__cls._popen.get("executable", None),
			preexec_fn=self.__cls._popen.get("preexec_fn", None),
			close_fds=self.__cls._popen.get("close_fds", True),
			shell=self.__cls._popen.get("shell", False),
			cwd=self.__cls._popen.get("cwd", None),
			env=self.__cls._popen.get("env", None),
			universal_newlines=True
			if self.__cls._popen.get("bufsize", -1) == 1
			else self.__cls._popen.get(
				"universal_newlines", None
			),
			startupinfo=self.__cls._popen.get(
				"startupinfo", None
			),
			creationflags=self.__cls._popen.get(
				"creationflags", 0
			),
			restore_signals=self.__cls._popen.get(
				"restore_signals", True
			),
			start_new_session=self.__cls._popen.get(
				"start_new_session", False
			),
			pass_fds=self.__cls._popen.get("pass_fds", ()),
			encoding=self.__cls._popen.get("encoding", None),
			errors=self.__cls._popen.get("errors", None),
			text=True
			if self.__cls._popen.get("bufsize", -1) == 1
			else self.__cls._popen.get(
				"universal_newlines", None
			),
		)

	def __capture(self, p, std):
		"""
			Answer: https://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python/519653#519653
			User: https://stackoverflow.com/users/17160/nosklo
		"""

		"""
			Answer: https://stackoverflow.com/questions/13243766/python-empty-generator-function/26271684#26271684
			User: https://stackoverflow.com/users/289240/zectbumo
		"""
		capture = iter(())

		if isinstance(p, Popen):
			if self.__cls._capture == "run":
				while p.poll() is None:
					if (output := getattr(p, f"std{std}").read(self.__cls._chunk_size)):
						print(new_output := (
							output.decode("utf-8")
							if isinstance(output, (bytes, bytearray))
							else output
						))
						capture = chain([new_output], capture)
					else:
						return capture
				else:
					return capture
			else:
				return iter(getattr(p, f"std{std}"))
		else:
			return capture