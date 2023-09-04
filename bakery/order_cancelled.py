# class MetaCancelled(type):
#     def __getattr__(cls, attr):
#         return type(attr, (cls,), dict(__hash__=lambda self: attr.split("_")[1]))


# class OrderCancelled(Exception, metaclass=MetaCancelled):
#     pass

# Adapted From: https://github.com/amoffat/sh/blob/develop/sh.py

import re
import signal

from locale import getpreferredencoding
from oreo import tea
from typing import Dict, Type

DEFAULT_ENCODING = getpreferredencoding() or "UTF-8"


class OrderCancelledMeta(type):
    """a metaclass which provides the ability for an OrderCancelled (or
    derived) instance, imported from one sh module, to be considered the
    subclass of OrderCancelled from another module.  this is mostly necessary
    in the tests, where we do assertRaises, but the OrderCancelled that the
    program we're testing throws may not be the same class that we pass to
    assertRaises
    """

    def __subclasscheck__(self, o):
        other_bases = set([b.__name__ for b in o.__bases__])
        return self.__name__ in other_bases or o.__name__ == self.__name__


class OrderCancelled(Exception):
    __metaclass__ = OrderCancelledMeta

    """Base class for all exceptions as a result of a command's exit status
    being deemed an error. This base class is dynamically subclassed into
    derived classes with the format: OrderCancelled_NNN where NNN is the exit
    code number. The reason for this is it reduces boiler plate code when
    testing error return codes:

        try:
            some_cmd()
        except OrderCancelled_12:
            print("couldn't do X")

    vs:

        try:
            some_cmd()
        except OrderCancelled as e:
            if e.exit_code == 12:
                print("couldn't do X")

    It's not much of a savings, but I believe it makes the code easier to read."""

    def __reduce__(self):
        return self.__class__, (self.cmd(), self.output.stdout, self.output.stderr)

    def __init__(self, cmd: tea, output: Dict):
        self.cmd = cmd
        self.output = output
        stdout = "\n".join(self.output.stdout)
        stderr = "\n".join(self.output.stderr)
        msg = "\n\n  ".join(
            filter(
                None,
                (
                    f"\n\n  RAN: {self.cmd()}",
                    f"RETURNCODE: {self.output.returncode}",
                    f"STDOUT:\n{stdout}" if stdout else "",
                    f"STDERR:\n{stderr}" if stderr else "",
                ),
            )
        ).rstrip()

        super(OrderCancelled, self).__init__(msg)


class SignalException(OrderCancelled):
    pass


rc_exc_cache: Dict[str, Type[OrderCancelled]] = {}

SIGNAL_MAPPING = dict(
    [(v, k) for k, v in signal.__dict__.items() if re.match(r"SIG[a-zA-Z]+", k)]
)


def get_exc_from_name(name):
    """takes an exception name, like:

        OrderCancelled_1
        SignalException_9
        SignalException_SIGHUP

    and returns the corresponding exception.  this is primarily used for
    importing exceptions from sh into user code, for instance, to capture those
    exceptions"""

    exc = None
    try:
        return rc_exc_cache[name]
    except KeyError:
        m = re.compile(r"(OrderCancelled|SignalException)_((\d+)|SIG[a-zA-Z]+)").match(
            name
        )
        if m:
            base = m.group(1)
            rc_or_sig_name = m.group(2)

            if base == "SignalException":
                try:
                    rc = -int(rc_or_sig_name)
                except ValueError:
                    rc = -getattr(signal, rc_or_sig_name)
            else:
                rc = int(rc_or_sig_name)

            exc = get_rc_exc(rc)
    return exc


def get_rc_exc(rc):
    """takes a exit code or negative signal number and produces an exception
    that corresponds to that return code.  positive return codes yield
    OrderCancelled exception, negative return codes yield SignalException

    we also cache the generated exception so that only one signal of that type
    exists, preserving identity"""

    try:
        return rc_exc_cache[rc]
    except KeyError:
        pass

    if rc >= 0:
        name = f"OrderCancelled_{rc}"
        base = OrderCancelled
    else:
        name = f"SignalException_{SIGNAL_MAPPING[abs(rc)]}"
        base = SignalException

    exc = OrderCancelledMeta(name, (base,), {"exit_code": rc})
    rc_exc_cache[rc] = exc
    return exc


def cancelOrder(cmd: tea, output: Dict):
    return get_rc_exc(output.returncode)(cmd, output)
