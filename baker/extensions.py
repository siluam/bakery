def ext_(
    bakeriy,
    _program: str,
    *args,
    _ignore_check: bool = False,
    _baked_commands: Dict[str, Any] = None,
    _baked_settings: Dict[str, Any] = None,
    **kwargs,
):
    """
		For any programs not in "$PATH", such as scripts; useful when used with the "_run_as" keyword argument,
		such as:
			script = ext_("path/to/script", _bake_args = (), _bake_kwargs = dict(_run_as = "python"))
	"""
    return bakeriy(
		_program,
		*args,
		_ignore_check = _ignore_check,
		_baked_commands = _baked_commands or D({}),
		_baked_settings = _baked_settings or D({}),
		**kwargs,
	)


def baker_(
    bakeriy,
    *args,
    _baked_commands: Dict[str, Any] = None,
    _baked_settings: Dict[str, Any] = None,
    **kwargs,
):
    return bakeriy(
		"",
		*args,
		_ignore_check = True,
		_baked_commands = _baked_commands or D({}),
		_baked_settings = _baked_settings or D({}),
		**kwargs,
	)
