from typing import Callable

from .classbuild import patchClassBuild


def derive(cls_name: str, callback: Callable, /, *bases, metaclass=None, **kwds):
    @patchClassBuild
    def buildMetaClass():
        global __new__

        def __new__(cls, name, bases, env, *args, **kwds):
            return callback(cls, name, bases, env, args, kwds)

    if metaclass is not None:
        kwds["metaclass"] = metaclass
    return __build_class__(buildMetaClass, cls_name, *bases, **kwds)


__all__ = ["derive"]


def __dir__():
    return __all__
