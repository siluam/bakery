# From Imports
from addict import Dict as D
from functools import partial
from nanite import peek, trim
from shlex import split
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

			self.__cls._program = self.__command()
			return self

		else:

			if self.__cls._str:
				return self.__command()

			output = self.__return()

			if isinstance(output, dict):
				if output.stderr:
					_peek_value, output.stderr = peek(
						output.stderr, return_first=2
					)
					if _peek_value:
						raise stderr("\n".join(output.stderr))

				conversion_partial = partial(
					self.__cls._convert_to_type,
					_type = self.__cls._type,
				)

				if self.__cls._capture in ("stdout", "run"):
					if not output.dict and not isinstance(output.stderr, dict):
						del output.stderr
					if not self.__cls._ignore_stdout:
						output.stdout = conversion_partial(output.stdout)
				if self.__cls._capture == "stderr":
					if not self.__cls._ignore_stderr:
						output.stderr = conversion_partial(output.stderr)
				if self.__cls._capture == "both":
					if not self.__cls._ignore_stdout:
						output.stdout = conversion_partial(output.stdout)
					if not self.__cls._ignore_stderr:
						output.stderr = conversion_partial(output.stderr)

			return output

	def __return(self):

		process = self.__set_popen_partial()

		if self.__cls._wait is None:

			with process() as p:
				return "None" if self.__cls._type.__name__ in ("str", "repr") else None

		elif self.__cls._wait:

			with process(
				stdin = self.__cls._popen.get("stdin", PIPE),
				stdout = self.__cls._popen.get("stdout", DEVNULL) if self.__cls._ignore_stdout else self.__cls._popen.get("stdout", PIPE),
				stderr = self.__cls._popen.get("stderr", DEVNULL) if self.__cls._ignore_stderr else self.__cls._popen.get("stderr", PIPE),
			) as p:

				p.wait()

				_ = D({})

				if self.__cls._ignore_stderr and self.__cls._ignore_stdout:
					pass
				elif self.__cls._ignore_stderr:
					if self.__cls._capture != "stderr":
						_.stdout = self.__decode_std(p.stdout, "stdout")
						if self.__cls._verbosity > 1:
							_.capture.stdout = p.stdout
				elif self.__cls._ignore_stdout:
					if self.__cls._capture != "stdout":
						_.stderr = self.__decode_std(p.stderr, "stderr")
						if self.__cls._verbosity > 1:
							_.capture.stderr = p.stderr
				else:
					if self.__cls._capture == "stderr":
						_.stderr = self.__decode_std(p.stderr, "stderr")
						if self.__cls._verbosity > 1:
							_.capture.stderr = p.stderr
					else:
						_.stdout = self.__decode_std(p.stdout, "stdout")
						if self.__cls._verbosity > 1:
							_.capture.stdout = p.stdout
						_.stderr = self.__decode_std(p.stderr, "stderr")
						if self.__cls._verbosity > 1:
							_.capture.stderr = p.stderr

				if self.__cls._verbosity > 0:
					_.returns.code = p.returncode
					_.returns.codes = p.returncodes
					_.command.bakeriy = self.__command()
					_.command.sarge = p.commands

				if self.__cls._verbosity > 1:
					_.tea = self.__command
					_.sub = self.__cls._sub
					_.final = D(
						self.__cls._command.final[self.__subcommand]
					)
					_.baked = D(
						self.__cls._command.baked[self.__subcommand]
					)
					_.planetary = D(
						self.__cls._command.planetary[self.__subcommand]
					)
					_.called = D(
						self.__cls._command.called[self.__subcommand]
					)

				if (
					self.__cls._n_lines.number is not None
					and not self.__cls._type.__name__ in ("str", "repr")

					# TODO: If "tee" works, remove this line
					and self.__cls._capture != "run"
				):
					trim_part = partial(
						trim,
						ordinal=self.__cls._n_lines.ordinal,
						number=self.__cls._n_lines.number,
						_type=self.__cls._type,
						ignore_check=True,
					)

					if self.__cls._n_lines.std in ("stdout", "both"):
						_.stdout = trim_part(iterable=_.stdout)

					if self.__cls._n_lines.std in ("stderr", "both"):
						_.stderr = trim_part(iterable=_.stderr)

				return _

		else:

			return p

	def __set_popen_partial(self):

		return partial(
			Popen,
			self.__command() if self.__cls._popen.get("shell", False) else split(self.__command()),
			bufsize = self.__cls._popen.get("bufsize", -1),
			executable = self.__cls._popen.get("executable", None),
			preexec_fn = self.__cls._popen.get("preexec_fn", None),
			close_fds = self.__cls._popen.get("close_fds", True),
			shell = self.__cls._popen.get("shell", False),
			cwd = self.__cls._popen.get("cwd", None),
			env = self.__cls._popen.get("env", None),
			universal_newlines = True if self.__cls._popen.get("bufsize", -1) == 1 else self.__cls._popen.get("universal_newlines", None),
			startupinfo = self.__cls._popen.get("startupinfo", None),
			creationflags = self.__cls._popen.get("creationflags", 0),
			restore_signals = self.__cls._popen.get("restore_signals", True),
			start_new_session = self.__cls._popen.get("start_new_session", False),
			pass_fds = self.__cls._popen.get("pass_fds", ()),
			encoding = self.__cls._popen.get("encoding", None),
			errors = self.__cls._popen.get("errors", None),
			text = True if self.__cls._popen.get("bufsize", -1) == 1 else self.__cls._popen.get("text", None),,
		)

	def __capture(self, p):
	"""
		Answer: https://stackoverflow.com/a/519653
		User: https://stackoverflow.com/users/17160/nosklo
	"""

		capture = []

		if self.__cls._capture == "run":
			while p.poll() is None:
				if self.__cls._ignore_stdout and self.__cls._ignore_stderr:
					pass
				elif self.__cls._ignore_stderr:
					output = p.stdout.readline(block=self.__cls._block_stdout)
					output = output.decode("utf-8") if isinstance(output, (bytes, bytearray)) else output
					if output:
						print(output)
				elif self.__cls._ignore_stdout:
					output = p.stderr.readline(block=self.__cls._block_stderr)
					output = output.decode("utf-8") if isinstance(output, (bytes, bytearray)) else output
					if output:
						print(output)
				else:
					stdoutput = p.stdout.readline(block=self.__cls._block_stdout)
					stdoutput = stdoutput.decode("utf-8") if isinstance(stdoutput, (bytes, bytearray)) else stdoutput
					if stdoutput:
						print(stdoutput)
					stderrput = p.stderr.readline(block=self.__cls._block_stderr)
					stderrput = stderrput.decode("utf-8") if isinstance(stderrput, (bytes, bytearray)) else stderrput
					if stderrput:
						print(stderrput)
		else:
			for cat in ("out, err"):
				while True:
					if not (output := getattr(p, f"std{cat}").readline()):
						break
					capture.append(
						output.decode("utf-8") if isinstance(
							output, (bytes, bytearray)
						) else output
					)

		yield from capture