from types import CodeType
from typing import Callable

from opcode import opmap, opname


class PatchSyntaxError(Exception):
    pass


def patchClassBuild(func: Callable) -> Callable:
    """
    func: unit -> unit
    """
    mapping = {
        "LOAD_GLOBAL": "LOAD_NAME",
        "STORE_GLOBAL": "STORE_NAME",
        "DELETE_GLOBAL": "DELETE_NAME",
    }
    flag_values = {
        "OPTIMIZED": 1,
        "NEWLOCALS": 2,
        "VARARGS": 4,
        "VARKEYWORDS": 8,
        "NESTED": 16,
        "GENERATOR": 32,
        "NOFREE": 64,
        "COROUTINE": 128,
        "ITERABLE_COROUTINE": 256,
        "ASYNC_GENERATOR": 512,
    }
    mask = sum(
        v
        for k, v in flag_values.items()
        if k
        not in (
            "NEWLOCALS",
            "VARARGS",
            "VARKEYWORDS",
            "GENERATOR",
            "COROUTINE",
            "ITERABLE_COROUTINE",
            "ASYNC_GENERATOR",
        )
    )
    code: CodeType = func.__code__
    if code.co_argcount != 0:
        raise PatchSyntaxError(f"{func} contains arguments")
    if code.co_kwonlyargcount != 0:
        raise PatchSyntaxError(f"{func} contains kwonly arguments")
    if code.co_posonlyargcount != 0:
        raise PatchSyntaxError(f"{func} contains posonly arguments")

    bc = code.co_code
    flags = code.co_flags & mask
    bytecode = []
    for idx in range(0, len(bc), 2):
        op, arg = bc[idx], bc[idx + 1]
        if opname[op] in ("LOAD_GLOBAL", "STORE_GLOBAL", "DELETE_GLOBAL"):
            bytecode += [opmap[mapping[opname[op]]], arg]
        else:
            bytecode += [op, arg]
    func.__code__ = code.replace(co_code=bytes(bytecode), co_flags=flags)
    return func


__all__ = ["patchClassBuild", "PatchSyntaxError"]


def __dir__():
    return __all__
