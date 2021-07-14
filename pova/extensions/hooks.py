from functools import wraps
from typing import Callable, Any

from pova.cli import broadcast_message


_HOOKS: dict[Any, dict[Any, list]] = {}


def use_before(name: str) -> Callable:
    """Registers a function to be used when calling call_before_hooks().

    Args:
        name (str): The name of the function that you want to preload.
    """
    def decorator(func: Callable) -> Callable:
        _register_hook(func, 'before', name)
        return func
    return decorator


def use_after(name: str):
    """Registers a function to be used when calling call_after_hooks().
    """
    def decorator(func: Callable) -> Callable:
        _register_hook(func, 'after', name)
        return func
    return decorator


def extensible(types_: list) -> Callable:
    """TODO: Add Docstring here"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            name = '.'.join([func.__module__, func.__qualname__])

            # Run the before hooks
            if 'before' in types_:
                _call_hooks('before', name)

            # Run the function
            output = func(*args, **kwargs)

            # Run the after hooks
            if 'after' in types_:
                _call_hooks('after', name)

            return output
        return wrapper
    return decorator


def _register_hook(func: Callable, type_: str, name: str) -> None:
    if _HOOKS.get(name) is None:
        _HOOKS[name] = {}

    if _HOOKS[name].get(type_) is not None:
        _HOOKS[name][type_].append(func)
    else:
        _HOOKS[name][type_] = [func]


def _call_hooks(type_: str, name: str) -> None:
    for hook in _HOOKS.get(name, {}).get(type_, []):
        hook() if callable(hook) else broadcast_message('warn',
                                                        f'Could not call hook. "{hook.__name__}" is not callable.')
