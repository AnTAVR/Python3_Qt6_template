__all__ = ['decor_log_debug']

import functools
import logging
from inspect import getfile
from types import FunctionType
from typing import Any


def decor_log_debug(logger_: logging.Logger):
    def decorator(func: FunctionType):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if logger_.isEnabledFor(logging.DEBUG):
                logger_.handle(logger_.makeRecord(
                    logger_.name,
                    logging.DEBUG,
                    getfile(func),
                    func.__code__.co_firstlineno,
                    '{} ARGS{!r} KWARGS{!r}'.format(func.__code__.co_name, args, kwargs),
                    (),
                    None,
                    func.__code__.co_name,
                ))

            ret = func(*args, **kwargs)

            if logger_.isEnabledFor(logging.DEBUG):
                import inspect
                logger_.handle(logger_.makeRecord(
                    logger_.name,
                    logging.DEBUG,
                    inspect.getfile(func),
                    func.__code__.co_firstlineno,
                    '{} RETURN={!r}'.format(func.__code__.co_name, ret),
                    (),
                    None,
                    func.__code__.co_name,
                ))

            return ret

        return wrapper

    return decorator
