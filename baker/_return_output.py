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

            output = self.__capture_output()

            if isinstance(output, dict):
                if output.stderr:
                    _peek_value, output.stderr = peek(
                        output.stderr, return_first=2
                    )
                    if _peek_value and not self.__cls._ignore_stderr:
                        raise stderr("\n".join(output.stderr))

                conversion_partial = partial(
                    self.__cls._convert_to_type,
                    _type = self.__cls._type,
                )

                if self.__cls._capture == "stdout":
                    del output.stderr
                    output.stdout = conversion_partial(output.stdout)
                if self.__cls._capture == "stderr":
                    output.stderr = conversion_partial(output.stderr)
                if self.__cls._capture == "both":
                    output.stdout = conversion_partial(output.stdout)
                    output.stderr = conversion_partial(output.stderr)

            return output

    def __capture_output(self):

        stderr_capture = Capture(
            timeout=self.__cls._timeout_stderr,
            buffer_size=1
            if self.__cls._capture == "run"
            else self.__cls._buffer_size_stderr,
        )

        partial_Pipeline = partial(
            Pipeline,
            self.__command(),
            posix=self.__cls._posix,
            stderr=stderr_capture,
        )

        if self.__cls._capture in ("both", "stdout"):
            p = partial_Pipeline(stdout= Capture(
                timeout=self.__cls._timeout_stdout,
                buffer_size=1
                if self.__cls._capture == "run"
                else self.__cls._buffer_size_stdout,
            ))
        else:
            p = partial_Pipeline()

        p.run(
            input=self.__cls._input,
            async_=self.__cls._async,
        )

        if self.__cls._wait is None:

            p.close()

            return None

        elif self.__cls._wait:

            p.wait()

            _ = D({})

            if self.__cls._capture in ("both", "stdout"):
                _.stdout = self.__decode_std(p.stdout, "stdout")

            _.stderr = self.__decode_std(p.stderr, "stderr")

            if self.__cls._verbosity > 0:
                if not _.stdout:
                    _.stdout = self.__decode_std(p.stdout, "stdout")
                _.returns.code = p.returncode
                _.returns.codes = p.returncodes
                _.command.bakeriy = self.__command()
                _.command.sarge = p.commands

            if self.__cls._verbosity > 1:
                if not _.capture.stdout:
                    _.capture.stdout = p.stdout
                _.capture.stderr = p.stderr
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
                and self.__cls._type.__name__ != "str"
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

            p.close()

            return _

        else:

            return p

    def __decode_std(self, std, std_str):
        """
			Answer: https://stackoverflow.com/a/519653
			User: https://stackoverflow.com/users/17160/nosklo
		"""
        while True:
            chunk = std.read(
                size=getattr(
                    self.__cls, f"_chunk_size_{std_str}"
                ),
            )
            if not chunk:
                break
            yield chunk.decode("utf-8") if isinstance(
                chunk, (bytes, bytearray)
            ) else chunk
            std.close(stop_threads=self.__cls._stop_threads)
