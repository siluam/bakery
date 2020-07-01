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
			*self.__cls._command.final[self.__subcommand].components.kwargs.starter
		)

		if self.__cls._shell:
			_command.glue(" -c '")

		_command.append(
			*self.__cls._command.final[self.__subcommand].components.args.starter
			*self.__cls._command.final[self.__subcommand].components.kwargs.regular
			*self.__cls._command.final[self.__subcommand].components.args.regular
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