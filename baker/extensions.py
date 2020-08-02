from typing import Dict, Any

def ext_(
	bakeriy,
	*args,
	_program: str = None,
	_ignore_check: bool = False,
	_baked_commands: Dict[str, Any] = None,
	_baked_settings: Dict[str, Any] = None,
	**kwargs,
):
	"""
		For any programs not in "$PATH", such as scripts;
		useful when used with the "_run_as" keyword argument, such as:
			script = ext_("path/to/script", _baked_settings = dict(_run_as = "/usr/bin/env python"))
	"""
	return bakeriy(
		*args,
		_program = _program or "",
		_ignore_check = _ignore_check,
		_baked_commands = _baked_commands or D({}),
		_baked_settings = _baked_settings or D({}),
		**kwargs,
	)