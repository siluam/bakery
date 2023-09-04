import __main__
import builtins
import sys

from addict import Dict
from inspect import currentframe
from more_itertools import collapse
from oreo import is_coll
from shutil import which


dunder_settings = lambda obj: Dict(
    {
        "_" + k: v
        for k, v in dict(
            # Whether the bakery is being used with a context manager
            context=False,
            # Pretty print the output
            dazzle=False,
            # Pretty print the output as it is generated;
            # note that the default value is `None' to align with `subprocess.Popen's universal_newlines' default value
            dazzling=None,
            # Print all the current values after each step;
            # accepts a boolean or a dictionary of options passed to https://rich.readthedocs.io/en/latest/reference/init.html#rich.inspect
            debug=False,
            default_inspect_kwargs=dict(all=True),
            # Use a single forward slash instead of a dash for options, as `DOS' expects
            dos=False,
            # Instead of raising a `SystemError', return `False'
            false_stderr=False,
            # Whether to keep underscores in program options instead of replacing them with dashes
            fixed=False,
            # Ignore standard error
            ignore_stderr=False,
            # Ignore standard output
            ignore_stdout=False,
            # Used to pass input to the `subprocess.Popen' class;
            # note that `_popen.stdin' overrides this.
            input=None,
            # Whether to keep options as they are, not replacing underscores with dashes
            intact_option=False,
            # Whether to use one dash for program options,
            # such as in the case of `find'
            one_dash=False,
            # A dictionary used to pass options to the `subprocess Popen' class
            popen=dict(),
            # Print the command and continue running.
            # A good way to debug commands is to see what the command actually was
            # use the `_print_command_and_run' keyword argument to print the final command and continue running.
            print_command_and_run=False,
            # If the final output is an iterable,
            # return it wrapped in an https://rich.readthedocs.io/en/stable/reference/progress.html progress bar;
            # accepts a color string value.
            progress=None,
            # An alternate way to pass arguments to the program as a separate list
            regular_args=tuple(),
            # An alternate way to pass options to the program as a separate dictionary
            regular_kwargs=dict(),
            # Instead of raising a `SystemError', return another value
            replace_stderr=False,
            # Return output as usual
            return_output=False,
            # Run bakery as program; useful when `_program' is a path to a script
            run_as="",
            # What shell to use
            shell=None,
            # Sort then filter the output, if both settings are enabled
            sort_then_filter=False,
            # Split the output by newlines, tabs, spaces, etc. if set to `True',
            # or else by the value provided
            split=False,
            # Split after converting the output, and optionally sorting and filtering
            split_after=False,
            # Pipe STDERR to STDOUT
            stdout_stderr=False,
            # To use the `_tiered' setting, bake the command in from before with all applicable
            # replacements replaced with `{{ b.t }}', and bake in `_tiered' to True; then when
            # calling the command, pass in all the arguments that are going to replace the
            # `{{ b.t }}' previously baked into the command.
            # To reset the command function, use the `splat-' function as necessary.
            tiered=False,
            # `_type' can be any available type, such as:
            # - iter
            # - list
            # - tuple
            # - set
            # - frozenset
            type=iter,
            # How verbose the output should be
            verbosity=0,
            # - If set to True, `_capture = "run"' will wait for the process to finish before returning an addict dictionary of values depending on `_return' and `_verbosity'
            # - If set to False, `_capture = "run"' will return the `Popen' object
            # - If set to None, `_capture = "run"' will wait for the process to finish before returning None
            wait=True,
        ).items()
    }
    | {
        f"_{obj if isinstance(obj, (str, bytes, bytearray)) else obj.__name__}__" + k: v
        for k, v in dict(
            # Return a function call which can be evaluated
            call=False,
            # Which output stream to capture; values are listed below in `_captures'
            capture="stdout",
            # Environment variables to be set while running the command,
            # passed in as dictionary of variable names and values.
            exports=dict(),
            # Filter the output before it's converted
            filter=False,
            # Return the bakery just before running the command;
            # any type not in `type_groups.acceptable_args' will freeze the bakery.
            frozen=False,
            # Return a Hy Model
            model=False,
            # How many lines of output to return; can chop `n' lines off the top or bottom.
            # Can accept a singular value of a boolean, string, or integer, a tuple of the same types,
            # or a dictionary of `{ "last": [bool], "number": [int], "std": [string of "stdout", "stderr", or "both"] }'
            n_lines=dict(last=False, number=0, std="stdout"),
            # Environment variables to be set while running the command,
            # COMPLETELY REPLACING THE OLD ENVIRONMENT,
            # passed in as dictionary of variable names and values
            new_exports=dict(),
            # Print the returned command from the setting above.
            # A good way to debug commands is to see what the command actually was
            # use the `_print_command' keyword argument to print the final command.
            print_command=False,
            # Allow more return codes
            returncodes=[],
            # Return the command itself instead of the output of the command.
            # A good way to debug commands is to see what the command actually was
            # use the `_return_command' keyword argument to return the final command.
            return_command=False,
            # Sort the output before it's converted, or if a list, return the sorted list;
            # accepts a value of `None' for default sorting
            sort=False,
            # Pipe STDOUT to STDERR
            stderr_stdout=False,
            # May be a string of length 1, and value `i' or `s', or a boolean.
            # If a dict-like object, must be in the form {"i" : user} or {"s" : user},
            # to use or not use the configuration files of the specified user.
            sudo=False,
        ).items()
    },
)

settings = lambda obj: {"_" + k.strip("_"): v for k, v in dunder_settings(obj).items()}


def get_global(attr, default=None):
    # Adapted From:
    # Answer 1: https://stackoverflow.com/a/58598665/10827766
    # User 1: https://stackoverflow.com/users/100297/martijn-pieters
    # Answer 2: https://stackoverflow.com/a/40690954/10827766
    # User 2: https://stackoverflow.com/users/320726/6502
    frame = currentframe()
    while frame:
        if attr in frame.f_globals:
            return frame.f_globals[attr]
        frame = frame.f_back
    return getattr(builtins, attr, default)


def process_freezer(freezer, *value):
    if not freezer:
        freezer = []
    elif is_coll(value):
        freezer = list(collapse((freezer, value)))
    else:
        raise TypeError(
            f'Sorry; the "freezer" can only accept non-string iterables or non-truthy values!'
        )
    return freezer


def split_and_flatten(iterable, delim):
    return list(
        collapse(
            j.split() if isinstance(delim, bool) else j.split(str(delim))
            for j in collapse(iterable)
        )
    )


def check(self, program):
    return None if which(program) is None else self


def mangle(self, k):
    return (
        ("_" + object.__getattribute__(self, "__class__").__name__ + k)
        if k.startswith("__")
        else k
    )


# Adapted From:
# Answer: https://stackoverflow.com/a/64523765/10827766
# User: https://stackoverflow.com/users/3620725/pyjamas
def is_interactive():
    return (
        hasattr(sys, "ps1")
        or hasattr(sys, "ps2")
        or sys.__stdin__.isatty()
        or sys.__stdout__.isatty()
        or hasattr(__builtins__, "__IPYTHON__")
        # or not hasattr(__main__, "__file__")
        or bool(sys.flags.interactive)
    )
