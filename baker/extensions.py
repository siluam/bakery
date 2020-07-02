def ext_(
    bakeriy,
    program: str,
    *args,
    _ignore_check: bool = False,
    _baked_commands: Dict[str, Any] = D({}),
    _baked_settings: Dict[str, Any] = D({}),
    **kwargs,
):
    """
		For any programs not in "$PATH", such as scripts; useful when used with the "_run_as" keyword argument,
		such as:
			script = ext_("path/to/script", _bake_args = (), _bake_kwargs = dict(_run_as = "python"))
	"""
    return bakeriy(
		program,
		*args,
		_ignore_check = _ignore_check,
		_baked_commands = _baked_commands,
		_baked_settings = _baked_settings,
		**kwargs,
	)


def baker_(
    bakeriy,
    *args,
    _baked_commands: Dict[str, Any] = D({}),
    _baked_settings: Dict[str, Any] = D({}),
    **kwargs,
):
    return bakeriy(
		"",
		*args,
		_ignore_check = True,
		_baked_commands = _baked_commands,
		_baked_settings = _baked_settings,
		**kwargs,
	)
