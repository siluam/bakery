# From Imports
from addict import Dict as D
from functools import partial
from itertools import chain
from nanite import peek, trim, fullpath
from shlex import split, join
from subprocess import Popen, PIPE, DEVNULL
from typing import Dict, Any

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
					raise SystemError("\n".join(output.stderr))

				stds = ["out", "err"]
				for std, opp in zip(stds, stds[::-1]):
					stdstd = f"std{std}"
					stdopp = f"std{opp}"
					if self.__cls._verbosity < 1:
						if self.__cls._capture == stdstd:
							del output[stdopp]

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

				for std in ("out", "err"):
					chained = []
					stdstr = f"std{std}"
					if (output := getattr(p, stdstr)):
						for line in output:
							chained = chain(chained, [
								line.decode("utf-8").strip()
								if isinstance(line, (bytes, bytearray))
								else line.strip()
							])
					_[stdstr] = iter(chained)

				p.wait()

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

		if self.__cls._input is None:
			stdin = self.__cls._popen.get("stdin", None)
		else:
			stdin = self.__cls._input

		if self.__cls._capture == "stderr":
			stdout = self.__cls._popen.get("stdout", DEVNULL)
		elif self.__cls._capture == "run":
			stdout = self.__cls._popen.get("stdout", None)
		else:
			stdout = (
				self.__cls._popen.get("stdout", DEVNULL)
				if self.__cls._ignore_stdout
				else self.__cls._popen.get("stdout", PIPE)
			)

		if self.__cls._capture == "run":
			stderr = self.__cls._popen.get("stderr", None)
		else:
			stderr = (
				self.__cls._popen.get("stderr", DEVNULL)
				if self.__cls._ignore_stderr
				else self.__cls._popen.get("stderr", PIPE)
			)

		return partial(
			Popen,
			join(split(self.__command()))
			if self.__cls._popen.get("shell", True)
			else split(self.__command()),
			bufsize=self.__cls._popen.get("bufsize", -1),
			stdin=stdin,
			stdout=stdout,
			stderr=stderr,
			executable=fullpath(self.__cls._popen.get("executable", "/bin/sh")),
			preexec_fn=self.__cls._popen.get("preexec_fn", None),
			close_fds=self.__cls._popen.get("close_fds", True),
			shell=self.__cls._popen.get("shell", True),
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
