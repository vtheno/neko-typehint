from typing import Any, Optional

from .derive import derive


def pop_if_exist(env: dict, source: str, target: str):
    value = env.get(source, None)
    if value is not None:
        env[target] = value
        env.pop(source)


def impl_if_not_exist(name: str, env: dict, source: str):
    value = env.get(source, None)
    if value is None:

        def impl(self, *args, **kwds):
            raise NotImplementedError(f"{name}.{source}(...)")

        env[source] = impl


def typehint_callback(cls, name: str, bases: tuple, env: dict, *args, **kwds):
    if bases and Typehint in bases:
        for source in (
            "init",
            "string",
            "typecheck",
        ):
            impl_if_not_exist(name, env, source)
        pop_if_exist(env, "init", "__init__")
        pop_if_exist(env, "string", "__str__")
        env["__repr__"] = env["__str__"]
        pop_if_exist(env, "typecheck", "__instancecheck__")

        def type_assertion(self, value: Any, msg: Optional[str] = None):
            if not isinstance(value, self):
                tracemsg = msg + " " if msg is not None else ""
                raise TypeError(f"{tracemsg!s}{self!s} is not accept of {value!r}")

        env["type_assertion"] = type_assertion

        custom_value_struct = env.get("value_struct", None)

        if custom_value_struct is None:

            def value_struct(self, value: Any, msg: Optional[str] = None) -> Any:
                self.type_assertion(value=value, msg=msg)
                return value

        else:

            def value_struct(self, value: Any, msg: Optional[str] = None) -> Any:
                self.type_assertion(value=value, msg=msg)
                return custom_value_struct(self, value=value, msg=msg)

        env["value_struct"] = value_struct

    return type.__new__(cls, name, bases, env)


class Typehint(metaclass=derive("Typehint", typehint_callback, type)):
    """
    Typehint just a  combinators.
    equals to some complex isinstance check
    """


class TypehintSyntaxError(Exception):
    pass


"""
Example:
class Point(Dataclass):
    x: Box(int)
    y: Box(int)

class List:
    pass

class Nil(List, Dataclass):
    pass

class Cons(List, Dataclass):
    head: Box(object)
    tail: Box(impl)

"""
__all__ = ["Typehint", "TypehintSyntaxError"]


def __all__():
    return __all__
