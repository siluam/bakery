# From Imports
from gensing import tea

class Error(Exception):
	pass


class tbr_not_equal_to_args(Error):
	pass


class _create_command:
	def _create_command(self, _cls = None, _subcommand = "supercalifragilisticexpialidocious"):

		self.__cls = self._cls_check(_cls)
		self.__subcommand = _subcommand

		if self.__cls._frozen:

			return tea(self.__cls._program)

		else:

			_command = tea()

			if self.__cls._sudo:
				_command.append(
					f"sudo -{next(iter(self.__cls._sudo.keys()))} -u {next(iter(self.__cls._sudo.values()))}"
				)

			if self.__cls._shell:
				_command.append(self.__cls._shell + " -c")
				_command.append("'")
				if self.__cls._run_as:
					_command.glue(self.__cls._run_as)
					_command.append(self.__cls._program)
				else:
					_command.glue(self.__cls._program)
			else:
				_command.extend(
					self.__cls._run_as,
					self.__cls._program,
				)

			if self.__cls._sub.processed:
				_command.append(self.__cls._sub.processed)

			# CAREFUL! The order must not change here!
			for c1 in ("starter", "regular"):
				for c2 in ("kwargs", "args"):
					_command.extend(*self.__cls._command.final[self.__subcommand].components[c2][c1])

			if self.__cls._shell:
				_command.glue("'")

			"""

				To use the "_tiered" setting, bake the command in from before with all applicable
				replacements replaced with "{{ b.t }}", and bake in "_tiered" to True; then when
				calling the command, pass in all the arguments that are going to replace the
				"{{ b.t }}" previously baked into the command.

				To reset the command function, use the "splat_" function as necessary.

			"""
			if self.__cls._tiered:

				tier = "{{ b.t }}"

				to_be_replaced = 0
				for value in _command.values():
					if value == tier:
						to_be_replaced += 1
						if to_be_replaced > len(self.__args):
							raise tbr_not_equal_to_args("Sorry! The number of tiered replacements must be equal to the number of arguments provided!")

				if to_be_replaced < len(self.__args):
					raise tbr_not_equal_to_args("Sorry! The number of tiered replacements must be equal to the number of arguments provided!")

				for index, kv in _command.items(indexed = True):
					if kv.value == tier:
						_command[kv.key] = self.__args[index]

			return _command