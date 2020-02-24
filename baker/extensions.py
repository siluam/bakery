def ext_(
	bakeriy,
    program,
    _bake_args=(),
    _bake_kwargs={},
    _bake_after_args=(),
    _bake_after_kwargs={},
):
    """
		For any programs not in "$PATH", such as scripts; useful when used with the "_run_as" keyword argument,
		such as:
			script = ext_("path/to/script", _bake_args = (), _bake_kwargs = dict(_run_as = "python"))
	"""
    return bakeriy(
        program,
        _bake_args=_bake_args,
        _bake_kwargs=_bake_kwargs,
        _bake_after_args=_bake_after_args,
        _bake_after_kwargs=_bake_after_kwargs,
        _ignore_check=True,
    )


def baker_(
	bakeriy,
    _bake_args=(),
    _bake_kwargs={},
    _bake_after_args=(),
    _bake_after_kwargs={},
):
    return bakeriy(
        "",
        _bake_args=_bake_args,
        _bake_kwargs=_bake_kwargs,
        _bake_after_args=_bake_after_args,
        _bake_after_kwargs=_bake_after_kwargs,
        _ignore_check=True,
    )
