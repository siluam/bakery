import hy
import sys
import weakref

from addict import Dict
from autoslot import SlotsMeta
from copy import copy, deepcopy
from functools import partial
from inspect import isclass
from itertools import chain, filterfalse
from more_itertools import collapse, peekable
from oreo import (
    eclair,
    first_last_n,
    is_coll,
    is_either,
    is_int,
    tea,
)
from os import environ
from pathlib import Path
from queue import Queue, Empty
from rich import inspect, print
from rich.pretty import pprint, pretty_repr
from shlex import join, split
from subprocess import DEVNULL, PIPE, Popen, STDOUT
from textwrap import TextWrapper
from threading import Thread
from typing import Any
from uuid import uuid4, uuid5
from valiant import SuperPath, dirs, toTuple, filter_options

from .frosting import frosting
from .miscellaneous import *
from .order_cancelled import cancelOrder
from .subcommand import Subcommand


# Adapted From:
# Answer 1: https://stackoverflow.com/a/1800999/10827766
# User 1: https://stackoverflow.com/users/36433/a-coady
# Answer 2: https://stackoverflow.com/a/31537249/10827766
# User 2: https://stackoverflow.com/users/302343/timur
# Answer 3: https://stackoverflow.com/a/66029358/10827766
# User 3: https://stackoverflow.com/users/108205/jsbueno
class melcery(SlotsMeta):
    def __new__(cls, name, bases, ns, slots=tuple()):
        cls._dunder_settings = dunder_settings(name)
        ns["__slots__"] = chain(
            ("__weakref__", "_set_by_property"), cls._dunder_settings, slots
        )
        cls._stores = []
        return super().__new__(cls, name, bases, ns)


# Adapted From: https://github.com/python/typing/issues/345#issuecomment-270814750
# And: https://github.com/cjrh/autoslot#weakref
class milcery(metaclass=melcery):
    # This tells the bakery that the program is a combination of multiple programs,
    # such as `ls | tail'.
    @property
    def _freezer(self):
        return self.__freezer

    @_freezer.setter
    def _freezer(self, value):
        freezer = process_freezer(self.__freezer, value)
        self.__freezer = freezer
        self._freezer_hash = hash(tuple(freezer))

    @property
    def _frozen(self):
        return self.__frozen

    @_frozen.setter
    def _frozen(self, value):
        self.__frozen = bool(value)
        self._dependency_setter("return_output", True)

    @property
    def _model(self):
        return self.__model

    @_model.setter
    def _model(self, value):
        self.__model = bool(value)
        self._dependency_setter("return_output", True)

    @property
    def _call(self):
        return self.__call

    @_call.setter
    def _call(self, value):
        self.__call = bool(value)
        self._dependency_setter("return_output", True)

    # Return the final command
    @property
    def _return_command(self):
        return self.__return_command

    @_return_command.setter
    def _return_command(self, value):
        self.__return_command = bool(value)
        self._dependency_setter("type", str)

    # Print the final command
    @property
    def _print_command(self):
        return self.__print_command

    @_print_command.setter
    def _print_command(self, value):
        self.__print_command = bool(value)
        self._dependency_setter("return_command", True)

    @property
    def _returncodes(self):
        return self.__returncodes

    @_returncodes.setter
    def _returncodes(self, value):
        if is_coll(value):
            self.__returncodes = value
        else:
            self.__returncodes = (value,)

    # Capture types, consisting of `stdout', `stderr', and both
    @property
    def _capture(self):
        return self.__capture

    @_capture.setter
    def _capture(self, value):
        if value in self._captures:
            self.__capture = value
        else:
            raise TypeError(
                f"""Sorry; capture type "{value}" is not permitted! Choose from one of: {', '.join(self._captures)}"""
            )

    @property
    def _run(self):
        return self._capture == "run"

    @_run.setter
    def _run(self, value):
        if value:
            self._dependency_setter("capture", "run")

    @property
    def _stderr_stdout(self):
        return self.__stderr_stdout

    @_stderr_stdout.setter
    def _stderr_stdout(self, value):
        self.__stderr_stdout = bool(value)
        if value:
            self._intact_command = True
            self._dependency_setter("capture", "stderr")

    # Sort the output before it's converted, or if a list, return the sorted list;
    # accepts a value of ~None~ for default sorting.
    @property
    def _sort(self):
        return self.__sort

    @_sort.setter
    def _sort(self, value):
        if value is None or value:
            reverse_default = False
            key_default = None
            if isinstance(value, dict):
                self.__sort = Dict(
                    reverse=value.get("reverse", reverse_default),
                    key=value.get("key", key_default),
                )
            elif is_coll(value):
                self.__sort = Dict(
                    reverse=(
                        [item for item in value if isinstance(item, bool)]
                        or (reverse_default,)
                    )[0],
                    key=([item for item in value if callable(item)] or (key_default,))[
                        0
                    ],
                )
            else:
                self.__sort = Dict()
                if isinstance(value, bool):
                    self.__sort.reverse = value
                else:
                    self.__sort.reverse = reverse_default
                if callable(value):
                    self.__sort.key = value
                else:
                    self.__sort.key = key_default

    # Filter the output before it's converted
    @property
    def _filter(self):
        return self.__filter

    @_filter.setter
    def _filter(self, value):
        if value is None or value:
            reverse_default = False
            key_default = None
            if isinstance(value, dict):
                self.__filter = Dict(
                    reverse=value.get("reverse", reverse_default),
                    key=value.get("key", key_default),
                )
            elif is_coll(value):
                self.__filter = Dict(
                    reverse=(
                        [item for item in value if isinstance(item, bool)]
                        or (reverse_default,)
                    )[0],
                    key=([item for item in value if callable(item)] or (key_default,))[
                        0
                    ],
                )
            else:
                self.__filter = Dict()
                if isinstance(value, bool):
                    self.__filter.reverse = value
                else:
                    self.__filter.reverse = reverse_default
                if callable(value):
                    self.__filter.key = value
                else:
                    self.__filter.key = key_default

    # Shaves off the first or last `n' lines off of `std',
    # whether that be `stdout' or `stderr'.
    @property
    def _n_lines(self):
        return self.__n_lines

    # TODO: Split this into stdout, stderr, and both
    @_n_lines.setter
    def _n_lines(self, value):
        last_default = False
        number_default = 0
        std_default = "stdout"
        if isinstance(value, dict):
            self.__n_lines = Dict(
                last=value.get("last", last_default),
                number=value.get("number", number_default),
                std=value.get("std", std_default),
            )
        elif is_coll(value):
            self.__n_lines = Dict(
                last=(
                    [item for item in value if isinstance(item, bool)]
                    or (last_default,)
                )[0],
                number=([item for item in value if is_int(item)] or (number_default,))[
                    0
                ],
                std=(
                    [item for item in value if isinstance(item, str)] or (std_default,)
                )[0],
            )
        else:
            # Be very careful here; since `bool' is a subclass of `int',
            # we need to first check if `value' is an instance of `bool',
            # then `int', otherwise `(isinstance value int)' will catch both cases.
            self.__n_lines = Dict()
            if isinstance(value, bool):
                self.__n_lines.last = value
            else:
                self.__n_lines.last = last_default
            if is_int(value):
                self.__n_lines.number = value
            else:
                self.__n_lines.number = number_default
            if isinstance(value, str):
                self.__n_lines.std = value
            else:
                self.__n_lines.std = std_default
        if self.__n_lines.std not in (stds := ("stdout", "stderr", "both")):
            raise TypeError(
                f"Sorry; you must choose an `std' value from: {', '.join(stds)}"
            )

    @property
    def _sudo(self):
        return self.__sudo

    @_sudo.setter
    def _sudo(self, value):
        error_message = """Sorry; `_sudo' must be a string of "i" or "s", or a dict-like object of length 1, key "i" or "s", and value `user', or a boolean!"""
        if value:
            if isinstance(value, bool) or len(value) == 1:
                if isinstance(value, str):
                    if value in ("i", "s"):
                        self.__sudo = {value: "root"}
                    else:
                        raise ValueError(error_message)
                elif isinstance(value, bool):
                    self.__sudo = value
                elif isinstance(value, dict):
                    if next(iter(value.keys())) in ("i", "s"):
                        self.__sudo = value
                    else:
                        raise ValueError(error_message)
            else:
                raise ValueError(error_message)

    @property
    def _exports(self):
        return self.__exports

    @_exports.setter
    def _exports(self, value):
        self.__exports = value
        if value:
            self._intact_command = bool(value)

    @property
    def _new_exports(self):
        return self.__new_exports

    @_new_exports.setter
    def _new_exports(self, value):
        self.__new_exports = value
        if value:
            self._intact_command = bool(value)

    def __init__(
        self, *args, program_=None, base_program_=None, freezer_=None, **kwargs
    ):
        if program_:
            self._program = program_.replace("_", "-") or ""
            if "--" in self._program:
                self._program = SuperPath(self._program.replace("--", "."))
            if not check(self, self._program):
                raise ImportError(
                    f"cannot import name '{self._program}' from '{self.__class__.__module__}'"
                )
            self._base_program = base_program_ or self._program
        else:
            self._program = ""
            self._base_program = base_program_ or self._program

        self._id = uuid5(uuid4(), str(uuid4()))
        self._ids = [self._id]

        self._set_by_property = set()

        # Adapted From:
        # Answer 1: https://stackoverflow.com/a/26626707/10827766
        # User 1: https://stackoverflow.com/users/100297/martijn-pieters
        # Answer 2: https://stackoverflow.com/a/328882/10827766
        # User 2: https://stackoverflow.com/users/9567/torsten-marek
        self.__class__._stores.append(weakref.ref(self, self))
        self._flagship = len(self.__class__._stores) == 1
        self._origin = (
            self
            if self._flagship
            else getattr(self.__class__._stores[0], "__callback__")
        )

        self._type_groups = Dict(
            acceptable_args=[str, int, Path],
            reprs=("str", "repr"),
            this_class_subclass=[self.__class__],
            genstrings=(tea,),
            excluded_classes=("type", "filter"),
        )
        self._type_groups.acceptable_args.extend(
            self._type_groups.this_class_subclass + list(self._type_groups.genstrings)
        )

        # NOTE: Subcommand-specific arguments and keyword arguments can only be set via `baking'
        self._subcommand = Subcommand()

        self.__freezer = process_freezer(freezer_)
        self._freezer_hash = hash(tuple(self._freezer))

        self._arg_kwarg_classes = (
            "world",
            "base_programs",
            "base_program",
            "programs",
            "program",
            "freezers",
            "freezer_hash",
            "instantiated",
            "baked",
            "subcommand",
        )
        self._args = Dict(
            world=[] if self._flagship else deepcopy(self._origin._args.world),
            base_program=(
                {self._base_program: []}
                if self._flagship
                else deepcopy(self._origin._args.base_program)
            ),
            program=(
                {self._program: []}
                if self._flagship
                else deepcopy(self._origin._args.program)
            ),
            instantiated=list(args),
            baked={self._subcommand.default: []},
            called=[],
            current=dict(
                unprocessed=dict(starter=[], regular=[]),
                processed=dict(starter=[], regular=[]),
            ),
        )
        self._kwargs = Dict(instantiated=Dict(kwargs))
        if not self._flagship:
            self._kwargs |= {
                kws: deepcopy(self._origin._kwargs.get(kws, Dict()))
                for kws in ("world", "base_program", "program", "freezer")
            }
        self._return_categories = (
            "stdout",
            "stderr",
            "return_codes",
            "command",
            "tea",
            "verbosity",
        )
        self._command = tea()

        # Set `_gitea.bool' to `True',
        # or add the program to `_gitea.list' to allow this program to do something like `git(C = path).status()',
        # and set `_gitea.off' to override and disable both.
        # Named after https://gitea.io/en-us/ and my own https://gitlab.com/picotech/nanotech/gensing modules:
        self._gitea = Dict(
            list=["git", "yadm", "tailapi"],
        )
        self._gitea |= dict(
            bool=self._base_program in self._gitea.list,
            off=False,
        )

        self._return_output_attrs = (
            "call",
            "model",
            "frozen",
            "return_output",
        )
        self._captures = ("stdout", "stderr", "both", "run")
        self._current_settings = Dict()

        # Default settings for certain programs and their subcommands
        for k, v in self.__class__._dunder_settings.items():
            setattr(self, k, deepcopy(v))
        self._settings = Dict(
            defaults=settings(self.__class__)
            # Don't lexically split and join the command.
            # NOTE: This may allow shell-injection attacks.
            | dict(_intact_command=bool(self._freezer))
        )
        self._intact_command = deepcopy(self._settings.defaults._intact_command)

        self._settings.programs.zpool["import"]._sudo = True
        self._settings.programs.zfs.load_key = Dict(_run=True, _sudo=True)
        self._settings.programs.rich[self._subcommand.default]._run = True

    def _dependency_setter(self, name: str, value: Any, force: bool = False):
        if not name.startswith("_"):
            name = "_" + name
        if force or value:
            setattr(self, name, value)
        self._set_by_property.add(name)

    def _set_defaults(self):
        for [key, value] in self._settings.defaults.items():
            setattr(self, key, deepcopy(value))
        self._current_settings.program = (
            self._settings.programs[self._base_program]
            or self._settings.programs[self._base_program.replace("_", "-")]
        )
        for [key, value] in self._current_settings.program[
            self._subcommand.default
        ].items():
            setattr(self, key, deepcopy(value))

    def _process_all(self, *args, **kwargs):
        if not self._freezer:
            for _args in (
                self._args.world,
                self._args.base_program[self._base_program],
                self._args.program[self._program],
                self._args.instantiated,
                self._args.baked[self._subcommand.processed],
            ):
                self._process_args(*_args)
        self._process_args(*args)
        for _kwargs in (
            self._kwargs.world,
            self._kwargs.base_program[self._base_program],
            self._kwargs.program[self._program],
        ):
            self._process_kwargs(**_kwargs)
        self._process_kwargs(
            frozen_kwargs=True,
            **self._kwargs.freezer[self._freezer_hash],
        )
        for _kwargs in (
            self._kwargs.instantiated,
            self._kwargs.baked[self._subcommand.processed],
        ):
            self._process_kwargs(**_kwargs)
        self._process_kwargs(called_kwargs=True, **kwargs)

    def _process_args(self, *args, starter=False):
        sr = "starter" if starter else "regular"
        for arg in args:
            if isinstance(arg, tuple(self._type_groups.acceptable_args)):
                if isinstance(self._args.current.unprocessed[sr], list):
                    self._args.current.unprocessed[sr].append(arg)
                else:
                    self._args.current.unprocessed[sr] = [arg]
            else:
                self._settings.current._frozen = True

    def _process_type(self, attr):
        trimmed_attr = attr.strip("_")
        literal_attr = get_global(trimmed_attr)
        return (
            (not trimmed_attr in self._type_groups.excluded_classes)
            and isclass(literal_attr)
            and isinstance(literal_attr, type)
        ), literal_attr

    def _process_kwargs(self, frozen_kwargs=False, called_kwargs=False, **kwargs):
        def inner(itr, starter=False):
            for key, value in itr.items():
                if key.startswith("_"):
                    match key:
                        case "_starter_args":
                            self._process_args(
                                *toTuple(value),
                                starter=True,
                            )
                        case "_starter_kwargs":
                            inner(value, starter=True)
                        # The values in `_regular_args' will always be appended to `self._args.current.regular',
                        # since `_regular_args' is a keyword argument.
                        case "_regular_args":
                            self._process_args(*value)
                        # NOTE: Depending on where `_regular_kwargs' is in the keyword arguments of the function call,
                        #       its values will replace any prexisting values of the same type; for example, in the following case,
                        #       where `_frozen' is True, while `_regular_kwargs.frozen' is False:
                        #       - If `_regular_kwargs' is before `_frozen', the value of `_frozen' will replace the value of `_regular_kwargs.frozen',
                        #         and final value of `_frozen' will be True
                        #       - If `_regular_kwargs' is after `_frozen', the value of `_regular_kwargs.frozen' will replace the value of `_frozen',
                        #         and final value of `_frozen' will be False
                        #       In other words, the values of whichever comes first will be replaced by the value of whichever comes second.
                        case "_regular_kwargs":
                            inner(value)
                        # Adapted From:
                        # Answer: https://stackoverflow.com/a/70794425/10827766
                        # User: https://stackoverflow.com/users/2988730/mad-physicist
                        case _:
                            is_type, literal_attr = self._process_type(key)
                            if value and is_type:
                                self._settings.current._type = literal_attr
                            else:
                                if not key in ["_" + attr for attr in ("subcommand",)]:
                                    self._settings.current[key] = value
                else:
                    if called_kwargs or not (self._freezer or frozen_kwargs):
                        self._kwargs.current.unprocessed[
                            "starter" if starter else "regular"
                        ][key] = value

        inner(kwargs)

    def _apply_kwargs(self):
        for k, v in self._settings.current.items():
            setattr(self, k, v)
        # This is so that settings set by properties will be overriden
        # by settings during call
        for k, v in self._settings.current.items():
            if k in self._set_by_property:
                setattr(self, k, v)

    def _command_process_args(self, starter=False):
        sr = "starter" if starter else "regular"
        for arg in self._args.current.unprocessed[sr]:
            if isinstance(arg, self._type_groups.genstrings):
                _arg = arg()
            elif isinstance(arg, int):
                _arg = str(arg)
            elif isinstance(arg, self.__class__):
                _arg = arg(_type=str)
            else:
                _arg = arg
            if isinstance(self._args.current.processed[sr], list):
                self._args.current.processed[sr].append(_arg)
            else:
                self._args.current.processed[sr] = [_arg]

    # If the boolean value is non-truthy, don't put the argument in;
    # for example, if `program.subcommand([...], option = False)',
    # then the result would be "program subcommand [...]",
    # i.e. without "--option".
    def _command_process_kwargs(self, starter=False):
        def inner(value):
            if isinstance(value, self._type_groups.genstrings):
                return value()

            # Again, remember that since `bool' is a subclass of `int',
            # we need to first check if `value' is an instance of `bool', then ~int~,
            # otherwise `(isinstance value int)' will catch both cases.
            if isinstance(value, bool):
                return None
            if isinstance(value, int):
                return str(value)

            if isinstance(value, self.__class__):
                return value(_type=str)
            return value

        sr = "starter" if starter else "regular"
        srv = sr + "_values"
        for key, value in self._kwargs.current.unprocessed[sr].items():
            if value:
                aa = tuple(self._type_groups.acceptable_args + [dict, bool])
                if isinstance(value, aa):
                    if isinstance(value, dict):
                        no_value_options = [
                            "repeat",
                            "repeat_with_values",
                            "rwv",
                        ]
                        options = no_value_options + [
                            "fixed",
                            "dos",
                            "one_dash",
                            "value",
                        ]
                        dct_value = value.get("value", None)
                        if dct_value:
                            _value = inner(dct_value)
                        elif any((o in no_value_options for o in value.keys())):
                            _value = None
                        else:
                            raise AttributeError(
                                f"""Sorry; you must use the "value" keyword if you do not use any of the following: {', '.join(no_value_options)}"""
                            )
                        for [k, v] in value.items():
                            if k in options:
                                if v:
                                    if k == "fixed" or self._fixed:
                                        _key = key
                                    else:
                                        _key = key.replace("_", "-")
                                    if k == "dos" or self._dos:
                                        _key = "/" + _key
                                    elif (
                                        (k == "one-dash")
                                        or self._one_dash
                                        or len(_key) == 1
                                    ):
                                        _key = "-" + _key
                                    else:
                                        _key = "--" + _key
                                    if k == "repeat":
                                        _key_values = [_key for i in range(v)]
                                    elif k in ("repeat-with-values", "rwv"):
                                        key_values = []
                                        for j in v:
                                            key_values.append(_key)
                                            if l := inner(j):
                                                if isinstance(
                                                    self._kwargs.current.processed[srv],
                                                    list,
                                                ):
                                                    self._kwargs.current.processed[
                                                        srv
                                                    ].append(l)
                                                else:
                                                    self._kwargs.current.processed[
                                                        srv
                                                    ] = [l]
                                                key_values.append(l)
                                        _key_values = key_values
                                else:
                                    _key = None
                                    _value = None
                                    _key_values = None
                            else:
                                raise AttributeError(
                                    f"Sorry; a keyword argument value of type dict can only have the following keys: {', '.join(options)}"
                                )
                    else:
                        _value = inner(value)
                        _key = key if self._fixed else key.replace("_", "-")
                        if self._dos:
                            _key = "/" + _key
                        elif self._one_dash or len(_key) == 1:
                            _key = "-" + _key
                        else:
                            _key = "--" + _key
                        _key_values = None
                else:
                    raise TypeError(
                        f"""Sorry; the keyword argument value "{value}" of type "{type(value)}" must be one of the following types: {', '.join((arg.__name__ for arg in aa))}"""
                    )
            if _key_values or _key:
                if isinstance(self._kwargs.current.processed[sr], list):
                    if _key_values:
                        self._kwargs.current.processed[sr].extend(_key_values)
                    else:
                        self._kwargs.current.processed[sr].append(_key)
                else:
                    if _key_values:
                        self._kwargs.current.processed[sr] = _key_values
                    else:
                        self._kwargs.current.processed[sr] = [_key]
            if _value and (not _key_values):
                if isinstance(self._kwargs.current.processed[srv], list):
                    self._kwargs.current.processed[srv].append(_value)
                else:
                    self._kwargs.current.processed[srv] = [_value]
                if isinstance(self._kwargs.current.processed[sr], list):
                    self._kwargs.current.processed[sr].append(_value)
                else:
                    self._kwargs.current.processed[sr] = [_value]

    def _return_process_output(self):
        if self._model:
            return self._return_model()
        if self._call:
            return self._return_call()
        if self._frozen:
            return deepcopy(self)
        if self._return_command:
            return self._command()
        output = self._return_process()
        if isinstance(output, dict):
            # output.stderr = peekable(output.stderr)
            stds = ("out", "err")
            if output.returncode and (
                not ((output.returncode in self._returncodes) or self._ignore_stderr)
            ):
                if self._replace_stderr or self._false_stderr:
                    output["stdout"] = self._replace_stderr or False
                else:
                    # exec(
                    #     f"class OrderCancelled_{output.returncode}(OrderCancelled): pass"
                    # )
                    # raise getattr(
                    #     OrderCancelled, f"OrderCancelled_{output.returncode}"
                    # )(
                    # raise eval(f"OrderCancelled_{output.returncode}")(
                    raise cancelOrder(self._command, output)
            for std, opp in zip(stds, stds[::-1]):
                stdstd = "std" + std
                stdopp = "std" + opp
                if self._verbosity < 1 and self._capture == stdstd:
                    output.pop(stdopp, None)
            if self._verbosity < 1:
                del output["returncode"]
        return output

    def _return_model(self):
        settings = []
        for k, v in self._settings.defaults.items():
            if k not in self._return_output_attrs:
                settings.append(hy.models.Keyword(k))
                if isinstance(v, Dict):
                    settings.append(hy.models._dict_wrapper(v))
                elif callable(v):
                    settings.append(hy.models.Symbol(v.__name__))
                else:
                    settings.append(v)
        return hy.models.as_model(
            hy.models.Expression(
                [
                    hy.models.Symbol("bakery"),
                    hy.models.Keyword("program-"),
                    self._program,
                    hy.models.Keyword("base-program-"),
                    self._base_program,
                    hy.models.Keyword("freezer-"),
                    self._freezer,
                    *(settings or []),
                ]
            )
        )

    def _return_call(self):
        settings = ""
        for k, v in self._settings.defaults.items():
            if k not in self._return_output_attrs:
                if isinstance(v, str) and (not v):
                    _v = "''"
                elif callable(v):
                    _v = v.__name__
                else:
                    _v = v
                settings += f""", {k} = {_v}"""
        return f"""bakery(program_ = {self._program or "''"}, base_program_ = {self._base_program}, freezer_ = {self._freezer}{settings})"""

    def _return_process(self):
        if self._command():
            process = self._popen_partial()
            if self._wait is None:
                with process(stdout=DEVNULL, stderr=DEVNULL) as p:
                    return None
            # Adapted From:
            # Answer: https://stackoverflow.com/a/4896288/10827766
            # User: https://stackoverflow.com/users/4279/jfs
            if self._wait:
                with process() as p:
                    _return = Dict()
                    q = Queue()

                    def inner(output, stdstd):
                        if output:
                            chained = []
                            for line in output:
                                if isinstance(line, (bytes, bytearray)):
                                    line = line.decode("utf-8").strip()
                                else:
                                    line = line.strip()
                                chained = chain(chained, [line])
                                if self._dazzling:
                                    q.put(line)
                            _return[stdstd] = iter(chained)

                    threads = []
                    for std in ("out", "err"):
                        stdstd = "std" + std
                        t = Thread(
                            target=inner,
                            args=(
                                getattr(p, stdstd),
                                stdstd,
                            ),
                        )
                        t.daemon = True
                        t.start()
                        threads.append(t)
                    if self._dazzling:
                        while p.poll() is None:
                            try:
                                line = q.get_nowait()
                            except Empty:
                                pass
                            else:
                                print(line)
                    else:
                        p.wait()
                    q.join()
                    for thread in threads:
                        thread.join()
                    _return.returncode = p.returncode
                    if self._verbosity > 0:
                        _return.command.bakery = self._command()
                        _return.command.subprocess = p.args
                        _return.pid = p.pid
                    if self._verbosity > 1:
                        _return.tea = self._command
                        _return.subcommand = self._subcommand
                    first_last_n_part = partial(
                        first_last_n,
                        last=self._n_lines.last,
                        number=self._n_lines.number,
                    )
                    if self._n_lines.std in ("stdout", "both"):
                        _return.stdout = first_last_n_part(iterable=_return.stdout)
                    if self._n_lines.std in ("stderr", "both"):
                        _return.stderr = first_last_n_part(iterable=_return.stderr)

                    return _return
            return process()

    def _type_name_is_string(self, _type=None):
        return getattr(_type or self._type, "__name__") in self._type_groups.reprs

    def _convert_type_filter(self, input):
        if self._filter:
            string_like = isinstance(input, str)
            if self._filter.reverse:
                input = tuple(filterfalse(self._filter.key, input))
            else:
                input = tuple(filter(self._filter.key, input))
            if string_like:
                input = "".join(input)
        return input

    def _convert_type_sort(self, input):
        if self._sort:
            string_like = isinstance(input, str)
            input = sorted(input, **self._sort)
            if string_like:
                input = "".join(input)
        return input

    def _convert_type_convert(self, input, _type=None):
        _type = _type or self._type
        if input:
            if isinstance(input, self._type_groups.genstrings):
                frosted_input = input()
                if self._return_command or self._print_command:
                    pass
                elif isinstance(frosted_input, str):
                    input = TextWrapper(
                        break_long_words=False, break_on_hyphens=False
                    ).wrap(frosted_input)
                elif isinstance(frosted_input, int):
                    if self._type_name_is_string(_type=_type):
                        return pretty_repr(frosted_input)
                    else:
                        return frosted_input
            if self._sort:
                if self._filter:
                    if self._sort_then_filter:
                        input = self._convert_type_filter(
                            self._convert_type_sort(input)
                        )
                    else:
                        input = self._convert_type_sort(
                            self._convert_type_filter(input)
                        )
                else:
                    input = self._convert_type_sort(input)
            elif self._filter:
                input = self._convert_type_filter(input)
            if self._progress and is_coll(input):
                return eclair(input, self._command(), self._progress)
            if self._type_name_is_string(_type=_type):
                return "\n".join(input)
            if self._sort and is_either(_type, list):
                if self._filter:
                    return list(input)
                else:
                    return input
        try:
            return _type()
        except TypeError:
            return _type(input)

    def reset_(
        self,
        world_=False,
        base_programs_=False,
        programs_=False,
        freezers_=False,
        instantiated_=False,
        baked_=False,
        args_=False,
        kwargs_=False,
        all_args_=False,
        all_kwargs_=False,
        all_classes_=False,
        base_program_=None,
        program_=None,
        freezer_hash_=None,
        subcommand_=None,
        set_defaults_=True,
    ):
        self._current_settings = Dict()

        # CAREFUL! These variables need to be before the variables in the block below, and in these orders!
        programs_ = programs_ or program_
        base_programs_ = (
            (self._freezer and program_)
            or (program_ == "")
            or base_programs_
            or base_program_
        )
        freezers_ = freezers_ or freezer_hash_
        baked_ = baked_ or subcommand_

        program_ = program_ or self._program
        base_program_ = (
            (program_ if self._freezer else None)
            or (base_program_ if program_ == "" else None)
            or base_program_
            or self._base_program
        )
        freezer_hash_ = freezer_hash_ or self._freezer_hash
        subcommand_ = Subcommand(None if self._freezer else subcommand_)

        and_args_kwargs = args_ and kwargs_
        args_kwargs = and_args_kwargs or not and_args_kwargs
        and_all_args_kwargs = all_args_ and all_kwargs_
        all_args_kwargs = and_all_args_kwargs or not and_all_args_kwargs

        def inner(store, name, value, default_value=None):
            default_value = default_value or getattr(store, "_" + name)
            if args_ or args_kwargs:
                if all_args_ or all_args_kwargs:
                    store._args[name] = Dict()
                    store._args[name][default_value] = []
                else:
                    store._args[name][value] = []
            if kwargs_ or args_kwargs:
                if all_kwargs_ or all_args_kwargs:
                    store._kwargs[name] = Dict()
                else:
                    store._kwargs[name][value] = Dict()

        for m in ("settings", "args", "kwargs"):
            getattr(self, "_" + m)["current"] = Dict()
        self._args.called = []
        self._kwargs.called = Dict()
        if world_ or all_classes_:
            for store in self.chain_():
                if args_ or args_kwargs:
                    store._args.world = []
                if kwargs_ or args_kwargs:
                    store._kwargs.world = Dict()
        if base_programs_ or all_classes_:
            for store in self.chain_():
                inner(store, "base_program", base_program_)
        if programs_ or all_classes_:
            for store in self.chain_():
                inner(store, "program", program_)
        if freezers_ or all_classes_:
            for store in self.chain_():
                if kwargs_ or args_kwargs:
                    if all_kwargs_ or all_args_kwargs:
                        store._kwargs.freezer = Dict()
                    else:
                        store._kwargs.freezer[freezer_hash_] = Dict()
        if instantiated_:
            if args_ or args_kwargs:
                self._args.instantiated = []
            if kwargs_ or args_kwargs:
                self._args.instantiated = Dict()
        if baked_ or all_classes_:
            inner(
                self,
                "baked",
                subcommand_.processed,
                default_value=subcommand_.default,
            )
        if set_defaults_:
            self._set_defaults()

    def _popen_partial(self, stdout=None, stderr=None):
        command = self._command()

        kwargs = Dict(
            # Adapted From:
            # Answer: https://stackoverflow.com/a/28319191/10827766
            # User: https://stackoverflow.com/users/4279/jfs
            bufsize=1 if self._dazzling else -1,
            # Adapted From:
            # Answer: https://stackoverflow.com/a/4896288/10827766
            # User: https://stackoverflow.com/users/4279/jfs
            close_fds="posix" in sys.builtin_module_names,
            # For some reason, `Popen's env' keyword doesn't like
            # https://github.com/mewwts/addict...
            env=self._new_exports.to_dict() or environ.copy(),
            executable=None,
            shell=self._intact_command,
            stdin=self._input,
            universal_newlines=self._dazzling,
        )

        kwargs.env |= self._exports

        if stderr:
            kwargs.stderr = stderr
        elif (self._capture == "run") or self._stdout_stderr:
            kwargs.stderr = STDOUT
        else:
            kwargs.stderr = PIPE

        if stdout:
            kwargs.stdout = stdout
        elif self._capture == "run":
            kwargs.stdout = None
        else:
            kwargs.stdout = PIPE

        kwargs.text = (kwargs.bufsize == 1) or kwargs.universal_newlines

        kwargs = kwargs.to_dict()
        kwargs |= self._popen

        return partial(
            Popen,
            command
            if self._intact_command
            else join(split(command))
            if kwargs["shell"]
            else split(command),
            **kwargs,
        )

    # f"{_shell} -c ({_freezer} or {_program})
    #                {_kwargs.current.processed.starter}
    #                {_subcommand.current.processed}
    #                {_args.current.processed.starter}
    #                {_kwargs.current.processed.regular}
    #                {_args.current.processed.regular}"
    def _spin(self, *args, subcommand_=None, **kwargs):
        def inner(title):
            opts = self._debug or kwargs.get("_debug", self._debug)
            bool_opts = {}
            if isinstance(opts, dict):
                opts.update({"title": title})
                self.inspect_(**opts)
            else:
                if opts:
                    bool_opts.update(self._default_inspect_kwargs)
                    bool_opts.update({"title": title})
                    self.inspect_(**bool_opts)

        try:
            inner("Setup")
            self._set_defaults()
            if self._freezer:
                self._subcommand = Subcommand()
            else:
                subcommand_ = Subcommand(subcommand_)
                if subcommand_ == self._subcommand.default:
                    for keywords in (
                        self._kwargs.world,
                        self._kwargs.base_program[self._base_program],
                        self._kwargs.program[self._program],
                        self._kwargs.instantiated,
                        self._kwargs.baked[subcommand_.processed],
                        kwargs,
                    ):
                        self._subcommand.extract(**keywords)
                else:
                    self._subcommand = subcommand_
            self._current_settings.subcommand = self._current_settings.program[
                self._subcommand.processed
            ]
            for key, value in self._current_settings.subcommand.items():
                setattr(self, key, deepcopy(value))
            self._args.called = args
            self._kwargs.called = kwargs
            self._process_all(*args, **kwargs)
            self._apply_kwargs()

            inner("Process")
            for i in range(2):
                self._command_process_args(starter=i)
                self._command_process_kwargs(starter=i)

            inner("Create")
            if self._sudo:
                if isinstance(self._sudo, bool):
                    self._command.append("sudo")
                else:
                    self._command.append(
                        f"sudo -{next(iter(self._sudo.keys()))} -u {next(iter(self._sudo.values()))}"
                    )
            if self._shell and (not self._freezer):
                self._command.extend(self._shell, "-c", "'")
                if self._run_as:
                    self._command.glue(self._run_as)
                    self._command.append(self._program)
                else:
                    self._command.glue(self._program)
            else:
                if self._run_as:
                    self._command.extend(self._run_as, self._program)
                else:
                    self._command.append(self._program)
            if self._freezer:
                if self._shell:
                    for [index, value] in enumerate(self._freezer):
                        if value[-1] == "'":
                            self._freezer[index] = value[0:-1]
                self._command.extend(*self._freezer)
            self._command.extend(*self._kwargs.current.processed.starter)
            if self._subcommand != self._subcommand.default:
                self._command.append(self._subcommand.processed)
            self._command.extend(
                *self._args.current.processed.starter,
                *self._kwargs.current.processed.regular,
                *self._args.current.processed.regular,
            )
            self._command.glue("'") if self._shell else None
            if self._tiered:
                tier = "{{ b.t }}"
                replacements = (
                    self._kwargs.current.processed.starter_values
                    + self._args.current.processed.starter
                    + self._kwargs.current.processed.regular_values
                    + self._args.current.processed.regular
                )
                to_be_replaced = self._command.values().count(tier)
                if to_be_replaced == len(replacements):
                    for [index, kv] in self._command.items(indexed=True):
                        if kv.value == tier:
                            self._command[kv.key] = replacements[index]
                else:
                    raise ValueError(
                        "Sorry; the number of tiered replacements must be equal to the number of arguments provided!"
                    )
            if self._stderr_stdout and not self._frozen:
                self._command.append("1>&2")

            inner("Return")
            if output := self._return_process_output():
                if self._return_output:
                    return output
                if self._replace_stderr or self._false_stderr:
                    return output.stdout
                if isinstance(output, dict) and len(output) == 1:
                    frosted_output = next(iter(output.values()))
                else:
                    frosted_output = output
                dict_like_frosted_output = isinstance(frosted_output, dict)
                if self._dazzle:
                    if dict_like_frosted_output:
                        converted_frosted_output = Dict()
                        for k, v in frosted_output.items():
                            v = tuple(v)
                            if v:
                                converted_frosted_output[k] = v
                        frosted_output = converted_frosted_output
                    elif is_coll(frosted_output):
                        frosted_output = tuple(frosted_output)
                    else:
                        frosted_output = (frosted_output,)
                if self._print_command_and_run:
                    print(self._command())
                if self._print_command:
                    print(frosted_output)
                elif self._dazzle:
                    if dict_like_frosted_output:
                        for cat in frosted_output:
                            outcat = output[cat]
                            if isinstance(outcat, int) or isinstance(outcat, str):
                                print(f"{cat}: {outcat}")
                            else:
                                if not cat in self._captures:
                                    print(cat + ": ")
                                if cat == "return-codes":
                                    print(outcat)
                                else:
                                    for line in outcat:
                                        print(line)
                    else:
                        for line in frosted_output:
                            print(line)
                if dict_like_frosted_output:
                    for std in ("out", "err"):
                        stdstd = "std" + std
                        if hasattr(frosted_output, stdstd):
                            processed_output = frosted_output[stdstd]
                            if self._split:
                                processed_output = split_and_flatten(
                                    processed_output, self._split
                                )
                            processed_output = self._convert_type_convert(
                                processed_output
                            )
                            if self._split_after:
                                processed_output = split_and_flatten(
                                    processed_output, self._split_after
                                )
                            frosted_output[stdstd] = processed_output
                            new_frosted_output = frosted_output
                else:
                    new_frosted_output = frosting(frosted_output, self._capture)
                    if self._split:
                        new_frosted_output = split_and_flatten(
                            new_frosted_output, self._split
                        )
                    new_frosted_output = self._convert_type_convert(new_frosted_output)
                    if self._split_after:
                        new_frosted_output = split_and_flatten(
                            new_frosted_output, self._split_after
                        )
                return new_frosted_output

        finally:
            inner("Reset")
            self.reset_()
            if not self._frozen:
                self._command = tea()

    def _apply_pipe_redirect(self, pr, value):
        is_milcery = isinstance(value, self.__class__)

        def inner(v):
            if isinstance(v, self._type_groups.genstrings):
                return [v()]
            if is_milcery:
                return v._freezer or v._command.values() or [v._base_program]
            if isinstance(v, str):
                return [v]
            type_string = ", ".join(
                (
                    t.__name__
                    for t in list(self._type_groups.genstrings)
                    + self._type_groups.this_class_subclass
                    + [str]
                )
            )
            raise NotImplemented(
                f"Sorry; value '{v}' can only be of the following types: {type_string}"
            )

        # If the value is a tuple, assume the first item is the value itself,
        # while the second item is the pipe or redirect;
        # this allows for more compilcated redirects,
        # such as `&>', `2>&1', etc.
        if isinstance(value, tuple):
            if len(value) == 2:
                processed_value = inner(value[0])
                processed_pr = value[1]
            else:
                raise NotImplemented(
                    "Sorry; a tuple value may only contain 2 items: (value, pr)"
                )
        else:
            processed_value = inner(value)
            processed_pr = pr
        kwargs = dict()
        for kws in (
            self._kwargs.world,
            self._kwargs.base_program[self._base_program],
            self._kwargs.program[self._program],
            self._kwargs.freezer[self._freezer_hash],
            self._kwargs.instantiated,
            self._kwargs.baked[self._subcommand.processed],
            self._kwargs.called,
        ):
            kwargs.update(filter_options(**kws))
        if is_milcery:
            for kws in (
                value._kwargs.world,
                value._kwargs.base_program[value._base_program],
                value._kwargs.program[value._program],
                value._kwargs.freezer[value._freezer_hash],
                value._kwargs.instantiated,
                value._kwargs.baked[value._subcommand.processed],
                value._kwargs.called,
            ):
                kwargs.update(filter_options(**kws))
        return self.__class__(
            # Note that `freezer-' will always use the `_freezer' value from the bakery on the left-hand side of the operation calling it
            freezer_=(
                self._freezer or list(self._command.values()) or [self._base_program],
                processed_pr,
                processed_value,
            ),
            base_program_=self._base_program,
            **kwargs,
        )

    def pr_(self, pr, value=""):
        return self._apply_pipe_redirect(pr, value)

    def deepcopy_(self, *args, subcommand_=None, **kwargs):
        return deepcopy(self).bake_(
            *args,
            instantiated_=True,
            _subcommand=Subcommand(subcommand_),
            **kwargs,
        )

    def check_(self):
        return check(self, self._program)

    def freeze_(self):
        self._frozen = True

    def defrost_(self):
        self._frozen = self._settings._frozen

    # https://amoffat.github.io/sh/sections/baking.html arguments and options into the command from before for specific subcommands
    def bake_(
        self,
        *args,
        world_=False,
        base_programs_=False,
        programs_=False,
        freezers_=False,
        instantiated_=False,
        # The default, i.e. just "bake" the current instance.
        baked_=True,
        base_program_=None,
        program_=None,
        freezer_hash_=None,
        subcommand_=None,
        **kwargs,
    ):
        subcommand_ = Subcommand(None if self._freezer else subcommand_)

        # CAREFUL! These variables need to be before the variables in the block below, and in these orders!
        programs_ = programs_ or program_
        base_programs_ = (
            (self._freezer and program_)
            or program_ == ""
            or base_programs_
            or base_program_
        )
        freezers_ = freezers_ or freezer_hash_

        program_ = program_ or self._program
        base_program_ = (
            (program_ if self._freezer else base_program_ if program_ == "" else None)
            or base_program_
            or self._base_program
        )
        freezer_hash_ = freezer_hash_ or self._freezer_hash
        args = list(args)

        # CAREFUL! The order is important here; it is meant to conflict with similar blocks above!
        if world_:
            for store in self.chain_():
                if isinstance(store._args.world, list):
                    store._args.world.extend(args)
                else:
                    store._args.world = args
                store._kwargs.world.update(kwargs)
        elif base_programs_:
            for store in self.chain_():
                if isinstance(
                    (base_program_args := store._args.base_program[base_program_]),
                    list,
                ):
                    base_program_args.extend(args)
                else:
                    base_program_args = args
                store._kwargs.base_program[base_program_].update(kwargs)
        elif programs_:
            for store in self.chain_():
                if isinstance(
                    (program_args := store._args.program[program_]),
                    list,
                ):
                    program_args.extend(args)
                else:
                    program_args = args
                store._kwargs.program[program_].update(kwargs)
        elif freezers_:
            for store in self.chain_():
                store._kwargs.freezer[freezer_hash_].update(kwargs)
        elif instantiated_:
            self._args.instantiated.extend(args)
            self._kwargs.instantiated.update(kwargs)
        else:
            self._args.baked[subcommand_.processed].extend(args)
            self._kwargs.baked[subcommand_.processed].update(kwargs)
        return self

    # Remove baked arguments and options;
    # accepts keyword arguments taken by `reset_'
    def splat_(self, set_defaults_=False, **kwargs):
        if any(kwargs.get(akc, False) for akc in self._arg_kwarg_classes):
            return self.reset_(set_defaults_=set_defaults_, **kwargs)
        else:
            return self.reset_(baked_=True, set_defaults_=set_defaults_, **kwargs)

    # Remove arguments and options from all bakeries;
    # accepts keyword arguments taken by `reset_'.
    # As Baymax would say: Oh no.
    def oh_no_(self, set_defaults_=False, **kwargs):
        for store in self.chain_():
            store.splat_(set_defaults_=set_defaults_, **kwargs)

    # Return an `addict' dictionary with all the current values for the class variables;
    # can be used for debugging purposes or otherwise.
    def current_values_(self):
        return dirs(self)

    # Print an `addict' dictionary with all the current values for the class variables;
    # can be used for debugging purposes or otherwise.
    def print_values_(self):
        pprint(cv := self.current_values_())
        return cv

    # Debug the current function
    def inspect_(self, **kwargs):
        return inspect(self, **(kwargs or self._default_inspect_kwargs))

    # Return a list of all bakeries
    def chain_(self):
        return [store.__callback__ for store in self.__class__._stores]

    def _wrapper(self, *args, **kwargs):
        if kwargs.pop("_context", kwargs.pop("_c", False)):
            return self.deepcopy_(*args, **kwargs)
        elif kwargs.pop("_new_context", kwargs.pop("_nc", False)):
            return self.__class__(
                program_=self._program,
                base_program_=self._base_program,
                *args,
                **kwargs,
            )
        else:
            return self._spin(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if not self._gitea.off and (
            self._gitea.bool or self._base_program in self._gitea.list
        ):
            return self.deepcopy_(_starter_args=args, _starter_kwargs=kwargs)
        else:
            _dazzle = kwargs.pop("_dazzle", is_interactive())
            return self._wrapper(*args, _dazzle=_dazzle, **kwargs)

    def __setattr__(self, name, value):
        if name.startswith("__"):
            if name.endswith("__"):
                object.__setattr__(self, name, value)
            elif name not in self.__class__._dunder_settings:
                raise TypeError(
                    f'Sorry; "{name}" is assumed to be a private setting with a property getter, but it is not in the dictionary of private settings! Please add it there!'
                )
            else:
                object.__setattr__(self, mangle(self, name), value)
        else:
            object.__setattr__(self, name, value)

    def __getattribute__(self, attr):
        if attr.startswith("__"):
            if attr.endswith("__"):
                return object.__getattribute__(self, attr)
            return object.__getattribute__(self, mangle(self, attr))
        return object.__getattribute__(self, attr)

    def __getattr__(self, subcommand):
        if len(subcommand) == 44:
            raise AttributeError
        if subcommand.startswith("_"):
            if subcommand.endswith("__"):
                raise AttributeError
            is_type, literal_attr = self._process_type(subcommand.strip("_"))
            if is_type:
                return self._type == literal_attr
            raise AttributeError
        return partial(self._wrapper, subcommand_=subcommand)

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        for var in collapse(
            getattr(s, "__slots__", []) for s in self.__class__.__mro__
        ):
            if not var in ("__weakref__",):
                setattr(result, var, copy(getattr(self, var)))
        if hasattr(self, "__dict__"):
            result.__dict__.update(self.__dict__)
        result._frozen = result._settings.defaults._frozen
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        if (
            hasattr(self, "_cache")
            and self._cache
            and not isinstance(self._cache, partial)
        ):
            memo[id(self._cache)] = self._cache.__new__(dict)
        for var in collapse(
            getattr(s, "__slots__", []) for s in self.__class__.__mro__
        ):
            if not var in ("__weakref__",):
                setattr(result, var, deepcopy(getattr(self, var), memo))
        if hasattr(self, "__dict__"):
            for [k, v] in self.__dict__.items():
                setattr(result, k, deepcopy(v, memo))
        result._frozen = result._settings.defaults._frozen
        result._id = uuid5(uuid4(), str(uuid4()))
        result._ids.append(result._id)
        return result

    def __repr__(self):
        if is_interactive():
            return self._spin(_str=True)
        else:
            # <bakery.milcery.milcery object at 0x0000000>
            # Adapted From:
            # Answer: https://stackoverflow.com/a/48777036/10827766
            # User: https://stackoverflow.com/users/5770658/internet-user
            return object.__repr__(self)

    def __rich_repr__(self):
        if is_interactive():
            yield from self._spin()
        else:
            yield from self._args.instantiated
            yield "program_", self._program
            yield "base_program_", self._base_program
            yield "freezer_", self._freezer
            for k, v in self._kwargs.instantiated:
                yield k, v

    def __iter__(self):
        return (yield from self._spin())

    def __or__(self, value):
        return self._apply_pipe_redirect("|", value)

    def __and__(self, value):
        return self._apply_pipe_redirect("| tee", value)

    def __add__(self, value):
        return self._apply_pipe_redirect("| tee -a", value)

    def __lt__(self, value):
        return self._apply_pipe_redirect("<", value)

    def __lshift__(self, value):
        return self._apply_pipe_redirect("<<", value)

    def __gt__(self, value):
        return self._apply_pipe_redirect(">", value)

    def __rshift__(self, value):
        return self._apply_pipe_redirect(">>", value)

    def __or__(self, value):
        return self._apply_pipe_redirect("|", value)

    def __and__(self, value):
        return self._apply_pipe_redirect("| tee", value)

    def __add__(self, value):
        return self._apply_pipe_redirect("| tee -a", value)

    def __lt__(self, value):
        return self._apply_pipe_redirect("<", value)

    def __lshift__(self, value):
        return self._apply_pipe_redirect("<<", value)

    def __gt__(self, value):
        return self._apply_pipe_redirect(">", value)

    def __rshift__(self, value):
        return self._apply_pipe_redirect(">>", value)

    def __enter__(self):
        return deepcopy(self)

    def __exit__(self, exception_type, exception_val, exception_traceback):
        pass
