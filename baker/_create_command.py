# From Imports
from gensing import tea

class Error(Exception):
	pass


class tbr_not_equal_to_args(Error):
	pass


class _create_command:
	def _create_command(self, *args, _cls = self, _subcommand = "command", **kwargs):

		self.__args = args
		self.__kwargs = kwargs
		self.__cls = _cls
		self.__subcommand = _subcommand

		_command = tea(
			self.__cls._run_as,
			self.__cls.program,
			*self.__cls._command.baked[self.__subcommand].components.kwargs.starter
			*self.__cls._command.called[self.__subcommand].components.kwargs.starter
		)

		if self._sub.processed and self._sub_before_shell:
			_command.append(self._sub.processed)

		# TODO: Do I put the subcommand before or after the glue?
		if self.__cls._shell:
			_command.glue(" -c '")

		if self._sub.processed and not self._sub_before_shell:
			_command.append(self._sub.processed)

		_command.append(
			*self.__cls._command.baked[self.__subcommand].components.args.starter
			*self.__cls._command.called[self.__subcommand].components.args.starter
			*self.__cls._command.baked[self.__subcommand].components.kwargs.regular
			*self.__cls._command.called[self.__subcommand].components.kwargs.regular
			*self.__cls._command.baked[self.__subcommand].components.args.regular
			*self.__cls._command.called[self.__subcommand].components.args.regular
		)

		if self.__cls._shell:
			_command.glue("'")

		if self.__cls._tiered:

			tier = "{{ b.t }}"

			to_be_replaced = 0
			for value in _command.values():
				if value == tier:
					to_be_replaced += 1
					if to_be_replaced > len(args):
						raise tbr_not_equal_to_args("Sorry! The number of tiered replacements must be equal to the number of arguments provided!")

			if to_be_replaced < len(args):
				raise tbr_not_equal_to_args("Sorry! The number of tiered replacements must be equal to the number of arguments provided!")

			for index, kv in _command.items(indexed = True):
				if kv.value == tier:
					_command[kv.key] = args[index]

		return _command