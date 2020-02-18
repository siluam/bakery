# From Imports
from nanite import gensing

class _create_command:

	"""

		Example final commands are below:

			***

			Code:

				from bakery import ext_
				script = ext_()
				script
					OR
				script = ext_()
					OR
				script = ext_()

			self.__command = python3 script.py arg1 arg2

			Where:

				self._run_as = python3
				self.program = script.py
				self.cake / self.after_cake = arg1 arg2 (or it can be attached to the command
														 after the preliminary command is created,
														 when passed in while calling the function.)

			***

			self.__command = [hg example]

			***

			self.__command = [git example]

	"""

	def _create_command(self, args, kwargs):

		self.__args = args
		self.__kwargs = kwargs

		if self.tiered:
			self.__tiered()

		else:
			
			self.__prepare_command()

			self.__kwargs = {
				key: value
				for key, value in self.__kwargs.items()
				if key[0] != "_"
			}

			self.__command = self._attach_command_args_kwargs(
				self.__command, args, self.__kwargs
			)

			# End args is global because otherwise it would be incorporated into the self.__kwargs above
			self.__command = self._attach_command_args_kwargs(
				self.__command, self._end_args, self._end_kwargs
			)

			if self._shell:
				self.__command.glue("'")

		return self.__command

	def __tiered(self):

		# The good thing about assigning self.tiered to self.__command is that self.tiered can be reused
		self.__command = self.tiered

		for argument in self.__args:
			for part in (self.__command):
				if "__tier__" in part:
					part.replace("__tier__", str(argument))
					break
					
	def __prepare_command(self):

		self.__command = gensing()

		self.__command.append(
			(
				self.__kwargs.pop("_beg_command", ""),
				self._run_as,
				self.program,
			)
		)

		self.__command = self._attach_command_args_kwargs(
			self.__command, self._before_args, self._before_kwargs
		)

		if self._shell:
			if self.__kwargs.pop(
				"_sub_before_shell", False
			) or not self.__kwargs.pop("_subcommand", False):
				self.__command.glue(" -c '")

		self.__command.append(
			(
				*self.cake,
				self.__kwargs.pop("_end_command", ""),
				*self.after_cake,
			)
		)
		
