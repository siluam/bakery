# From Imports
from gensing import tea

class tier_:
	"""

		Creates a command based on the arguments and keyword arguments passed in and assign it to
		the class variable "tiered"; the command is then returned, primarily for piping and
		redirection purposes.
		
		This command will have several of its arg and kwarg values, as well as parts of said values,
		replaced with "__tier__". 
		
		When the class instance is called, instead of the regular command condition being run,
		the function creating the new command will replace the prexisting "__tier__"s' in the previous
		command with the arguments passed in with the instance call; only the "args" will be used, however.

		This "tiered" class variable can be reused (unless one uses the "_temp_tiered" keyword argument,
		which resets the "tiered" class variable after creating the command), and therefore any furthur
		attempts to call the instance will utilize the aformentioned variable as the command instead
		of creating a new one. To restore regular usage, run the "flat_()" function
		(not "splat_()", as that is used for the baking function).

		This function allows the user to avoid using partials and temporary functions, such as in a
		case where they want to use a long command in a series of conditionals, but where some values
		differ, while others remain the same. For example:

			echo.tier_("Hello, __tier__!")
			if name == "Queen Elizabeth":
				echo("your majesty") ==> "Hello, your majesty!"
			elif name == "Voldemort":
				echo("He Who Must Not Be Named") ==> "Hello, He Who Must Not Be Named!"
			else:
				echo(name) ==> "Hello, [name]!"

		For a more complicated example:

			https://github.com/shadowrylander/nanotech/blob/master/nanotech/gen_tests.py#L18
			The same line of the link.

	"""

	def tier_(self, *args, **kwargs):

		self.__kwargs = kwargs

		_temp_tiered = self.__kwargs.pop("_temp_tiered", False)

		self.__set_args_kwargs()

		args, self.__kwargs = self._set(self, args, self.__kwargs)

		# If the "tiered" class variable is set, reset it, as we need a new command
		if self.tiered:
			self.tiered = None

		# Create the new "tiered" command
		self.tiered = self._create_command(args, self.__kwargs)

		# Put the original "_starter_args" list back into the variable, and set the temp variable to None
		self._reset_all()

		# If the "_temp_tiered" kwarg is set, return the new command and reset the "tiered" class variable
		if _temp_tiered:
			_ = self.tiered
			self.tiered = tea()
			return _
		# Otherwise, just return the new command in the "tiered" class variable
		else:
			return self.tiered

	def __set_args_kwargs(self):
		"""

			Since we don't want to use the current "_starter_args" list,
			we'll store the current list in its temp variable and get the list
			in the keyword arguments, and an empty list if it doesn't exist.

		"""
		if not self.__kwargs.get("_command_kwargs", False):
			self.__kwargs["_command_kwargs"] = {}
		if not self.__kwargs.get("_starter_args", False):
			self.__kwargs["_starter_args"] = []

	def flat_(self):
		"""

			Disable the "tier" functionality; refer to the "tier_" function for more information.

		"""
		self.tiered = tea()