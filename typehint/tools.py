import inspect
from typing import Any, Callable, Optional

from .datatype import MetaDataclass
from .typehint import Typehint, TypehintSyntaxError


class Box(Typehint):
    """
    Box(Typehint) is a wrap for other types
    """

    def init(self, in_type):
        if isinstance(in_type, MetaDataclass):
            raise TypehintSyntaxError("Box not accept MetaDataclass instance")
        if not isinstance(in_type, (type, Typehint)):
            raise TypehintSyntaxError(
                "Box just accept type instance of Typehint instance"
            )
        self.type = in_type

    def string(self):
        return f"Box {{ {self.type!r} }}"

    def value_struct(self, value: Any, msg: Optional[str] = None) -> Any:
        return value

    def typecheck(self, value: Any) -> bool:
        return isinstance(value, self.type)


class Data(Typehint):
    """
    Data(Typehint) is a wrap for Dataclass
    """

    def init(self, in_type):
        if not isinstance(in_type, MetaDataclass):
            raise TypehintSyntaxError("Data just accept MetaDataclass instance")
        self.type = in_type

    def string(self):
        return f"Data {{ {self.type!r} }}"

    def value_struct(self, value: Any, msg: Optional[str] = None) -> Any:
        if isinstance(value, dict):
            return self.type(**value)
        return value

    def typecheck(self, value: Any) -> bool:
        if isinstance(value, dict):
            checks = [
                isinstance(value.get(field_name, None), field_type)
                for field_name, field_type in self.type._specifications.items()
            ]
            return checks and all(checks)
        return isinstance(value, self.type)


class Option(Typehint):
    def init(self, in_type):
        self.type = in_type

    def string(self):
        return f"Option {{  {self.type!r} }}"

    def typecheck(self, value: Any) -> bool:
        return value is None or isinstance(value, self.type)


class Lazyhint(Typehint):
    def init(self, callback: Callable):
        self.callback = callback
        self._cached_type = None

    def string(self):
        if self._cached_type is not None:
            return f"Lazyhint {{ {self._cached_type!r} }}"
        return f"Lazyhint {{ {inspect.getsource(self.callback) !r} }}"

    def typecheck(self, value: Any) -> bool:
        if self._cached_type is None:
            self._cached_type = self.callback()
        return isinstance(value, self._cached_type)


__all__ = ["Box", "Data", "Option", "Lazyhint"]


def __dir__():
    return __all__
