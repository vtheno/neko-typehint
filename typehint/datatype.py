from .derive import derive
from .typehint import Typehint


class DataclassSyntaxError(Exception):
    pass


class Empty:
    pass


EMPTY = Empty()


def dataclass_callback(cls, name, bases, env, args, kwds):
    if bases and Dataclass in bases:
        specifications = env.get("__annotations__", None)
        env["_specifications"] = specifications
        if specifications is not None:
            for field_name, field_type in specifications.items():
                if not isinstance(field_type, Typehint):
                    raise DataclassSyntaxError(
                        f"{name}.{field_name} require Typehint instance"
                    )

            def __init__(self, **kwds):
                # for field_name in self._specifications.keys():
                #     if kwds.get(field_name, EMPTY) is EMPTY:
                #         raise TypeError("{self!s} missing {field_name!s} field")

                for field_name, field_type in self._specifications.items():
                    field_value = kwds.get(field_name, None)
                    field_value = field_type.value_struct(
                        value=field_value, msg=f"{name}.{field_name} require {field_type!r} but got {field_value!r}"
                    )
                    setattr(self, field_name, field_value)

            def __repr__(self):
                temp = ", ".join(
                    f"{field_name}={{ {getattr(self, field_name)!r} }}"
                    for field_name in self._specifications.keys()
                )
                return f"{name!s}({temp!s})"

            env["__init__"] = __init__
            env["__repr__"] = __repr__

            env["__solts__"] = tuple(["_specifications"] + list(specifications.keys()))
        else:
            raise DataclassSyntaxError("not support yet")
    return type.__new__(cls, name, bases, env)


MetaDataclass = derive("MetaDataclass", dataclass_callback, type)


class Dataclass(metaclass=MetaDataclass):
    pass


__all__ = ["MetaDataclass", "Dataclass", "DataclassSyntaxError"]


def __dir__():
    return __all__
