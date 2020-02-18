# From Imports
from functools import partial
from nanite import module_installed, fullpath
from typing import MutableSequence as MS, Dict, Any

_milcery = module_installed(
    fullpath("_milcery.py", f_back=2)
)._milcery


class i(_milcery):
    def __init__(
        self,
        program: str,
        *args,
        ignore_check: bool = False,
        _bake_args: MS[Any] = (),
        _bake_kwargs: Dict[str, Any] = {},
        _bake_after_args: MS[Any] = (),
        _bake_after_kwargs: Dict[str, Any] = {},
        **kwargs,
    ):
        super().__init__(
            program,
            *args,
            ignore_check,
            _bake_args,
            _bake_kwargs,
            _bake_after_args,
            _bake_after_kwargs,
            **kwargs,
        )

    def _(self, *args, **kwargs):
        return self._run_frosting(args, kwargs)

    @property
    def __call__(self):
        return partial(i, self.program)


def __getattr__(program):
    """
		Answer 1: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56786875#56786875
		User 1:   https://stackoverflow.com/users/1016216/l3viathan

		Answer 2: https://stackoverflow.com/questions/56786604/import-modules-that-dont-exist-yet/56795585#56795585
		User 2:   https://stackoverflow.com/users/3830997/matthias-fripp

		Modified by me
	"""
    if program == "__path__":
        raise AttributeError

    return i(program)
